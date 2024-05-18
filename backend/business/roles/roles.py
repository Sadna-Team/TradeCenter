from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class Permissions:
    def __init__(self):
        self.__add_product: bool = False
        self.__change_purchase_policy: bool = False
        self.__change_purchase_types: bool = False
        self.__change_discount_policy: bool = False
        self.__change_discount_types: bool = False
        self.__add_manager: bool = False

    @property
    def add_product(self) -> bool:
        return self.__add_product

    @property
    def change_purchase_policy(self) -> bool:
        return self.__change_purchase_policy

    @property
    def change_purchase_types(self) -> bool:
        return self.__change_purchase_types

    @property
    def change_discount_policy(self) -> bool:
        return self.__change_discount_policy

    @property
    def change_discount_types(self) -> bool:
        return self.__change_discount_types

    @property
    def add_manager(self) -> bool:
        return self.__add_manager


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


class Nomination:
    __nomination_id_serializer = 0

    def __init__(self, store_id, nominator_id: int, nominee_id: int, role: StoreRole):
        self.__nomination_id = Nomination.__nomination_id_serializer
        Nomination.__nomination_id_serializer += 1
        self.__store_id: int = store_id
        self.__nominator_id: int = nominator_id
        self.__nominee_id: int = nominee_id
        self.__role: StoreRole = role

    @property
    def nomination_id(self) -> int:
        return self.__nomination_id

    @property
    def store_id(self) -> int:
        return self.__store_id

    @property
    def nominator_id(self) -> int:
        return self.__nominator_id

    @property
    def nominee_id(self) -> int:
        return self.__nominee_id

    @property
    def role(self) -> StoreRole:
        return self.__role


class Node:
    def __init__(self, data):
        self.__data: int = data
        self.children: List[Node] = []

    def add_child(self, child: int) -> None:
        self.children.append(Node(child))

    @property
    def data(self) -> int:
        return self.__data


