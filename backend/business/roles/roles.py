from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from threading import Lock
from backend.business.notifier.notifier import Notifier
from backend.error_types import *
from backend.business.DTOs import RoleNominationDTO, UserDTO
from backend.database import db
from sqlalchemy.orm import backref, relationship
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                     format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Roles Logger")


class Permissions(db.Model):

    __tablename__ = 'permissions'

    id = db.Column(db.String(100), primary_key=True) # user_id_store_id
    add_product = db.Column(db.Boolean, nullable=False)
    change_purchase_policy = db.Column(db.Boolean, nullable=False)
    change_purchase_types = db.Column(db.Boolean, nullable=False)
    change_discount_policy = db.Column(db.Boolean, nullable=False)
    change_discount_types = db.Column(db.Boolean, nullable=False)
    add_manager = db.Column(db.Boolean, nullable=False)
    get_bid = db.Column(db.Boolean, nullable=False)

    def __init__(self):
        self.__id = None
        self.__add_product: bool = False
        self.__change_purchase_policy: bool = False
        self.__change_purchase_types: bool = False
        self.__change_discount_policy: bool = False
        self.__change_discount_types: bool = False
        self.__add_manager: bool = False
        self.__get_bid: bool = False

    @property
    def id(self) -> str:
        return self.__id

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

    def set_permissions(self, id: str, add_product: bool, change_purchase_policy: bool, change_purchase_types: bool,
                        change_discount_policy: bool, change_discount_types: bool, add_manager: bool,
                        get_bid: bool) -> None:
        self.__id = id
        self.__add_product = add_product
        self.__change_purchase_policy = change_purchase_policy
        self.__change_purchase_types = change_purchase_types
        self.__change_discount_policy = change_discount_policy
        self.__change_discount_types = change_discount_types
        self.__add_manager = add_manager
        self.__get_bid = get_bid


class StoreRole(db.Model, ABC):
    __tablename__ = 'store_roles'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    store_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'store_role'
    }

    @abstractmethod
    def __init__(self, store_id, user_id):
        self.store_id = store_id
        self.user_id = user_id

    def __str__(self):
        return self.__class__.__name__


class StoreOwner(StoreRole):
    __tablename__ = 'store_owners'

    id = db.Column(db.Integer, db.ForeignKey('store_roles.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'store_owner',
    }

    def __init__(self, store_id, user_id):
        super().__init__(store_id, user_id)

    def __str__(self):
        return "StoreOwner"


class StoreManager(StoreRole):
    __tablename__ = 'store_managers'

    id = db.Column(db.Integer, db.ForeignKey('store_roles.id'), primary_key=True)
    permissions_id = db.Column(db.Integer, db.ForeignKey('permissions.id'))
    permissions = db.relationship('Permissions', backref=backref('manager', uselist=False))

    __mapper_args__ = {
        'polymorphic_identity': 'store_manager',
    }

    def __init__(self, store_id, user_id):
        super().__init__(store_id, user_id)
        self.permissions = Permissions()

    @property
    def permissions(self) -> Permissions:
        return self.permissions

    def __str__(self):
        return "StoreManager"


class Nomination(db.Model):
    __tablename__ = 'nominations'
    __nomination_id_serializer = 0

    nomination_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, nullable=False)
    nominator_id = db.Column(db.Integer, nullable=False)
    nominee_id = db.Column(db.Integer, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('store_roles.id'))
    role = db.relationship('StoreRole')

    def __init__(self, store_id, nominator_id: int, nominee_id: int, role: StoreRole):
        self.nomination_id = Nomination.__nomination_id_serializer
        Nomination.__nomination_id_serializer += 1
        self.store_id = store_id
        self.nominator_id = nominator_id
        self.nominee_id = nominee_id
        self.role = role

    @property
    def nomination_id(self) -> int:
        return self.nomination_id

    @property
    def store_id(self) -> int:
        return self.store_id

    @property
    def nominator_id(self) -> int:
        return self.nominator_id

    @property
    def nominee_id(self) -> int:
        return self.nominee_id

    @property
    def role(self) -> StoreRole:
        return self.role

