from dataclasses import dataclass
import os
import shortuuid
import discord
from discord import app_commands
import validators

from bot import TWPlaceClient
from modules import logging, content_moderation
from modules.supabase import supabaseClient

@dataclass
class ConfessionConfig:
    logging_enabled: bool
    mentioning_enabled: bool
    images_enabled: bool

async def get_confession_config(interaction: discord.Interaction, client: TWPlaceClient, report: bool = False):
    confessions_enabled = client.guilds_dict[interaction.guild.id][
        "confessions_enabled"
    ]
    confession_config = client.guilds_dict[interaction.guild.id][
        "confession_config"
    ]
    if not confessions_enabled:
        await interaction.response.send_message(
            "Confessions are not enabled for this server.", ephemeral=True
        )
        return

    # Getting the confession channel
    confession_channel_id = client.guilds_dict[interaction.guild.id][
        "confession_channel_id"
    ]
    if not confession_channel_id:
        await interaction.response.send_message(
            "This server does not have a confessions channel set up. Please contact an admin to set one up.",
            ephemeral=True,
        )
        return
    
    confession_channel = client.get_channel(confession_channel_id)

    report_channel = None
    if report:
        report_channel_id = client.guilds_dict[interaction.guild.id][
            "report_channel_id"
        ]
        if not report_channel_id:
            await interaction.response.send_message(
                "This server does not have a report channel set up. Please contact an admin to set one up.",
                ephemeral=True,
            )
            return confession_channel, None
        
        report_channel = client.get_channel(report_channel_id)

    return confession_channel, report_channel, ConfessionConfig(**confession_config)

