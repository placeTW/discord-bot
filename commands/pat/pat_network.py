from ..modules.supabase import supabaseClient
import networkx as nx
import discord
from discord import app_commands
from bot import TWPlaceClient
from discord.app_commands import Choice
import matplotlib.pyplot as plt
import tempfile
from os import chmod


def get_pat_statistics(
    pat_type: str, user_id: int,  limit: int = 5
) -> list[dict]:
    if pat_type not in ["patted", "patter"]:
        raise ValueError("pat_type must be either 'patted' or 'patter'")
        
    # data, c = supabaseClient.table(f'total_{pat_type}_counts').select("*").limit(10).execute()
    query = supabaseClient.table(f"pat_graph").select("*")
    query = query.eq(pat_type, user_id)
    query = query.limit(limit)
    data, c = query.execute()
    return data[1]

def get_and_draw_networkx_graph(pat_list: list[dict], usernames: dict = None):
    # an element in pat_list looks like this:
    ## {'patter': int, 'patted': int, 'pat_count': int}
    G = nx.DiGraph()
    for pat in pat_list:
        G.add_edge(pat["patter"], pat["patted"], weight=pat["pat_count"])
    # draw graph
    fig, ax = plt.subplots(figsize=(10, 10))
    pos = nx.planar_layout(G)
    # draw nodes
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=0)
    # draw node labels by getting the username of the node id from discord
    if usernames is not None:
        labels = {node: usernames[node] for node in G.nodes}
    else: # use the node id as the label
        labels = {node: node for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, ax=ax)

    # draw edges
    nx.draw_networkx_edges(G, pos, ax=ax, arrowsize=20)

    # draw edge labels
    edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, ax=ax)

    # set title
    ax.set_title("Pat Network: Patter -> Patted")

    return G, fig, ax

async def fetch_usernames(result: list[dict], client: TWPlaceClient) -> dict:
    usernames = {}
    for pat in result:
        for pat_type in ['patter', 'patted']:
            if pat[pat_type] not in usernames:
                user = await client.fetch_user(pat[pat_type])
                usernames[pat[pat_type]] = user.name
    return usernames


def register_commands(tree, client: TWPlaceClient, guilds: list[discord.Object]):
    pat_network_stats = app_commands.Group(name="pat_network",description="Pat network visualisation")

    # # pat direction has two possible choices: patted or patter, so create those choices
    # pat_direction_choices = [
    #     Choice(name="Patted", value="patted"),
    #     Choice(name="Patter", value="patter"),
    # ]

    @pat_network_stats.command(name='patted', description="See who has patted you")
    @app_commands.describe(user='The user to get the pat network for, default is you')
    async def patted_stats(interaction: discord.Interaction, user: discord.Member=None):
        # if user is None, then the user is the one who called the command
        if user is None:
            user = interaction.user
        user_id = user.id or interaction.user.id
        # * get pat statistics (looks like this: [{'patter': int, 'patted': int, 'pat_count': int}, ...])
        result = get_pat_statistics('patted', user_id)
        if result is None:
            await interaction.response.send_message(
                f"There was an error getting the pat network. Please try again",
                ephemeral=True,
            )
            return

        ## * for each patter and patted, get the user name from discord
        usernames = await fetch_usernames(result, client)
        # * get and draw networkx graph
        G, fig, ax = get_and_draw_networkx_graph(result, usernames)
        # * send the graph
        # create a temporary file to save the graph to
        with tempfile.NamedTemporaryFile(suffix=".png", delete_on_close=False, dir=".") as temp_file:
            # # set the permissions of the file to be readable and writable by everyone
            # chmod(temp_file.name, 0o666)
            fig.savefig(temp_file.name)
            await interaction.response.send_message(content=f"Showing the top 5 people who have patted {user.name}", file=discord.File(temp_file.name))


        # await interaction.response.send_message(content=f"results: {result}")

    tree.add_command(pat_network_stats, guilds=guilds)

if __name__ == "__main__":
    patters = get_pat_statistics("patter", "211981146941030401")
    get_networkx_graph(patters)
    print(patters)