class TreeNode(db.Model):
    __tablename__ = 'tree_nodes'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Integer, nullable=False)
    store_tree_id = db.Column(db.Integer, db.ForeignKey('store_trees.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('tree_nodes.id'))
    children = relationship("TreeNode",
                            backref=backref('parent', remote_side=[id]),
                            cascade="all, delete-orphan")

    def __init__(self, data: int, store_tree_id: int, parent_id: Optional[int] = None):
        self.data = data
        self.store_tree_id = store_tree_id
        self.parent_id = parent_id


class StoreTree(db.Model):
    __tablename__ = 'store_trees'

    id = db.Column(db.Integer, primary_key=True)
    root_id = db.Column(db.Integer, db.ForeignKey('tree_nodes.id'))
    root = relationship("TreeNode", uselist=False, foreign_keys=[root_id])

    def __init__(self, root: TreeNode):
        self.root = root


class Node:
    def __init__(self, data, store_tree_id=None, parent_id=None):
        self.__data: int = data
        self.children: List[Node] = []
        self.store_tree_id = store_tree_id
        self.parent_id = parent_id

    def add_child(self, child: int) -> None:
        self.children.append(Node(child, self.store_tree_id, self.__data))

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
            return True
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

    @staticmethod
    def from_db(store_tree_id: int) -> 'Tree':
        root_node = db.session.query(TreeNode).filter_by(store_tree_id=store_tree_id, parent_id=None).one()
        root = Node(root_node.data, root_node.store_tree_id, root_node.parent_id)
        tree = Tree(root)
        Tree.__load_children(root)
        return tree

    @staticmethod
    def __load_children(node: Node) -> None:
        child_nodes = db.session.query(TreeNode).filter_by(parent_id=node.data).all()
        for child_node in child_nodes:
            child = Node(child_node.data, child_node.store_tree_id, child_node.parent_id)
            node.add_child(child.data)
            Tree.__load_children(child)


class SystemManagerModel(db.Model):
    __tablename__ = 'system_managers'

    user_id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, nullable=False)


class RolesFacade:
    __instance = None

    def __new__(cls):
        if RolesFacade.__instance is None:
            RolesFacade.__instance = object.__new__(cls)
        return RolesFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.__stores_to_role_tree: Dict[int, Tree] = self.__load_trees_from_db()
            self.__stores_to_roles: Dict[int, Dict[int, StoreRole]] = self.__load_roles_from_db()
            self.__systems_nominations: Dict[int, Nomination] = self.__load_nominations_from_db()
            self.__system_managers: List[int] = self.__load_system_managers_from_db()
            self.__system_admin: int = self.__load_system_admin_from_db()
            self.__notifier = Notifier()

            Nomination.__nomination_id_serializer = Nomination.get_max_nomination_id() + 1

            self.__creation_lock = Lock()
            self.__stores_locks: Dict[int, Lock] = {store_id: Lock() for store_id in self.__stores_to_role_tree.keys()}
            self.__system_managers_lock = Lock()

    def __load_trees_from_db(self) -> Dict[int, Tree]:
        trees = {}
        store_trees = db.session.query(StoreTree).all()
        for store_tree in store_trees:
            trees[store_tree.id] = Tree.from_db(store_tree.id)
        return trees

    def __load_roles_from_db(self) -> Dict[int, Dict[int, StoreRole]]:
        roles = {}
        store_roles = db.session.query(StoreRole).all()
        for store_role in store_roles:
            store_id = store_role.store_id
            if store_id not in roles:
                roles[store_id] = {}
            if store_role.role_type == 'store_owner':
                roles[store_id][store_role.user_id] = StoreOwner()
            elif store_role.role_type == 'store_manager':
                manager = StoreManager()
                permissions = store_role.permissions
                manager.permissions.set_permissions(
                    add_product=permissions.add_product,
                    change_purchase_policy=permissions.change_purchase_policy,
                    change_purchase_types=permissions.change_purchase_types,
                    change_discount_policy=permissions.change_discount_policy,
                    change_discount_types=permissions.change_discount_types,
                    add_manager=permissions.add_manager,
                    get_bid=permissions.get_bid
                )
                roles[store_id][store_role.user_id] = manager
        return roles

    def __load_nominations_from_db(self) -> Dict[int, Nomination]:
        nominations = {}
        db_nominations = db.session.query(Nomination).all()
        for db_nomination in db_nominations:
            nomination = Nomination(
                store_id=db_nomination.store_id,
                nominator_id=db_nomination.nominator_id,
                nominee_id=db_nomination.nominee_id,
                role=StoreOwner() if db_nomination.role_type == 'store_owner' else StoreManager()
            )
            nominations[db_nomination.id] = nomination
        return nominations

    def __load_system_managers_from_db(self) -> List[int]:
        managers = db.session.query(SystemManagerModel).all()
        return [manager.user_id for manager in managers]

    def __load_system_admin_from_db(self) -> int:
        admin = db.session.query(SystemManagerModel).filter_by(is_admin=True).one_or_none()
        if admin is None:
            return -1
        return admin.user_id

    def clean_data(self):
        self.__stores_to_role_tree.clear()
        self.__stores_to_roles.clear()
        self.__systems_nominations.clear()
        self.__system_managers.clear()
        self.__system_admin = -1
        Nomination.__nomination_id_serializer = 0
        self.__notifier.clean_data()
        db.session.query(TreeNode).delete()
        db.session.query(StoreTree).delete()
        db.session.query(StoreRole).delete()
        db.session.query(Nomination).delete()
        db.session.query(SystemManagerModel).delete()
        db.session.commit()

    def add_store(self, store_id: int, owner_id: int) -> None:
        """
        Add the first owner to the store roles (the store is already created)
        Called in the market facade
        """
        if store_id in self.__stores_to_roles:
            raise RoleError("Store already exists", RoleErrorTypes.store_already_exists)

        # Create root node and store tree
        root_node = TreeNode(data=owner_id, store_tree_id=store_id)
        store_tree = StoreTree(root=root_node)

        # Save to database
        db.session.add(store_tree)
        db.session.commit()

        self.__stores_to_roles[store_id] = {owner_id: StoreOwner()}
        self.__stores_to_role_tree[store_id] = Tree(Node(owner_id, store_tree_id=store_tree.id))
        self.__stores_locks[store_id] = Lock()
        self.__notifier.sign_listener(owner_id, store_id)

    def remove_store(self, store_id: int, actor_id: int) -> None:
        if store_id not in self.__stores_to_roles:
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        if actor_id not in self.__stores_to_roles[store_id]:
            raise RoleError('Actor is not a member of the store', RoleErrorTypes.user_not_member_of_store)
        if not self.__stores_to_role_tree[store_id].is_root(actor_id):
            raise RoleError('Actor is not the root owner of the store', RoleErrorTypes.actor_not_founder)

        # Remove from database
        db.session.query(TreeNode).filter(TreeNode.store_tree_id == store_id).delete()
        db.session.query(StoreTree).filter(StoreTree.id == store_id).delete()
        db.session.commit()

        del self.__stores_to_roles[store_id]
        del self.__stores_to_role_tree[store_id]

        for nomination_id, nomination in self.__systems_nominations.copy().items():
            if nomination.store_id == store_id:
                del self.__systems_nominations[nomination_id]

    def nominate_owner(self, store_id: int, nominator_id: int, nominee_id: int) -> int:
        with self.__stores_locks[store_id]:
            self.__check_nomination_validation(store_id, nominator_id, nominee_id)
            if not isinstance(self.__stores_to_roles[store_id][nominator_id], StoreOwner):
                raise RoleError("Nominator is not an owner", RoleErrorTypes.nominator_not_owner)

            nomination = Nomination(store_id, nominator_id, nominee_id, StoreOwner())
            self.__systems_nominations[nomination.nomination_id] = nomination

            # Save to database
            db.session.add(nomination)
            db.session.commit()

            return nomination.nomination_id

    def nominate_manager(self, store_id: int, nominator_id: int, nominee_id: int) -> int:
        with self.__stores_locks[store_id]:
            self.__check_nomination_validation(store_id, nominator_id, nominee_id)
            if not self.__authorized_to_add_manager(store_id, nominator_id):
                raise RoleError("Nominator is not authorized to nominate a manager",
                                RoleErrorTypes.nominator_cant_nominate_manager)

            nomination = Nomination(store_id, nominator_id, nominee_id, StoreManager())
            self.__systems_nominations[nomination.nomination_id] = nomination

            # Save to database
            db.session.add(nomination)
            db.session.commit()

            return nomination.nomination_id

    def __authorized_to_add_manager(self, store_id: int, nominator_id: int) -> bool:
        return isinstance(self.__stores_to_roles[store_id][nominator_id], StoreOwner) or \
            (isinstance(self.__stores_to_roles[store_id][nominator_id], StoreManager) and
             self.__stores_to_roles[store_id][nominator_id].permissions.add_manager)

    def __check_nomination_validation(self, store_id: int, nominator_id: int, nominee_id: int) -> None:
        if store_id not in self.__stores_to_roles:
            raise StoreError("Store does not exist",StoreErrorTypes.store_not_found)
        if nominator_id not in self.__stores_to_roles[store_id]:
            raise RoleError("Nominator is not a member of the store",RoleErrorTypes.nominator_not_member_of_store)
        if nominee_id in self.__stores_to_roles[store_id]:
            raise RoleError("Nominee is already a member of the store",RoleErrorTypes.nominee_already_exists_in_store)

    def accept_nomination(self, nomination_id: int, nominee_id: int) -> None:
        if nomination_id not in self.__systems_nominations.keys():
            raise RoleError(f"Nomination does not exist - given id - {nomination_id}, {type(nomination_id)}",
                            RoleErrorTypes.nomination_does_not_exist)
        nomination = self.__systems_nominations[nomination_id]
        if nominee_id != nomination.nominee_id:
            raise RoleError("Nominee id does not match the nomination", RoleErrorTypes.nominee_id_error)

        self.__stores_to_roles[nomination.store_id][nominee_id] = nomination.role
        self.__stores_to_role_tree[nomination.store_id].add_child_to_father(nomination.nominator_id, nominee_id)
        self.__notifier.sign_listener(nominee_id, nomination.store_id)

        # Save to database
        store_role_model = StoreRole(
            store_id=nomination.store_id,
            user_id=nominee_id,
            role_type='store_owner' if isinstance(nomination.role, StoreOwner) else 'store_manager'
        )
        db.session.add(store_role_model)
        db.session.commit()

        # Delete all nominations of the nominee in the store
        for n_id, nomination in self.__systems_nominations.copy().items():
            if nomination.nominee_id == nominee_id and nomination.store_id == nomination.store_id:
                del self.__systems_nominations[n_id]
                db.session.query(Nomination).filter_by(id=n_id).delete()
        db.session.commit()
        logger.info(f"User {nominee_id} accepted the nomination {nomination_id} in store {nomination.store_id}")

    def decline_nomination(self, nomination_id: int, nominee_id) -> None:
        if nomination_id not in self.__systems_nominations:
            raise RoleError("Nomination does not exist", RoleErrorTypes.nomination_does_not_exist)
        nomination = self.__systems_nominations[nomination_id]
        if nominee_id != nomination.nominee_id:
            raise RoleError("Nominee id does not match the nomination", RoleErrorTypes.nominee_id_error)

        del self.__systems_nominations[nomination_id]

        # Remove from database
        db.session.query(Nomination).filter_by(id=nomination_id).delete()
        db.session.commit()

        logger.info(f"User {nominee_id} declined the nomination {nomination_id} in store {nomination.store_id}")

    def set_manager_permissions(self, store_id: int, actor_id: int, manager_id: int, add_product: bool,
                                change_purchase_policy: bool, change_purchase_types: bool, change_discount_policy: bool,
                                change_discount_types: bool, add_manager: bool, get_bid: bool) -> None:
        with self.__stores_locks[store_id]:
            if store_id not in self.__stores_to_roles:
                raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
            if manager_id not in self.__stores_to_roles[store_id]:
                raise RoleError("Manager is not a member of the store", RoleErrorTypes.manager_not_member_of_store)
            if not isinstance(self.__stores_to_roles[store_id][manager_id], StoreManager):
                raise RoleError("User is not a manager", RoleErrorTypes.user_not_manager)
            if not self.__stores_to_role_tree[store_id].is_descendant(actor_id, manager_id):
                raise RoleError("Actor is not an owner of the manager", RoleErrorTypes.actor_is_not_owner_of_manager)

            permissions_id = f"{manager_id}_{store_id}"
            self.__stores_to_roles[store_id][manager_id].permissions.set_permissions(
                permissions_id, add_product, change_purchase_policy, change_purchase_types, change_discount_policy,
                change_discount_types, add_manager, get_bid
            )

            # Save to database
            permissions_model = db.session.query(Permissions).filter_by(id=permissions_id).one_or_none()
            if permissions_model is None:
                permissions_model = Permissions()
                db.session.add(permissions_model)

            permissions_model.id = permissions_id
            permissions_model.add_product = add_product
            permissions_model.change_purchase_policy = change_purchase_policy
            permissions_model.change_purchase_types = change_purchase_types
            permissions_model.change_discount_policy = change_discount_policy
            permissions_model.change_discount_types = change_discount_types
            permissions_model.add_manager = add_manager
            permissions_model.get_bid = get_bid

            db.session.commit()

    def remove_role(self, store_id: int, actor_id: int, removed_id: int) -> None:
        with self.__stores_locks[store_id]:
            if store_id not in self.__stores_to_roles:
                raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
            if removed_id not in self.__stores_to_roles[store_id]:
                raise RoleError("Removed user is not a member of the store", RoleErrorTypes.user_not_member_of_store)
            if not self.__authorized_to_add_manager(store_id, actor_id) and actor_id != removed_id:
                raise RoleError("Actor is not authorized to remove a role",
                                RoleErrorTypes.actor_not_authorized_to_remove_role)
            if not self.__stores_to_role_tree[store_id].is_descendant(actor_id, removed_id):
                raise RoleError("Actor is not an ancestor of the removed user",
                                RoleErrorTypes.actor_not_ancestor_of_role)
            if self.__stores_to_role_tree[store_id].is_root(removed_id):
                raise RoleError("Cannot remove the root owner of the store", RoleErrorTypes.cant_remove_founder)

            removed = self.__stores_to_role_tree[store_id].remove_node(removed_id)

            for user_id in removed:
                self.__notifier.notify_removed_management_position(store_id, user_id)
                self.__notifier.unsign_listener(user_id, store_id)
                del self.__stores_to_roles[store_id][user_id]

                # Remove from database
                db.session.query(StoreRole).filter_by(store_id=store_id, user_id=user_id).delete()
                db.session.query(Permissions).filter_by(id=f"{user_id}_{store_id}").delete()
            db.session.commit()

    def get_employees_info(self, store_id: int, actor_id: int) -> Dict[int, str]:  # Dict[user_id, role]
        with self.__stores_locks[store_id]:
            if store_id not in self.__stores_to_roles:
                raise StoreError("Store does not exist",StoreErrorTypes.store_not_found)
            if actor_id not in self.__stores_to_roles[store_id]:
                raise RoleError("Actor is not a member of the store",RoleErrorTypes.actor_not_member_of_store)
            employees = {}
            for user_id, role in self.__stores_to_roles[store_id].items():
                employees[user_id] = role.__str__()

            return employees

    def is_system_manager(self, user_id: int) -> bool:
        return user_id in self.__system_managers

    def add_system_manager(self, actor: int, user_id: int) -> None:
        """
        if Actor is a system manager, he adds a new system manager
        """
        with self.__system_managers_lock:
            if not self.is_system_manager(actor):
                raise RoleError("Actor is not a system manager", RoleErrorTypes.actor_not_system_manager)

            self.__system_managers.append(user_id)

            # Save to database
            system_manager = SystemManagerModel(user_id=user_id, is_admin=False)
            db.session.add(system_manager)
            db.session.commit()

    def remove_system_manager(self, actor: int, user_id: int) -> None:
        with self.__system_managers_lock:
            if user_id == self.__system_admin:
                raise RoleError("Cannot remove the system admin", RoleErrorTypes.cant_remove_system_admin)
            if not self.is_system_manager(actor):
                raise RoleError("Actor is not a system manager", RoleErrorTypes.actor_not_system_manager)
            if user_id not in self.__system_managers:
                raise RoleError("User is not a system manager", RoleErrorTypes.user_not_system_manager)

            self.__system_managers.remove(user_id)

            # Remove from database
            db.session.query(SystemManagerModel).filter_by(user_id=user_id).delete()
            db.session.commit()

    def add_admin(self, user_id: int) -> None:
        """
        this method should not be called (but the facade initialization)
        Add the first system manager to the system
        :return:
        """
        self.__system_managers.append(user_id)
        self.__system_admin = user_id

        # Save to database
        system_admin = SystemManagerModel(user_id=user_id, is_admin=True)
        db.session.add(system_admin)
        db.session.commit()

    def __has_permission(self, store_id: int, user_id: int) -> bool:
        if store_id not in self.__stores_to_roles:
            return False
        if user_id not in self.__stores_to_roles[store_id]:
            return False
        if isinstance(self.__stores_to_roles[store_id][user_id], StoreOwner):
            return True
        raise RoleError("User is a manager",RoleErrorTypes.user_is_manager)

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

    def get_user_nominations(self, user_id: int) -> Dict[int, RoleNominationDTO]:
        nominations = {}
        for nomination_id, nomination in self.__systems_nominations.items():
            if nomination.nominee_id == user_id:
                nominations[nomination_id] = RoleNominationDTO(nomination_id, nomination.store_id,
                                                               nomination.nominator_id, nomination.nominee_id,
                                                               nomination.role.__str__())
        return nominations

    def get_my_stores(self, user_id) -> List[int]:
        stores = []
        for store_id, roles in self.__stores_to_roles.items():
            if user_id in roles:
                stores.append(store_id)
        return stores

    def get_store_role(self, user_id: int, store_id: int) -> str:
        with self.__stores_locks[store_id]:
            if user_id in self.__stores_to_roles[store_id]:
                # if it is the store owner, return ''founder''
                if self.__stores_to_role_tree[store_id].is_root(user_id):
                    return "Founder"
                return self.__stores_to_roles[store_id][user_id].__str__()
            return "User is not a member of the store"

    def get_user_stores(self, user_id: int) -> List[int]:
        stores = []
        for store_id, roles in self.__stores_to_roles.items():
            if user_id in roles:
                stores.append(store_id)
        return stores

    def get_user_employees(self, user_id, store_id) -> List[UserDTO]:
        # check if store exists
        if store_id not in self.__stores_to_roles:
            raise StoreError("Store does not exist",StoreErrorTypes.store_not_found)
        with self.__stores_locks[store_id]:
            if user_id not in self.__stores_to_roles[store_id]:
                raise RoleError("User is not a member of the store", RoleErrorTypes.user_not_member_of_store)
            employees = []
            # return all users under the user_id
            for user, role in self.__stores_to_roles[store_id].items():
                if self.__stores_to_role_tree[store_id].is_descendant(user_id, user) and not user == user_id:
                    if isinstance(role, StoreOwner):
                        employees.append(UserDTO(user_id=user, role=role.__str__(), is_owner=True, add_product=True,
                                                 change_purchase_policy=True, change_purchase_types=True,
                                                 change_discount_policy=True, change_discount_types=True,
                                                 add_manager=True, get_bid=True))
                    else:
                        employees.append(UserDTO(user_id=user, role=role.__str__(), is_owner=False,
                                                 add_product=role.permissions.add_product,
                                                 change_purchase_policy=role.permissions.change_purchase_policy,
                                                 change_purchase_types=role.permissions.change_purchase_types,
                                                 change_discount_policy=role.permissions.change_discount_policy,
                                                 change_discount_types=role.permissions.change_discount_types,
                                                 add_manager=role.permissions.add_manager,
                                                 get_bid=role.permissions.get_bid))

            return employees

    def get_employed_users(self, store_id: int) -> List[int]:
        if store_id not in self.__stores_to_roles:
            raise StoreError("Store does not exist",StoreErrorTypes.store_not_found)
        with self.__stores_locks[store_id]:
            return list(self.__stores_to_roles[store_id].keys())

    def get_bid_owners_managers(self, store_id: int) -> List[int]:
        if store_id not in self.__stores_to_roles:
            raise StoreError("Store does not exist",StoreErrorTypes.store_not_found)
        with self.__stores_locks[store_id]:
            owners_managers = []
            for user_id, role in self.__stores_to_roles[store_id].items():
                if isinstance(role, StoreOwner):
                    owners_managers.append(user_id)
                elif isinstance(role, StoreManager) and role.permissions.get_bid:
                    owners_managers.append(user_id)
            return owners_managers
