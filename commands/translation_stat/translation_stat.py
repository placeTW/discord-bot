from . import tr_core as core
import discord
from discord import app_commands
from discord.app_commands import Choice
import asyncio


def register_commands(tree, this_guild: discord.Object):

    with core.commands_initialize_condition:
        if not core.commands_initialize_condition_flag:
            core.commands_initialize_condition.wait()

    @tree.command(
        name="trans_stat",
        description="Get translation status",
        guild=this_guild,
    )
    @discord.app_commands.choices(
        lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    )
    async def trans_stat(
        interaction: discord.Interaction, lang: Choice[str]
    ):
        files_status = core.get_file_stat(lang.value)
        files_string = [
            f"{key}: {'Available' if value else 'Unavailable'}"
            for key, value in files_status.items()
        ]
        embed = discord.Embed(
            title="Translation Status",
            description="Comparing {} -> {}".format(lang.value, "en"),
        )
        embed.add_field(name="Files", value=files_string, inline=False)
        await interaction.response.send_message(embed=embed)
        return

    @tree.command(
        name="track_pr",
        description="Make language track translation pull request",
        guild=this_guild,
    )
    @discord.app_commands.choices(
        lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    )
    @app_commands.describe(pr_no="The string you want echoed backed")
    async def track_pr(
        interaction: discord.Interaction, lang: Choice[str], pr_no: int
    ):
        await interaction.response.defer()
        with core.trans_db[lang.value].mutex:
            loading_msg = asyncio.create_task(interaction.followup.send(
                "Performing action..."
            ))
            core.shift2pr(lang.value, pr_no)
            ref = core.trans_db[lang.value]
            ref.pr_no = pr_no
            embed = discord.Embed(
                title=f"Translation for {lang.value}",
                description=f"{lang.value} is now tracking PR {ref.pr_no}",
            )
            pr_files: str = "".join([f"{file} {core.get_transfile_progress(lang.value, file, False).progress_str_fwd()}\n" for file in ref.pr_files])
            master_files: str = "".join(
                [f"{file}" for file in ref.owned_files]
            )
            embed.add_field(
                name="Files provided by pull request",
                value=pr_files if len(pr_files) else "None",
                inline=False,
            )
            embed.add_field(
                name="Files provided by master",
                value=master_files if len(master_files) else "None",
                inline=False,
            )
            await loading_msg
            await interaction.edit_original_response(
                content=None, embed=embed
            )
