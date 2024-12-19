def is_active_tg_alerting(func):
    def wrapper(*args, **kwargs):
        user = args[1].user_data['user']
        if not user.is_active_tg_alerting:
            return
        else:
            return func(*args, **kwargs)
    return wrapper