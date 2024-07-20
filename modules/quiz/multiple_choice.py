import discord

def create_multiple_choice_embed(correct_choices: list, wrong_chocies: list) -> discord.Embed:
    """
    Create a multiple choice embed.
    
    Parameters:
    - correct_choices: list of correct choices
    - wrong_choices: list of wrong choices
    """
    embed = discord.Embed(
        title="Multiple Choice",
        description="Choose the correct answer",
        color=discord.Color.green()
    )
    for i, choice in enumerate(correct_choices):
        embed.add_field(name=f"Choice {i+1}", value=choice, inline=False)
    for i, choice in enumerate(wrong_chocies):
        embed.add_field(name=f"Choice {i+1+len(correct_choices)}", value=choice, inline=False)
    return embed