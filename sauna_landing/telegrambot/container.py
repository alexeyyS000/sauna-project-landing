from dependency_injector import containers, providers
from telegram.ext import Updater
from telegram import Bot
from redis import Redis
from  telegrambot.utils.persistance import RedisPersistence

class WorkerContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    bot = providers.Singleton(
        Bot,
        token=config.telegrambot_key
    )


class BotContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    redis = providers.Singleton(
        Redis,
        host="localhost",
        port=6379,
        db=0,
        password=None
    )


    persistence = providers.Singleton(
        RedisPersistence,
        redis=redis
    )


    updater = providers.Singleton(
        Updater,
        token=config.telegrambot_key,
        use_context=True,
        persistence=persistence
    )