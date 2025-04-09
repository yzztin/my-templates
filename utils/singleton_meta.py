from threading import Lock


class BaseSingleton:
    """
    用法：
    class A(BaseSingleton):
        pass
    """

    _instances = {}
    _lock = Lock()  # 保证线程安全

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:  # 在多线程环境中确保实例创建的安全
                if cls not in cls._instances:  # 双重检查锁定
                    instance = super().__new__(cls)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class SingletonMeta(type):
    """
    用法：
    class A(metaclass=SingletonMeta):
        pass
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
