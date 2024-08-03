import pytest
import supabase
import github

@pytest.mark.deployment
def test_BotInitialiser(monkeypatch):
    # | Note: the order of the imports is important since some modules depend on others being patched first

    # * PATCH ENVIRONMENT VARIABLES
    monkeypatch.setenv("PLACETW_SERVER_ID", "999") # set the environment variable for the placetw server id

    # * PATCH SUPABASE MODULE
    # patch the create_client command to do nothing
    def mock_create_client(url: str, private_key: str):
        return None
    monkeypatch.setattr(supabase, "create_client", mock_create_client)
    assert supabase.create_client("url", "private_key") is None # test the mock

    # patch the modules.config module, which uses supabaseClient
    import modules.config
    # patch the module.config.fetch_config to return a dict instead of fetching from supabase
    def mock_fetch_config(*args, **kwargs):
        return {0: {"key": "value"}}
    monkeypatch.setattr(modules.config, "fetch_config", mock_fetch_config)
    # patch the module.config.set_config to do nothing instead of setting the config in supabase
    def mock_set_config(*args, **kwargs):
        pass
    monkeypatch.setattr(modules.config, "set_config", mock_set_config)

    # * PATCH GITHUB MODULE
    # patch the github.Auth.Token to return a dummy object
    class DummyAuth:
        def __init__(self, *args, **kwargs): pass
    monkeypatch.setattr(github.Auth, "Token", DummyAuth)
    assert github.Auth.Token("token") is not None

    # patch the github.Github module so that it returns a dummy object with get_repo() method that does nothing
    class DummyGithub:
        def __init__(self, *args, **kwargs): pass
        @staticmethod
        def get_repo(repo_name):
            return None
    monkeypatch.setattr(github, "Github", DummyGithub)
    assert github.Github("token").get_repo("repo_name") is None

    # * PATCH BOT_GIT_UTILS MODULE
    from commands.restart import bot_git_utils
    # patch bot_git_utils.list_of_branches to return ['main']
    def mock_list_of_branches():
        return ['main']
    monkeypatch.setattr(bot_git_utils, "list_of_branches", mock_list_of_branches)
    assert bot_git_utils.list_of_branches() == ['main']

    # * PATCH RESTART MODULE
    from main import BotInitialiser # ! only import after patching, because it uses the modules.config module
    # create a BotInitialiser object
    bot = BotInitialiser()
    # assert that the BotInitialiser object is created
    assert isinstance(bot, BotInitialiser)
    # assert that self.client, self.guilds, self.tree are created
    assert hasattr(bot, "client")
    assert hasattr(bot, "guilds")
    assert hasattr(bot, "tree")
    # assert that self.placetw_guild is created
    assert hasattr(bot, "placetw_guild")