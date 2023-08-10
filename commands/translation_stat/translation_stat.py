from code import interact
from . import tr_core as core
import discord
from discord import app_commands
from discord.app_commands import Choice
from tabulate import tabulate


class MoreDetailsButtonView(discord.ui.View):
    def __init__(self, progresses: dict[str, core.transfile_progress], files_not_found: list[str]):
        super().__init__()
        self.progresses = progresses
        self.files_not_found = files_not_found

    @discord.ui.button(label="More Details", style=discord.ButtonStyle.primary, emoji='ℹ️')
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.button):
        await interaction.response.defer()
        if (len(self.files_not_found)):
            await interaction.channel.send("Files not found:\n".join(f"{item}\n" for item in self.files_not_found))

        messages: list[str] = []
        for key, value in self.progresses.items():
            table = [["Field", "Status"]]
            table.extend([[field, "Available" if status else "Unavailable"] for field, status in value.all_fields.items()])
            messages.append(f"\n{key}:\n" + tabulate(table, headers='firstrow', tablefmt='simple'))

        for message in messages:
            tmp = "```"
            for line in message.splitlines():
                if len(tmp) + 4 + len(line) > 2000:
                    await interaction.channel.send( tmp + "\n```")
                    tmp = "```"
                else:
                    tmp += f"\n{line}"
            await interaction.channel.send(tmp + "\n```")
        

def register_commands(tree, this_guild: discord.Object):

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
        if locale != core.main_lang:
            core.require_locale(core.main_lang)
        core.require_locale(locale)
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
            text=f"See /trans_stat {locale} for more information"
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
        ref = core.trans_db[lang.value]
        embed: discord.Embed = None
        with ref.mutex:
            main_lang_progresses = core.gen_mainlang_progress_map(lang.value != core.main_lang)
            if (lang.value != core.main_lang):
                core.require_locale(core.main_lang)
            core.require_locale(lang.value, main_lang_progresses)
            all_progresses = get_file_progresses(lang.value, ref.all_files())
            all_progresses_str = progresses_to_str(all_progresses)
        files_not_found: list[str] = []
        for item in main_lang_progresses.keys():
            if not all_progresses.get(item):
                files_not_found.append(item)
        files_available = f"{len(all_progresses.keys())}/{len(main_lang_progresses.keys())}"

        def get_total_progress(base: list[core.transfile_progress], target: list[core.transfile_progress]) -> str:
            all_available_indexes = int()
            all_total_indexes = int()
            for item in base:
                all_total_indexes += item.total_indexes
            for item in target:
                all_available_indexes += item.ready_indexes
            return f"{all_available_indexes}/{all_total_indexes}, {core.float_to_percentage(all_available_indexes / all_total_indexes)}%"
        total_progress = get_total_progress(main_lang_progresses.values(), all_progresses.values())
        embed = discord.Embed(
            title=f"Translation Progress for Language {lang.value}",
            description=f"Files: {files_available}, Indexes: {total_progress}",
            colour=discord.Colour.green()
        )
        embed.add_field(
            name="Unavailable files",
            value=(str().join([f"{item}\n" for item in files_not_found]) if len(files_not_found) else "None"),
            inline=False
        )
        for index, key in enumerate(all_progresses):
            value = str().join([all_progresses_str[index][1], f"\n{all_progresses[key].to_progress_str()}\n"])
            value += (f"**Provided by PR {ref.pr_no}**" if ref.pr_no and key in ref.pr_files else "**Provided by Master**")
            embed.add_field(
                name=key,
                value=value,
                inline=False
            )

        view = discord.ui.View()
        button = discord.ui.Button(style=discord.ButtonStyle.primary, label="More Details")
        await interaction.followup.send(content=None, embed=embed, view=MoreDetailsButtonView(all_progresses, files_not_found))
