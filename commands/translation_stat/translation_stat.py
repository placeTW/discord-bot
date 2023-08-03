from . import tr_core as core
import discord
from discord import app_commands
from discord.app_commands import Choice
import asyncio
from tabulate import tabulate


def register_commands(tree, this_guild: discord.Object):

    with core.commands_initialize_condition:
        if not core.commands_initialize_condition_flag:
            core.commands_initialize_condition.wait()

    # @tree.command(
    #     name="trans_stat",
    #     description="Get translation status",
    #     guild=this_guild,
    # )
    # @discord.app_commands.choices(
    #     lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    # )
    # async def trans_stat(
    #     interaction: discord.Interaction, lang: Choice[str]
    # ):
    #     files_status = core.get_file_stat(lang.value)
    #     files_string = [
    #         f"{key}: {'Available' if value else 'Unavailable'}"
    #         for key, value in files_status.items()
    #     ]
    #     embed = discord.Embed(
    #         title="Translation Status",
    #         description="Comparing {} -> {}".format(lang.value, "en"),
    #     )
    #     embed.add_field(name="Files", value=files_string, inline=False)
    #     await interaction.response.send_message(embed=embed)
    #     return
    #
    # @tree.command(
    #     name="track_pr",
    #     description="Make language track translation pull request",
    #     guild=this_guild,
    # )
    # @discord.app_commands.choices(
    #     lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    # )
    # @app_commands.describe(pr_no="The string you want echoed backed")
    # async def track_pr(
    #     interaction: discord.Interaction, lang: Choice[str], pr_no: int
    # ):
    #     await interaction.response.defer()
    #     ref = core.trans_db[lang.value]
    #     with ref.mutex:
    #         loading_msg = asyncio.create_task(interaction.followup.send(
    #             "Performing action..."
    #         ))
    #         core.shift2pr(lang.value, pr_no)
    #         ref.pr_no = pr_no
    #         embed = discord.Embed(
    #             title=f"Translation for {lang.value}",
    #             description=f"{lang.value} is now tracking PR {ref.pr_no}",
    #         )
    #         pr_files: str = "".join([f"{file} {core.get_transfile_progress(lang.value, file, False).progress_str_fwd()}\n" for file in ref.pr_files])
    #         master_files: str = "".join(
    #             [f"{file}" for file in ref.owned_files]
    #         )
    #         embed.add_field(
    #             name="Files provided by pull request",
    #             value=pr_files if len(pr_files) else "None",
    #             inline=False,
    #         )
    #         embed.add_field(
    #             name="Files provided by master",
    #             value=master_files if len(master_files) else "None",
    #             inline=False,
    #         )
    #         await loading_msg
    #         await interaction.edit_original_response(
    #             content=None, embed=embed
    #         )

    track_group = app_commands.Group(name="track", description="Set source for language tracking")

    def get_file_progresses(locale: str, files: list[str]) -> dict[str, core.transfile_progress]:
        ret: dict[str, core.transfile_progress] = {}
        for file in files:
            ret[file] = core.get_transfile_progress(locale, file, False)
        return ret

    def progresses_to_str(target: dict[str, core.transfile_progress]) -> list[list[str]]:
        return [[key, value.progress_str_fwd()] for key, value in target.items()]

    def match_table_rows(table: list[str], target: list[str]) -> dict[str, str]:
        ret: dict[str, str] = {}
        for item in table:
            for nested_item in target:
                if item.startswith(nested_item):
                    ret[nested_item] = item
                    break
        return ret

    async def track_handler(interaction: discord.Interaction, locale: str, pr_no: int = None):
        await interaction.response.defer()
        ref = core.trans_db[locale]
        all_progresses = pr_files = master_files = None
        info_msg = asyncio.create_task(interaction.followup.send("Performing action..."))
        with ref.mutex:
            if pr_no:
                if ref.pr_no and ref.pr_no == pr_no:
                    await info_msg
                    await interaction.edit_original_response(content=f"{locale} is already tracking PR {pr_no}")
                    return
                ref.pr_no = pr_no
                core.shift2pr(locale, pr_no)
            else:
                if not ref.pr_no:
                    await info_msg
                    await interaction.edit_original_response(content=f"{locale} is already tracking Master")
                    return
                core.shift2master(locale, False)

            all_progresses = get_file_progresses(locale, ref.all_files())
            tabulate_list = tabulate(progresses_to_str(all_progresses), tablefmt="plain").splitlines(False)
            pr_files = match_table_rows(tabulate_list, ref.pr_files)
            master_files = match_table_rows(tabulate_list, ref.owned_files)

        def concat_progress_str(file_progresses: dict[str, str]) -> str:
            nonlocal all_progresses
            ret = str()
            for key, value in file_progresses.items():
                ret += f"{value}\n"
                ret += f"{all_progresses[key].to_progress_str()}\n"
            return ret

        embed = discord.Embed(
            title=f"Source for Language {locale}",
            description=f"{locale} is now tracking {'Master' if not pr_no else f'PR {pr_no}'}",
        )
        embed.add_field(
            name="Files provided by Pull Request",
            value=concat_progress_str(pr_files) if len(pr_files) else "None",
            inline=False
        )
        embed.add_field(
            name="Files provided by Master",
            value=concat_progress_str(master_files) if len(master_files) else "None"
        )
        await info_msg
        await interaction.edit_original_response(
            content=None, embed=embed
        )


    @track_group.command(
        description="Set language tracking source to Pull Request",
    )
    @app_commands.choices(
        lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    )
    @app_commands.describe(pr_no="Pull request number")
    async def pr(interaction: discord.Interaction, lang: Choice[str], pr_no: int):
        await track_handler(interaction, lang.value, pr_no)

    @track_group.command(
        description="Set language tracking source to Master branch",
    )
    @app_commands.choices(
        lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    )
    async def master(interaction: discord.Interaction, lang: Choice[str]):
        await track_handler(interaction, lang.value)

    tree.add_command(track_group, guild=this_guild)
