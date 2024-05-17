from abc import ABC, abstractmethod


class Permissions:
    def __init__(self):
        self.__add_item: bool = False


class SystemRole(ABC):
    @abstractmethod
    def __init__(self):
        pass
class SystemManager(SystemRole):
    def __init__(self):
        pass

class StoreRole(ABC):
    @abstractmethod
    def __init__(self):
        pass

class StoreOwner(StoreRole):
    def __init__(self):
        pass

class StoreManager(StoreRole):
    def __init__(self):
        permissions: Permissions = Permissions()


class RolesFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if RolesFacade.__instance is None:
            RolesFacade.__instance = object.__new__(cls)
        return RolesFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.__