class Tree:
    def __init__(self, root: Node) -> None:
        self.__root: Node = root

    def is_root(self, user_id: int) -> bool:
        return self.__root.data == user_id

    def add_child_to_father(self, father: int, child: int) -> None:
        self.__add_child_to_father_rec(self.__root, father, child)

    def __add_child_to_father_rec(self, node: Node, father: int, child: int) -> None:
        if node.data == father:
            node.add_child(child)
            return
        for child_node in node.children:
            self.__add_child_to_father_rec(child_node, father, child)

    def is_descendant(self, ancestor_id: int, descendant_id: int) -> bool:
        if ancestor_id == descendant_id:
            return False
        ancestor = self.__find_node(self.__root, ancestor_id)
        if ancestor is None:
            return False
        return self.__find_node(ancestor, descendant_id) is not None

    def __find_node(self, node: Node, data: int) -> Optional[Node]:
        if node.data == data:
            return node
        for child in node.children:
            found = self.__find_node(child, data)
            if found is not None:
                return found
        return None

    # remove all children of the node with the given user_id and return a list of the removed children
    def remove_node(self, user_id: int) -> List[int]:
        removed = []
        removed_node = self.__find_node(self.__root, user_id)
        self.__in_order(removed_node, removed)
        self.__trim_tree(self.__root, user_id)
        return removed

    def __in_order(self, node: Node, lst: List[int]) -> None:
        if node is None:
            return
        lst.append(node.data)
        for child in node.children:
            self.__in_order(child, lst)

    def __trim_tree(self, node: Node, data: int) -> None:
        if node is None:
            return
        for child in node.children:
            if child.data == data:
                node.children.remove(child)
                return
            else:
                self.__trim_tree(child, data)


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
            self.__stores_to_role_tree: Dict[int, Tree] = {}  # Dict[store_id, Tree[role_id]]
            self.__stores_to_roles: Dict[int, Dict[int, StoreRole]] = {}  # Dict[store_id, Dict[role_id, StoreRole]]
            self.__system_roles: Dict[int, SystemRole] = {}  # Dict[role_id, SystemRole]
            self.__systems_nominations: Dict[int, Nomination] = {}

    def add_store(self, store_id: int, owner_id: int) -> None:
        if store_id in self.__stores_to_roles:
            raise ValueError("Store already exists")
        self.__stores_to_roles[store_id] = {owner_id: StoreOwner()}
        self.__stores_to_role_tree[store_id] = Tree(Node(owner_id))

    def close_store(self, store_id: int, actor_id: int) -> None:
        if store_id not in self.__stores_to_roles:
            raise ValueError("Store does not exist")
        if actor_id not in self.__stores_to_roles[store_id]:
            raise ValueError("Actor is not a member of the store")
        if not self.__stores_to_role_tree[store_id].is_root(actor_id):
            raise ValueError("Actor is not the root owner of the store")
        del self.__stores_to_roles[store_id]
        del self.__stores_to_role_tree[store_id]
        # remove all nominations in closed store
        for nomination_id, nomination in self.__systems_nominations.items():
            if nomination.store_id == store_id:
                del self.__systems_nominations[nomination_id]

    def nominate_owner(self, store_id: int, nominator_id: int, nominee_id: int) -> None:
        self.__check_nomination_validation(store_id, nominator_id, nominee_id)
        # check that nominator is an owner
        if not isinstance(self.__stores_to_roles[store_id][nominator_id], StoreOwner):
            raise ValueError("Nominator is not an owner")
        nomination = Nomination(store_id, nominator_id, nominee_id, StoreOwner())
        self.__systems_nominations[nomination.nomination_id] = nomination

    def nominate_manager(self, store_id: int, nominator_id: int, nominee_id: int) -> None:
        self.__check_nomination_validation(store_id, nominator_id, nominee_id)
        # check that nominator is an owner or that he is a manager with permissions to add a manager
        if not self.__authorized_to_add_manager(store_id, nominator_id):
            raise ValueError("Nominator is not authorized to nominate a manager")
        nomination = Nomination(store_id, nominator_id, nominee_id, StoreManager())
        self.__systems_nominations[nomination.nomination_id] = nomination

    def __authorized_to_add_manager(self, store_id: int, nominator_id: int) -> bool:
        return isinstance(self.__stores_to_roles[store_id][nominator_id], StoreOwner) or \
               (isinstance(self.__stores_to_roles[store_id][nominator_id], StoreManager) and
                self.__stores_to_roles[store_id][nominator_id].permissions.add_manager)

    def __check_nomination_validation(self, store_id: int, nominator_id: int, nominee_id: int) -> None:
        if store_id not in self.__stores_to_roles:
            raise ValueError("Store does not exist")
        if nominator_id not in self.__stores_to_roles[store_id]:
            raise ValueError("Nominator is not a member of the store")
        if nominee_id in self.__stores_to_roles[store_id]:
            raise ValueError("Nominee is already a member of the store")

    def accept_nomination(self, nomination_id: int, nominee_id: int) -> None:
        if nomination_id not in self.__systems_nominations:
            raise ValueError("Nomination does not exist")
        nomination = self.__systems_nominations[nomination_id]
        if nominee_id != nomination.nominee_id:
            raise ValueError("Nominee id does not match the nomination")
        self.__stores_to_roles[nomination.store_id][nominee_id] = nomination.role
        self.__stores_to_role_tree[nomination.store_id].add_child_to_father(nomination.nominator_id, nominee_id)
        # add role to the store
        self.__stores_to_roles[nomination.store_id][nominee_id] = nomination.role
        # delete all nominations of the nominee in the store
        for n_id, nomination in self.__systems_nominations.items():
            if nomination.nominee_id == nominee_id and nomination.store_id == nomination.store_id:
                del self.__systems_nominations[n_id]

    def decline_nomination(self, nomination_id: int, nominee_id) -> None:
        if nomination_id not in self.__systems_nominations:
            raise ValueError("Nomination does not exist")
        nomination = self.__systems_nominations[nomination_id]
        if nominee_id != nomination.nominee_id:
            raise ValueError("Nominee id does not match the nomination")
        del self.__systems_nominations[nomination_id]

    def set_manager_permissions(self, store_id: int, actor_id: int, manager_id: int, permissions: Permissions) -> None:
        if store_id not in self.__stores_to_roles:
            raise ValueError("Store does not exist")
        if manager_id not in self.__stores_to_roles[store_id]:
            raise ValueError("Manager is not a member of the store")
        if not isinstance(self.__stores_to_roles[store_id][manager_id], StoreManager):
            raise ValueError("User is not a manager")
        if not self.__stores_to_role_tree[store_id].is_descendant(actor_id, manager_id):
            raise ValueError("Actor is not a owner/manager of the manager")
        self.__stores_to_roles[store_id][manager_id].permissions = permissions

    def remove_role(self, store_id: int, actor_id: int, removed_id: int) -> None:
        if store_id not in self.__stores_to_roles:
            raise ValueError("Store does not exist")
        if removed_id not in self.__stores_to_roles[store_id]:
            raise ValueError("Removed user is not a member of the store")
        if not self.__authorized_to_add_manager(store_id, actor_id):
            raise ValueError("Actor is not authorized to remove a role")
        if not actor_id != removed_id and not self.__stores_to_role_tree[store_id].is_descendant(actor_id, removed_id):
            raise ValueError("Actor is not an ancestor of the removed user")
        if self.__stores_to_role_tree[store_id].is_root(removed_id):
            raise ValueError("Cannot remove the root owner of the store")
        removed = self.__stores_to_role_tree[store_id].remove_node(removed_id)
        for user_id in removed:
            del self.__stores_to_roles[store_id][user_id]
