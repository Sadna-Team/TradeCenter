from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class Permissions:
    def __init__(self):
        self.__add_item: bool = False
        self.__add_role: bool = False

    @property
    def add_item(self) -> bool:
        return self.__add_item

    @property
    def add_role(self) -> bool:
        return self.__add_role


class SystemRole(ABC):
    @abstractmethod
    def __init__(self):
        pass


class SystemManager(SystemRole):
    def __init__(self):
        super().__init__()


class StoreRole(ABC):
    @abstractmethod
    def __init__(self):
        pass


class StoreOwner(StoreRole):
    def __init__(self):
        super().__init__()


class StoreManager(StoreRole):
    def __init__(self):
        self.__permissions: Permissions = Permissions()

    @property
    def permissions(self) -> Permissions:
        return self.__permissions


class Node:
    def __init__(self, data):
        self.__data: StoreRole = data
        self.children: List[Node] = []

    def add_child(self, child: StoreRole) -> None:
        self.children.append(Node(child))

    @property
    def data(self) -> StoreRole:
        return self.__data


class Tree:
    def __init__(self, root: Node) -> None:
        self.__root: Node = root

    def find(self, role_id: int) -> Optional[StoreRole]:
        return self.__find(self.__root, role_id)

    def __find(self, node: Node, role_id: int) -> Optional[StoreRole]:
        if node.data.user_id == role_id:
            return node.data

        for child in node.children:
            found = self.__find(child, role_id)
            if found is not None:
                return found

        return None

    def add_role(self, store_role: StoreRole, appointer_id: int) -> None:
        self.__add_role(self.__root, store_role, appointer_id)

    def __add_role(self, node: Node, store_role: StoreRole, appointer_id: int) -> None:
        if node.data.user_id == appointer_id:
            node.add_child(store_role)
            return

        for child in node.children:
            self.__add_role(child, store_role, appointer_id)

        return

    def is_child(self, parent_id: int, child_id: int) -> bool:
        return self.__is_child(self.__root, parent_id, child_id)

    def __is_child(self, node: Node, parent_id: int, child_id: int) -> bool:
        if node.data.user_id == parent_id:
            for child in node.children:
                if child.data.user_id == child_id:
                    return True
            return False

        for child in node.children:
            if self.__is_child(child, parent_id, child_id):
                return True

        return False

    def remove_role(self, role_id: int):
        self.__remove_role(self.__root, role_id)

    def __remove_role(self, node: Node, role_id: int):
        for child in node.children:
            if child.data.user_id == role_id:
                node.children.remove(child)
                return

            self.__remove_role(child, role_id)
        return


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
            self.__stores_to_roles: Dict[int, Tree] = {}
            self.__system_roles: List[SystemRole] = []
            # TODO: add system nominations
            self.__systems_nominations: Dict[int, List[Tuple[int, StoreRole]]] = {}  # Dict[sore_id, List[Tuple[appointer_id, StoreRole]]]