def register_commands(
    tree: discord.app_commands.CommandTree,
    client: TWPlaceClient,
):
    confess_group = app_commands.Group(name="confess", description="Confession commands")
    
    @confess_group.command(
        name="create",
        description="Make an anonymous confession",
    )
    @app_commands.describe(reply_to="The confession or message to reply to (provide either the confession id, message id, or the message link)")
    @app_commands.describe(confession="The confession to make")
    @app_commands.describe(user_to_ping="The user to ping in the confession (only if the server has it enabled)")
    @app_commands.describe(image="An image to attach to the confession (only if the server has it enabled)")
    async def confess(interaction: discord.Interaction, confession: str, reply_to: str = None, user_to_ping: discord.Member = None, image: discord.Attachment = None):
        """Write an anonymous confession.

        Args:
            interaction (discord.Interaction): required by discord.py
            confession (str): The confession to make.
        """

        # Getting the confession channel and config
        confession_channel, _, confession_config = await get_confession_config(interaction, client)
        logging_enabled, mentioning_enabled, images_enabled = confession_config.logging_enabled, confession_config.mentioning_enabled, confession_config.images_enabled

        config_response = ''

        if image:
            if not images_enabled:
                config_response += "This server does not have image confessions enabled.\n"
            else:
                if not image.content_type.startswith('image/'):
                    await interaction.response.send_message(
                        "Please only send images.", ephemeral=True
                    )
                    return
                if not await content_moderation.review_image(image):
                    await interaction.response.send_message(
                        "Image blocked by content moderation. Please only send appropriate images.", ephemeral=True
                    )
                    print(f'Image sent by {interaction.user.display_name} blocked by content moderation: {image.url}')
                    return
                
        if user_to_ping and not mentioning_enabled:
            config_response += "This server does not have confession mentioning enabled.\n"

        try:
            # Building the confession
            confession_id = shortuuid.uuid()
            embed = discord.Embed(title="Confession", description=confession)
            embed.set_footer(text=f"confession id: {confession_id}{' (not logged, unable to report)' if not logging_enabled else ''}")

            reply_to_id: int = None
            reply_to_message = None
            reply_to_type: 'url' | 'generated_id' | 'message_id' | None = None

            if reply_to:
                if reply_to.isdigit():
                    reply_to_type = 'message_id'
                    reply_to_id = int(reply_to)
                elif validators.url(reply_to):
                    reply_to_type = 'url'
                    reply_to_id = int(reply_to.split('/')[-1])
                    reply_to = reply_to_id
                else:
                    reply_to_type = 'generated_id'
                    event_log_data = await logging.fetch_event_log(interaction.guild_id, reply_to, 'Confession')
                    if not event_log_data:
                        await interaction.response.send_message(
                            "That confession does not exist or could not be fetched from the logs.", ephemeral=True
                        )
                        return
                    
                    reply_to_confession = event_log_data[0]
                    reply_to_id = reply_to_confession["message_id"]

                reply_to_message = await confession_channel.fetch_message(reply_to_id)
                embed.add_field(name="Replying to", value=f"[{'Confession ' if reply_to_message.author.id == client.user.id else ''}{reply_to}](https://discord.com/channels/{interaction.guild_id}/{confession_channel.id}/{reply_to_id})")
                
                
            if image and images_enabled:
                embed.set_image(url=image.url)

            confession_message = await confession_channel.send(f"<@{user_to_ping.id}>" if user_to_ping and mentioning_enabled else None, embed=embed, reference=reply_to_message)
            confession_url = confession_message.jump_url

            user_id = interaction.user.id
            server = interaction.guild.name

            log_event = {
                "event": "Confession",
                "author_id": user_id,
                "user": f"<@{user_id}>",
                "server": server,
                "url": confession_url,
                "generated_id": confession_id,
                "metadata": {
                    'replied_to': reply_to_id,
                    'replied_to_type': reply_to_type,
                    'pinged_user': user_to_ping.id if user_to_ping and mentioning_enabled else None,
                    'image': image.url if image and images_enabled else None,
                },
            }

            if logging_enabled:
                await logging.log_event(confession_message, log_event, confession)
            await interaction.response.send_message(
                f"{config_response}Your confession has been sent. See it here: {confession_url}.",
                ephemeral=True,
                suppress_embeds=True,
            )
        except Exception as e:
            await interaction.response.send_message(
                f"Failed to send confession: {e}", ephemeral=True
            )

    @confess_group.command(
        name="report",
        description="Report a confession",
    )
    async def report_confession(interaction: discord.Interaction, confession_id: str, reason: str):
        confession_channel, report_channel, confession_config = await get_confession_config(interaction, client, report=True)
        logging_enabled = confession_config.logging_enabled

        if not report_channel:
            return
        event_log_data = await logging.fetch_event_log(interaction.guild_id, confession_id, 'Confession')

        if not event_log_data:
            await interaction.response.send_message(
                "That confession does not exist or could not be fetched from the logs.", ephemeral=True
            )
            return
        
        confession = event_log_data[0]

        confession_author = confession["author_id"]
        confession_server = client.guilds_dict[confession["guild_id"]]['server_name']
        confession_created_at = confession["created_at"]
        confession_content = confession["content"]
        
        report_embed = discord.Embed(title=f"Confession reported", description=f"Confession {confession_id} reported by <@{interaction.user.id}>", color=discord.Color.red())
        report_embed.add_field(name="reporter", value=f"<@{interaction.user.id}>", inline=False)
        report_embed.add_field(name="reason", value=reason, inline=False)
        report_embed.add_field(name="confession author", value=f"<@{confession_author}>", inline=False)
        report_embed.add_field(name="confession server", value=confession_server, inline=False)
        report_embed.add_field(name="confession created at", value=confession_created_at, inline=False)
        report_embed.add_field(name="confession content", value=confession_content, inline=False)
        report_embed.set_footer(text=f"confession id: {confession_id}")

        confession_embed = discord.Embed(title="Confession", description=f"[This confession was reported]", color=discord.Color.red())
        confession_embed.set_footer(text=f"confession id: {confession_id}")
        confession_message = await confession_channel.fetch_message(confession["message_id"])
        await confession_message.edit(embed=confession_embed)

        report_message = await report_channel.send(embed=report_embed)
    
        log_event = {
            "event": "Confession report",
            "author_id": interaction.user.id,
            "reporter_id": f"<@{interaction.user.id}>",
            "server": interaction.guild.name,
            "reason": reason,
            "confession_author": f"<@{confession_author}>",
            "confession_server": confession_server,
            "confession_created_at": confession_created_at,
            "confession_content": confession_content,
            "generated_id": confession_id,
        }
        if logging_enabled:
            await logging.log_event(report_message, log_event, reason, color=discord.Color.red())

        await interaction.response.send_message(
            "Your report has been sent. Thank you.", ephemeral=True
        )

    @confess_group.command(
        name="restore",
        description="Restores a confession (requires manage server permissions)",
    )
    async def restore_confession(interaction: discord.Interaction, confession_id: str):
        if not interaction.permissions.manage_guild:
            await interaction.response.send_message(
                "You do not have the required permissions to use this command.", ephemeral=True
            )
            return

        confession_channel, _, confession_config = await get_confession_config(interaction, client)
        logging_enabled = confession_config.logging_enabled

        event_log_data = await logging.fetch_event_log(interaction.guild_id, confession_id, 'Confession')

        if not event_log_data:
            await interaction.response.send_message(
                "That confession does not exist.", ephemeral=True
            )
            return
        
        confession = event_log_data[0]

        confession_embed = discord.Embed(title="Confession (Restored by admin)", description=confession["content"])
        confession_embed.set_footer(text=f"confession id: {confession_id}")
        confession_message = await confession_channel.fetch_message(confession["message_id"])

        await confession_message.edit(embed=confession_embed)

        log_event = {
            "event": "Confession restore",
            "author_id": interaction.user.id,
            "restorer_id": f"<@{interaction.user.id}>",
            "server": interaction.guild.name,
            "confession_content": confession["content"],
            "generated_id": confession_id,
        }

        if logging_enabled:
            await logging.log_event(confession_message, log_event, color=discord.Color.green())

        await interaction.response.send_message(
            "The confession has been restored.", ephemeral=True
        )


    tree.add_command(
        confess_group, 
        guilds=[  # Servers with a confessions channel
            discord.Object(id=int(server_id))
            for server_id in client.guilds_dict.keys()
        ],
    )