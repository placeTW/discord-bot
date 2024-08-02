import pytest
import supabase

@pytest.mark.deployment
def test_BotInitialiser(monkeypatch):
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