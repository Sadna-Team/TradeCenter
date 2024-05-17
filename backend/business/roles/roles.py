from abc import ABC, abstractmethod
from typing import Dict, List, Optional


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
    def __init__(self, user_id: int):
        self.__user_id = user_id


class SystemManager(SystemRole):
    def __init__(self, user_id: int):
        super().__init__(user_id)


class StoreRole(ABC):
    @abstractmethod
    def __init__(self, user_id: int):
        self.__user_id = user_id

    @property
    def user_id(self) -> int:
        return self.__user_id


class StoreOwner(StoreRole):
    def __init__(self, user_id: int):
        super().__init__(user_id)


class StoreManager(StoreRole):
    def __init__(self, user_id: int):
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
            # self.__systems_nominations: Dict[int, List[]]

    def add_system_manger(self, user_id: int) -> None:
        system_manager = SystemManager(user_id)
        self.__system_roles.append(system_manager)

    def add_store(self, store_id: int, owner_id: int) -> None:
        owner = StoreOwner(owner_id)
        root = Node(owner)
        tree = Tree(root)
        self.__stores_to_roles[store_id] = tree

    def add_store_manager(self, store_id: int, manager_id: int, appointer_id: int) -> None:
        self.__validate_store_id(store_id)

        appointer = self.__stores_to_roles[store_id].find(appointer_id)
        if appointer is None:
            raise ValueError("Appointer does not exist")

        if isinstance(appointer, StoreManager) and not appointer.permissions.add_role:
            raise ValueError("Appointer does not have permissions to add a role")

        if not self.__stores_to_roles[store_id].find(manager_id) is None:
            raise ValueError("Manager already exists in store")

        manager = StoreManager(manager_id)
        self.__stores_to_roles[store_id].add_role(manager, appointer_id)

    def add_store_owner(self, store_id: int, owner_id: int, appointer_id: int) -> None:
        self.__validate_store_id(store_id)

        appointer = self.__stores_to_roles[store_id].find(appointer_id)
        if appointer is None:
            raise ValueError("Appointer does not exist")

        if not isinstance(appointer, StoreOwner):
            raise ValueError("Appointer does not have permissions to add a role")

        if not self.__stores_to_roles[store_id].find(owner_id) is None:
            raise ValueError("Owner already exists in store")

        owner = StoreOwner(owner_id)
        self.__stores_to_roles[store_id].add_role(owner, appointer_id)

    def remove_store_role(self, store_id: int, role_id: int, remover_id: int) -> None:
        self.__validate_store_id(store_id)

        remover = self.__stores_to_roles[store_id].find(remover_id)
        if remover is None:
            raise ValueError("Remover does not exist")

        role = self.__stores_to_roles[store_id].find(role_id)
        if role is None:
            raise ValueError("Role does not exist")

        if role_id != remover_id and self.__stores_to_roles[store_id].is_child(remover_id, role_id):
            raise ValueError("Remover didnt appoint the role")

        self.__stores_to_roles[store_id].remove_role(role_id)

    def close_store(self, store_id: int) -> None:
        self.__validate_store_id(store_id)
        del self.__stores_to_roles[store_id]

    # TODO: add permission changing methods

    def is_store_owner(self, store_id: int, user_id: int) -> bool:
        self.__validate_store_id(store_id)
        role = self.__stores_to_roles[store_id].find(user_id)
        return (role is not None
                and isinstance(role, StoreOwner))

    def is_store_manager(self, store_id: int, user_id: int) -> bool:
        self.__validate_store_id(store_id)
        role = self.__stores_to_roles[store_id].find(user_id)
        return (role is not None
                and isinstance(role, StoreManager))

    def __validate_store_id(self, store_id: int) -> None:
        if not self.__store_exists(store_id):
            raise ValueError("Store does not exist")

    def __store_exists(self, store_id: int) -> bool:
        return store_id in self.__stores_to_roles
