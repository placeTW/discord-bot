from . import tr_core as core
import discord
from discord import app_commands
from discord.app_commands import Choice
from tabulate import tabulate


def register_commands(tree, this_guild: discord.Object):
    core.commands_initialize_condition.wait()

    track_group = app_commands.Group(
        name="track", description="Set source for language tracking"
    )

    def get_file_progresses(
        locale: str, files: list[str]
    ) -> dict[str, core.transfile_progress]:
        ret: dict[str, core.transfile_progress] = {}
        for file in files:
            ret[file] = core.read_transfile_progress(locale, file)
        return ret

    def progresses_to_str(
        target: dict[str, core.transfile_progress]
    ) -> list[list[str]]:
        return [
            [key, value.progress_str_fwd()] for key, value in target.items()
        ]

    def monospace_filename_table(table: list[str]):
        ret: list[str] = []
        for row in table:
            first_space_index = row.find(' ')
            index = core.re.search(r"[^ ]", row[first_space_index:]).start()
            index += first_space_index
            ret.append("``" + row[:index] + "``" + row[index:])
            print("``" + row[:index] + "``" + row[index:])
        return ret

    def match_table_rows(
        table: list[str], target: list[str]
    ) -> dict[str, str]:
        ret: dict[str, str] = {}
        for item in table:
            for nested_item in target:
                if item.find(nested_item) != -1:
                    ret[nested_item] = item
                    break
        return ret

    async def track_handler(
        interaction: discord.Interaction, locale: str, pr_no: int = None
    ):
        await interaction.response.defer()
        ref = core.trans_db[locale]
        all_progresses = pr_files = master_files = None
        with ref.mutex:
            if pr_no:
                if ref.pr_no and ref.pr_no == pr_no:
                    await interaction.followup.send(
                        content=f"{locale} is already tracking PR {pr_no}"
                    )
                    return
                core.shift2pr(locale, pr_no)
            else:
                if not ref.pr_no:
                    await interaction.followup.send(
                        content=f"{locale} is already tracking Master"
                    )
                    return
                core.shift2master(locale)

            all_progresses = get_file_progresses(locale, ref.all_files())
            tabulate_list = monospace_filename_table(tabulate(
                progresses_to_str(all_progresses), tablefmt="plain"
            ).splitlines(False))
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
            colour=discord.Colour.green()
        )
        embed.add_field(
            name="Files provided by Pull Request",
            value=concat_progress_str(pr_files) if len(pr_files) else "None",
            inline=False,
        )
        embed.add_field(
            name="Files provided by Master",
            value=concat_progress_str(master_files)
            if len(master_files)
            else "None",
        )
        embed.set_footer(
            text="See /trans_stat for more information"
        )
        await interaction.followup.send(content=None, embed=embed)

    @track_group.command(
        description="Set language tracking source to Pull Request",
    )
    @app_commands.choices(
        lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    )
    @app_commands.describe(pr_no="Pull request number")
    async def pr(
        interaction: discord.Interaction, lang: Choice[str], pr_no: int
    ):
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

    @tree.command(
        name="trans_stat",
        description="Check translation progress for language",
        guild=this_guild
    )
    @app_commands.choices(
        lang=[Choice(name=lang, value=lang) for lang in core.trans_db.keys()]
    )
    async def trans_stat(interaction: discord.Interaction, lang: Choice[str]):
        await interaction.response.defer()
        with core.trans_db[lang.value].mutex:
            pass
