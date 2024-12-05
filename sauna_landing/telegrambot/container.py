from dependency_injector import containers, providers
from telegram.ext import Updater


class BotContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    updater = providers.Singleton(
        Updater,
        token=config.telegrambot_key,
        use_context=True
    )