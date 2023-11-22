import os
import shortuuid
import discord
from discord import app_commands

from bot import TWPlaceClient
from ..modules import logging
from ..modules.supabase import supabaseClient

async def get_confession_channels(interaction: discord.Interaction, client: TWPlaceClient, report: bool = False):
    confessions_enabled = client.guilds_dict[interaction.guild.id][
            "confessions_enabled"
    ]
    confession_logging_enabled = client.guilds_dict[interaction.guild.id][
            "confession_logging_enabled"
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

    return confession_channel, report_channel, confession_logging_enabled

def register_commands(
    tree: discord.app_commands.CommandTree,
    client: TWPlaceClient,
):
    confess_group = app_commands.Group(name="confess", description="Confession commands")
    
    @confess_group.command(
        name="create",
        description="Make an anonymous confession",
    )
    @app_commands.describe(reply_to="The confession id to reply to")
    async def confess(interaction: discord.Interaction, confession: str, reply_to: str = None):
        """Write an anonymous confession.

        Args:
            interaction (discord.Interaction): required by discord.py
            confession (str): The confession to make.
        """

        # Getting the confession channel
        confession_channel, _, confession_logging_enabled = await get_confession_channels(interaction, client)

        try:
            # Building the confession
            confession_id = shortuuid.uuid()
            embed = discord.Embed(title="Confession", description=confession)
            embed.set_footer(text=f"confession id: {confession_id}{' (not logged, unable to report or reply)' if not confession_logging_enabled else ''}")

            reply_to_id = None
            reply_to_message = None

            if reply_to:
                event_log_data = await logging.fetch_event_log(interaction.guild_id, reply_to, 'Confession')
                if not event_log_data:
                    await interaction.response.send_message(
                        "That confession does not exist or could not be fetched from the logs.", ephemeral=True
                    )
                    return
                
                reply_to_confession = event_log_data[0]
                reply_to_id = reply_to_confession["message_id"]
                reply_to_message = await confession_channel.fetch_message(reply_to_id)
                embed.add_field(name="Replying to", value=f"[Confession {reply_to}](https://discord.com/channels/{interaction.guild_id}/{confession_channel.id}/{reply_to_id})")
                
                
            confession_message = await confession_channel.send(embed=embed, reference=reply_to_message)
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
                "mentioned_id": reply_to_id,
            }

            if confession_logging_enabled:
                await logging.log_event(confession_message, log_event, confession)
            await interaction.response.send_message(
                f"Your confession has been sent. See it here: {confession_url}",
                ephemeral=True,
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
        confession_channel, report_channel, confession_logging_enabled = await get_confession_channels(interaction, client, report=True)
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
        if confession_logging_enabled:
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

        confession_channel, _, confession_logging_enabled = await get_confession_channels(interaction, client)
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

        if confession_logging_enabled:
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