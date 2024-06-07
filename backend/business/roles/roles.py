from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from threading import Lock
from backend.business.notifier.notifier import Notifier

import logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                     format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Roles Logger")

class Permissions:
    def __init__(self):
        self.__add_product: bool = False
        self.__change_purchase_policy: bool = False
        self.__change_purchase_types: bool = False
        self.__change_discount_policy: bool = False
        self.__change_discount_types: bool = False
        self.__add_manager: bool = False
        self.__get_bid: bool = False

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

    @property
    def get_bid(self) -> bool:
        return self.__get_bid

    def set_permissions(self, add_product: bool, change_purchase_policy: bool, change_purchase_types: bool,
                        change_discount_policy: bool, change_discount_types: bool, add_manager: bool,
                        get_bid: bool) -> None:
        self.__add_product = add_product
        self.__change_purchase_policy = change_purchase_policy
        self.__change_purchase_types = change_purchase_types
        self.__change_discount_policy = change_discount_policy
        self.__change_discount_types = change_discount_types
        self.__add_manager = add_manager
        self.__get_bid = get_bid


class StoreRole(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


class StoreOwner(StoreRole):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "StoreOwner"


class StoreManager(StoreRole):
    def __init__(self):
        self.__permissions: Permissions = Permissions()

    @property
    def permissions(self) -> Permissions:
        return self.__permissions

    def __str__(self):
        return "StoreManager"


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
            self.__stores_to_role_tree: Dict[int, Tree] = {}  # Dict[store_id, Tree[user_id]]
            self.__stores_to_roles: Dict[int, Dict[int, StoreRole]] = {}  # Dict[store_id, Dict[user_id, StoreRole]]
            self.__systems_nominations: Dict[int, Nomination] = {}
            self.__system_managers: List[int] = []
            self.__system_admin: int = -1
            Nomination._Nomination__nomination_id_serializer = 0

            self.__creation_lock = Lock()
            self.__stores_locks: Dict[int, Lock] = {}  # Dict[store_id, Lock]
            self.__system_managers_lock = Lock()

    def clean_data(self):
        """
        For testing purposes only
        """
        self.__stores_to_role_tree.clear()
        self.__stores_to_roles.clear()
        self.__systems_nominations.clear()
        self.__system_managers.clear()
        self.__system_admin = -1
        Nomination._Nomination__nomination_id_serializer = 0

    def add_store(self, store_id: int, owner_id: int) -> None:
        """
        Add the first owner to the store roles (the store is already created)
        Called in the market facade
        """
        if store_id in self.__stores_to_roles:
            raise ValueError("Store already exists")
        self.__stores_to_roles[store_id] = {owner_id: StoreOwner()}
        self.__stores_to_role_tree[store_id] = Tree(Node(owner_id))
        self.__stores_locks[store_id] = Lock()

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

    def nominate_owner(self, store_id: int, nominator_id: int, nominee_id: int) -> int:
        with self.__stores_locks[store_id]:
            self.__check_nomination_validation(store_id, nominator_id, nominee_id)
            # check that nominator is an owner
            if not isinstance(self.__stores_to_roles[store_id][nominator_id], StoreOwner):
                raise ValueError("Nominator is not an owner")
            nomination = Nomination(store_id, nominator_id, nominee_id, StoreOwner())
            self.__systems_nominations[nomination.nomination_id] = nomination
            return nomination.nomination_id

    def nominate_manager(self, store_id: int, nominator_id: int, nominee_id: int) -> int:
        with self.__stores_locks[store_id]:
            self.__check_nomination_validation(store_id, nominator_id, nominee_id)
            # check that nominator is an owner or that he is a manager with permissions to add a manager
            if not self.__authorized_to_add_manager(store_id, nominator_id):
                raise ValueError("Nominator is not authorized to nominate a manager")
            nomination = Nomination(store_id, nominator_id, nominee_id, StoreManager())
            self.__systems_nominations[nomination.nomination_id] = nomination
            return nomination.nomination_id

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
        if nomination_id not in self.__systems_nominations.keys():
            raise ValueError(f"Nomination does not exist - given id - {nomination_id}, {type(nomination_id)}")
        nomination = self.__systems_nominations[nomination_id]
        if nominee_id != nomination.nominee_id:
            raise ValueError("Nominee id does not match the nomination")
        self.__stores_to_roles[nomination.store_id][nominee_id] = nomination.role
        self.__stores_to_role_tree[nomination.store_id].add_child_to_father(nomination.nominator_id, nominee_id)
        # add role to the store
        self.__stores_to_roles[nomination.store_id][nominee_id] = nomination.role

        Notifier().sign_listener(nominee_id, nomination.store_id)

        # delete all nominations of the nominee in the store
        for n_id, nomination in self.__systems_nominations.copy().items():
            if nomination.nominee_id == nominee_id and nomination.store_id == nomination.store_id:
                del self.__systems_nominations[n_id]
        logger.info(f"User {nominee_id} accepted the nomination {nomination_id} in store {nomination.store_id}")


    def decline_nomination(self, nomination_id: int, nominee_id) -> None:
        if nomination_id not in self.__systems_nominations:
            raise ValueError("Nomination does not exist")
        nomination = self.__systems_nominations[nomination_id]
        if nominee_id != nomination.nominee_id:
            raise ValueError("Nominee id does not match the nomination")
        del self.__systems_nominations[nomination_id]
        logger.info(f"User {nominee_id} declined the nomination {nomination_id} in store {nomination.store_id}")

    def set_manager_permissions(self, store_id: int, actor_id: int, manager_id: int, add_product: bool,
                                change_purchase_policy: bool, change_purchase_types: bool, change_discount_policy: bool,
                                change_discount_types: bool, add_manager: bool, get_bid: bool) -> None:
        '''
        Actor_id is the owner/manager of the store and tries to change the permissions of the manager_id '''

        with self.__stores_locks[store_id]:
            if store_id not in self.__stores_to_roles:
                raise ValueError("Store does not exist")
            if manager_id not in self.__stores_to_roles[store_id]:
                raise ValueError("Manager is not a member of the store")
            if not isinstance(self.__stores_to_roles[store_id][manager_id], StoreManager):
                raise ValueError("User is not a manager")
            if not self.__stores_to_role_tree[store_id].is_descendant(actor_id, manager_id):
                raise ValueError("Actor is not a owner/manager of the manager")
            (self.__stores_to_roles[store_id][manager_id].permissions
             .set_permissions(add_product, change_purchase_policy, change_purchase_types, change_discount_policy,
                              change_discount_types, add_manager, get_bid))

    def remove_role(self, store_id: int, actor_id: int, removed_id: int) -> None:
        with self.__stores_locks[store_id]:
            if store_id not in self.__stores_to_roles:
                raise ValueError("Store does not exist")
            if removed_id not in self.__stores_to_roles[store_id]:
                raise ValueError("Removed user is not a member of the store")
            if not self.__authorized_to_add_manager(store_id, actor_id):
                raise ValueError("Actor is not authorized to remove a role")
            if not actor_id != removed_id and not self.__stores_to_role_tree[store_id].is_descendant(actor_id,
                                                                                                     removed_id):
                raise ValueError("Actor is not an ancestor of the removed user")
            if self.__stores_to_role_tree[store_id].is_root(removed_id):
                raise ValueError("Cannot remove the root owner of the store")
            removed = self.__stores_to_role_tree[store_id].remove_node(removed_id)

            for user_id in removed:
                Notifier().unsign_listener(user_id, store_id)
                del self.__stores_to_roles[store_id][user_id]

    def get_employees_info(self, store_id: int, actor_id: int) -> Dict[int, str]:  # Dict[user_id, role]
        with self.__stores_locks[store_id]:
            if store_id not in self.__stores_to_roles:
                raise ValueError("Store does not exist")
            if actor_id not in self.__stores_to_roles[store_id]:
                raise ValueError("Actor is not a member of the store")
            employees = {}
            for user_id, role in self.__stores_to_roles[store_id].items():
                employees[user_id] = role.__str__()

            return employees

    def is_system_manager(self, user_id: int) -> bool:
        with self.__system_managers_lock:
            return user_id in self.__system_managers

    def add_system_manager(self, actor: int, user_id: int) -> None:
        """
        if Actor is a system manager, he adds a new system manager
        """
        with self.__system_managers_lock:
            if not self.is_system_manager(actor):
                raise ValueError("Actor is not a system manager")
            self.__system_managers.append(user_id)

    def remove_system_manager(self, actor: int, user_id: int) -> None:
        with self.__system_managers_lock:
            if user_id == self.__system_admin:
                raise ValueError("Cannot remove the system admin")
            if not self.is_system_manager(actor):
                raise ValueError("Actor is not a system manager")
            if user_id not in self.__system_managers:
                raise ValueError("User is not a system manager")
            self.__system_managers.remove(user_id)

    def add_admin(self, user_id: int) -> None:
        """
        this method should not be called (but the facade initialization)
        Add the first system manager to the system
        :return:
        """
        self.__system_managers.append(user_id)
        self.__system_admin = user_id

    def __has_permission(self, store_id: int, user_id: int) -> bool:
        if store_id not in self.__stores_to_roles:
            return False
        if user_id not in self.__stores_to_roles[store_id]:
            return False
        if isinstance(self.__stores_to_roles[store_id][user_id], StoreOwner):
            return True
        raise ValueError("User is a manager")

    def has_add_product_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except ValueError:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return self.__stores_to_roles[store_id][user_id].permissions.add_product
                return False

    def has_change_purchase_policy_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except ValueError:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return self.__stores_to_roles[store_id][user_id].permissions.change_purchase_policy
                return False

    def has_change_purchase_types_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except ValueError:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return self.__stores_to_roles[store_id][user_id].permissions.change_purchase_types
                return False

    def has_change_discount_policy_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except ValueError:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return self.__stores_to_roles[store_id][user_id].permissions.change_discount_policy
                return False

    def has_change_discount_types_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except ValueError:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return self.__stores_to_roles[store_id][user_id].permissions.change_discount_types
                return False

    def has_add_manager_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except ValueError:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return self.__stores_to_roles[store_id][user_id].permissions.add_manager
                return False

    def has_get_bid_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except ValueError:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return self.__stores_to_roles[store_id][user_id].permissions.get_bid
                return False

    def is_owner(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            if user_id in self.__stores_to_roles[store_id]:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreOwner):
                    return True
            return False

    def is_manager(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            if user_id in self.__stores_to_roles[store_id]:
                if isinstance(self.__stores_to_roles[store_id][user_id], StoreManager):
                    return True
            return False

    def get_store_owners(self, store_id: int) -> Dict[int, str]:  # Dict[user_id, role]
        with self.__stores_locks[store_id]:
            owners = {}
            for user_id, role in self.__stores_to_roles[store_id].items():
                owners[user_id] = role.__str__()
            return owners
