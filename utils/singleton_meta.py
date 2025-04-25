class SingletonMeta(type):
    """
    用法：
    class A(metaclass=SingletonMeta):
        pass
    """

    _instances = None

    def __call__(cls, *args, **kwargs):
        if cls._instances is None:
            instance = super().__call__(*args, **kwargs)
            cls._instances = instance
        return cls._instances