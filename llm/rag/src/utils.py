def singleton(func):
    def wrapper(*args, **kwargs):
        if wrapper.instance:
            return wrapper.instance
        instance = func(*args, **kwargs)
        wrapper.instance = instance
        return instance
    wrapper.instance = None
    return wrapper
