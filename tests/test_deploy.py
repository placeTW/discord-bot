import pytest
from main import BotInitialiser

@pytest.mark.deployment
def test_BotInitialiser(monkeypatch):
    # patch the register_commands command to do nothing
    def mock_register_commands(*args, **kwargs):
        pass
    monkeypatch.setattr(BotInitialiser, "register_commands", mock_register_commands)
    # patch the run command to do nothing (just in case)
    def mock_run(*args, **kwargs):
        pass
    monkeypatch.setattr(BotInitialiser, "run", mock_run)

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
