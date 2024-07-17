from abc import ABCMeta
from typing import Dict, List, Optional
from threading import Lock
from backend.business.notifier.notifier import Notifier
from backend.error_types import *
from backend.database import db
from sqlalchemy.ext.declarative import declared_attr
from backend.business.DTOs import RoleNominationDTO, UserDTO
import sqlalchemy.exc

import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Roles Logger")

class Permissions(db.Model):
    __tablename__ = 'permissions'

    store_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    add_product = db.Column(db.Boolean, nullable=False, default=False)
    change_purchase_policy = db.Column(db.Boolean, nullable=False, default=False)
    change_purchase_types = db.Column(db.Boolean, nullable=False, default=False)
    change_discount_policy = db.Column(db.Boolean, nullable=False, default=False)
    change_discount_types = db.Column(db.Boolean, nullable=False, default=False)
    add_manager = db.Column(db.Boolean, nullable=False, default=False)
    get_bid = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, store_id, user_id):
        self.store_id = store_id
        self.user_id = user_id
        self.add_product = False
        self.change_purchase_policy = False
        self.change_purchase_types = False
        self.change_discount_policy = False
        self.change_discount_types = False
        self.add_manager = False
        self.get_bid = False

    def set_permissions(self, add_product: bool, change_purchase_policy: bool, change_purchase_types: bool,
                        change_discount_policy: bool, change_discount_types: bool, add_manager: bool, get_bid: bool):
        self.add_product = add_product
        self.change_purchase_policy = change_purchase_policy
        self.change_purchase_types = change_purchase_types
        self.change_discount_policy = change_discount_policy
        self.change_discount_types = change_discount_types
        self.add_manager = add_manager
        self.get_bid = get_bid

class AbstractBaseModel(db.Model):
    __abstract__ = True
    __metaclass__ = ABCMeta

    @declared_attr
    def store_id(cls):
        return db.Column(db.Integer, primary_key=True)

    @declared_attr
    def user_id(cls):
        return db.Column(db.Integer, primary_key=True)

class StoreRole(AbstractBaseModel):
    __tablename__ = 'store_roles'

    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'store_role'
    }

    def __init__(self, store_id, user_id):
        self.store_id = store_id
        self.user_id = user_id

    def __str__(self):
        return self.__class__.__name__

class StoreOwner(StoreRole):
    __tablename__ = 'store_owners'

    __mapper_args__ = {
        'polymorphic_identity': 'store_owner',
        'inherit_condition': (
            (StoreRole.store_id == db.column('store_owners.store_id')) &
            (StoreRole.user_id == db.column('store_owners.user_id'))
        )
    }

    def __init__(self, store_id, user_id):
        super().__init__(store_id, user_id)

    def __str__(self):
        return "StoreOwner"

class StoreManager(StoreRole):
    __tablename__ = 'store_managers'

    __mapper_args__ = {
        'polymorphic_identity': 'store_manager',
        'inherit_condition': (
            (StoreRole.store_id == db.column('store_managers.store_id')) &
            (StoreRole.user_id == db.column('store_managers.user_id'))
        )
    }

    def __init__(self, store_id, user_id):
        super().__init__(store_id, user_id)
        self.permissions = Permissions(store_id, user_id)

    def __str__(self):
        return "StoreManager"

class Nomination(db.Model):
    __tablename__ = 'nominations'
    __nomination_id_serializer = 0

    nomination_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, nullable=False)
    nominator_id = db.Column(db.Integer, nullable=False)
    nominee_id = db.Column(db.Integer, nullable=False)
    role_store_id = db.Column(db.Integer, nullable=False)
    role_user_id = db.Column(db.Integer, nullable=False)
    role_type = db.Column(db.String(50), nullable=False)

    def __init__(self, store_id, nominator_id: int, nominee_id: int, role: StoreRole):
        self.nomination_id = Nomination.__nomination_id_serializer
        Nomination.__nomination_id_serializer += 1
        self.store_id = store_id
        self.nominator_id = nominator_id
        self.nominee_id = nominee_id
        self.role_store_id = role.store_id
        self.role_user_id = role.user_id
        self.role_type = role.type
        self.role = role

    @classmethod
    def get_max_nomination_id(cls):
        max_id = db.session.query(db.func.max(cls.nomination_id)).scalar()
        return max_id if max_id is not None else 0

    # when loading from db, the role is not stored in the db, so we need to set it manually
    def set_role(self, role: StoreRole):
        self.role = role


class TreeNode(db.Model):
    __tablename__ = 'tree_nodes'

    data = db.Column(db.Integer, nullable=False, primary_key=True)
    store_id = db.Column(db.Integer, nullable=False, primary_key=True)
    parent_id = db.Column(db.Integer, nullable=True)
    is_root = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, data: int, store_id: int, parent_id: Optional[int] = None, is_root: bool = False):
        self.data = data
        self.store_id = store_id
        self.parent_id = parent_id
        self.is_root = is_root



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
    def from_db(store_id: int) -> 'Tree':
        root_node = db.session.query(TreeNode).filter_by(store_id=store_id, is_root=True).one_or_none()
        if not root_node:
            raise StoreError(f"No root node found for store_id: {store_id}", StoreErrorTypes.store_not_found)
        root = Node(root_node.data, root_node.store_id, root_node.parent_id)
        tree = Tree(root)
        Tree.__load_children(root)
        return tree

    @staticmethod
    def __load_children(node: Node) -> None:
        child_nodes = db.session.query(TreeNode).filter_by(parent_id=node.data).all()
        for child_node in child_nodes:
            child = Node(child_node.data, child_node.store_id, child_node.parent_id)
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
            self.__notifier = Notifier()

            Nomination.__nomination_id_serializer = Nomination.get_max_nomination_id() + 1

            self.__creation_lock = Lock()
            self.__stores_locks: Dict[int, Lock] = {}
            self.__system_managers_lock = Lock()

    def __load_trees_from_db(self) -> Dict[int, Tree]:
        trees = {}
        root_nodes = db.session.query(TreeNode).filter_by(is_root=True).all()
        for root_node in root_nodes:
            trees[root_node.store_id] = Tree.from_db(root_node.store_id)
        return trees

    def __load_roles_from_db(self) -> Dict[int, Dict[int, StoreRole]]:
        roles = {}
        store_roles = db.session.query(StoreRole).all()

        for store_role in store_roles:
            store_id = store_role.store_id
            if store_id not in roles:
                roles[store_id] = {}

            if store_role.type == 'store_owner':
                roles[store_id][store_role.user_id] = StoreOwner(store_id=store_id, user_id=store_role.user_id)
            elif store_role.type == 'store_manager':
                manager = StoreManager(store_id=store_id, user_id=store_role.user_id)
                roles[store_id][store_role.user_id] = manager

        return roles

    def __load_nominations_from_db(self) -> Dict[int, Nomination]:
        nominations = {}
        db_nominations = db.session.query(Nomination).all()
        for db_nomination in db_nominations:
            if db_nomination.role_type == 'store_owner':
                role = StoreOwner(store_id=db_nomination.store_id, user_id=db_nomination.nominee_id)
            else:
                role = StoreManager(store_id=db_nomination.store_id, user_id=db_nomination.nominee_id)

            nomination = Nomination(
                store_id=db_nomination.store_id,
                nominator_id=db_nomination.nominator_id,
                nominee_id=db_nomination.nominee_id,
                role=role
            )
            nominations[db_nomination.nomination_id] = nomination
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

        from backend.app_factory import get_app
        with get_app().app_context():
            db.session.query(Permissions).delete()
            db.session.query(StoreOwner).delete()
            db.session.query(StoreManager).delete()
            db.session.query(TreeNode).delete()
            db.session.query(StoreRole).delete()
            db.session.query(Nomination).delete()
            db.session.query(SystemManagerModel).delete()
            db.session.commit()

    def add_store(self, store_id: int, owner_id: int) -> None:
        from flask import current_app as app
        with app.app_context():
            if db.session.query(TreeNode).filter_by(store_id=store_id, is_root=True).first():
                raise RoleError("Store already exists", RoleErrorTypes.store_already_exists)

            # Create root node for the store tree
            root_node = TreeNode(data=owner_id, store_id=store_id, is_root=True)

            # Add the root node to the session and commit
            db.session.add(root_node)
            db.session.commit()

            # Add store owner role and commit to database
            store_owner = StoreOwner(store_id=store_id, user_id=owner_id)
            db.session.add(store_owner)
            db.session.commit()

            # Initialize store lock
            self.__stores_locks[store_id] = Lock()

            self.__notifier.sign_listener(owner_id, store_id)

    def remove_store(self, store_id: int, actor_id: int) -> None:
        if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        if not db.session.query(StoreRole).filter_by(store_id=store_id, user_id=actor_id).first():
            raise RoleError('Actor is not a member of the store', RoleErrorTypes.user_not_member_of_store)
        if not self.is_root(store_id, actor_id):
            raise RoleError('Actor is not the root owner of the store', RoleErrorTypes.actor_not_founder)

        # Remove from database
        db.session.query(TreeNode).filter(TreeNode.store_id == store_id).delete()
        db.session.commit()

        db.session.query(StoreRole).filter(StoreRole.store_id == store_id).delete()
        db.session.commit()

        self.__stores_locks.pop(store_id, None)

    def nominate_owner(self, store_id: int, nominator_id: int, nominee_id: int) -> int:
        with self.__stores_locks[store_id]:
            self.__check_nomination_validation(store_id, nominator_id, nominee_id)
            if not isinstance(self.get_role(store_id, nominator_id), StoreOwner):
                raise RoleError("Nominator is not an owner", RoleErrorTypes.nominator_not_owner)

            nomination = Nomination(store_id, nominator_id, nominee_id, StoreOwner(store_id, nominee_id))

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

            nomination = Nomination(store_id, nominator_id, nominee_id, StoreManager(store_id, nominee_id))

            # Save to database
            db.session.add(nomination)
            db.session.commit()

            return nomination.nomination_id

    def __authorized_to_add_manager(self, store_id: int, nominator_id: int) -> bool:
        role = self.get_role(store_id, nominator_id)
        return isinstance(role, StoreOwner) or (isinstance(role, StoreManager) and role.permissions.add_manager)

    def __check_nomination_validation(self, store_id: int, nominator_id: int, nominee_id: int) -> None:
        if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        if not db.session.query(StoreRole).filter_by(store_id=store_id, user_id=nominator_id).first():
            raise RoleError("Nominator is not a member of the store", RoleErrorTypes.nominator_not_member_of_store)
        if db.session.query(StoreRole).filter_by(store_id=store_id, user_id=nominee_id).first():
            raise RoleError("Nominee is already a member of the store", RoleErrorTypes.nominee_already_exists_in_store)

    def accept_nomination(self, nomination_id: int, nominee_id: int) -> None:
        nomination = db.session.query(Nomination).filter_by(nomination_id=nomination_id).one_or_none()
        if not nomination:
            raise RoleError(f"Nomination does not exist - given id - {nomination_id}",
                            RoleErrorTypes.nomination_does_not_exist)
        if nominee_id != nomination.nominee_id:
            raise RoleError("Nominee id does not match the nomination", RoleErrorTypes.nominee_id_error)
        role_type = nomination.role_type

        self.__stores_locks.setdefault(nomination.store_id, Lock())
        with self.__stores_locks[nomination.store_id]:

            if role_type == 'store_owner':
                if db.session.query(StoreRole).filter_by(store_id=nomination.store_id, user_id=nominee_id).first():
                    raise RoleError("Nominee is already a member of the store",
                                    RoleErrorTypes.nominee_already_exists_in_store)
                role = StoreOwner(store_id=nomination.store_id, user_id=nominee_id)
            else:
                if db.session.query(StoreRole).filter_by(store_id=nomination.store_id, user_id=nominee_id).first():
                    raise RoleError("Nominee is already a member of the store",
                                    RoleErrorTypes.nominee_already_exists_in_store)
                role = StoreManager(store_id=nomination.store_id, user_id=nominee_id)
                db.session.add(role.permissions)
                db.session.commit()
            db.session.add(role)
            db.session.commit()

            # Add the user to the store tree
            treeNode = TreeNode(data=nominee_id, store_id=nomination.store_id, parent_id=nomination.nominator_id)
            db.session.add(treeNode)
            db.session.commit()

            self.__notifier.sign_listener(nominee_id, nomination.store_id)

            # Delete all nominations of the nominee in the store
            db.session.query(Nomination).filter_by(store_id=nomination.store_id, nominee_id=nominee_id).delete()
            db.session.commit()
            logger.info(f"User {nominee_id} accepted the nomination {nomination_id} in store {nomination.store_id}")

    def decline_nomination(self, nomination_id: int, nominee_id) -> None:
        nomination = db.session.query(Nomination).filter_by(nomination_id=nomination_id).one_or_none()
        if not nomination:
            raise RoleError("Nomination does not exist", RoleErrorTypes.nomination_does_not_exist)
        if nominee_id != nomination.nominee_id:
            raise RoleError("Nominee id does not match the nomination", RoleErrorTypes.nominee_id_error)

        db.session.query(Nomination).filter_by(nomination_id=nomination_id).delete()
        db.session.commit()

        logger.info(f"User {nominee_id} declined the nomination {nomination_id} in store {nomination.store_id}")

    def set_manager_permissions(self, store_id: int, actor_id: int, manager_id: int, add_product: bool,
                                change_purchase_policy: bool, change_purchase_types: bool, change_discount_policy: bool,
                                change_discount_types: bool, add_manager: bool, get_bid: bool) -> None:
        with self.__stores_locks[store_id]:
            if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
                raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
            if not db.session.query(StoreRole).filter_by(store_id=store_id, user_id=manager_id).first():
                raise RoleError("Manager is not a member of the store", RoleErrorTypes.manager_not_member_of_store)
            if not isinstance(self.get_role(store_id, manager_id), StoreManager):
                raise RoleError("User is not a manager", RoleErrorTypes.user_not_manager)
            if not self.is_descendant(store_id, actor_id, manager_id):
                raise RoleError("Actor is not an owner of the manager", RoleErrorTypes.actor_is_not_owner_of_manager)

            permissions_model = db.session.query(Permissions).filter_by(store_id=store_id, user_id=manager_id).one_or_none()
            if permissions_model is None:
                permissions_model = Permissions(store_id, manager_id)
                db.session.add(permissions_model)

            permissions_model.set_permissions(add_product, change_purchase_policy, change_purchase_types,
                                              change_discount_policy, change_discount_types, add_manager, get_bid)

            db.session.commit()

    def remove_role(self, store_id: int, actor_id: int, removed_id: int) -> None:
        with self.__stores_locks[store_id]:
            if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
                raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
            if not db.session.query(StoreRole).filter_by(store_id=store_id, user_id=removed_id).first():
                raise RoleError("Removed user is not a member of the store", RoleErrorTypes.user_not_member_of_store)
            if not self.__authorized_to_add_manager(store_id, actor_id) and actor_id != removed_id:
                raise RoleError("Actor is not authorized to remove a role",
                                RoleErrorTypes.actor_not_authorized_to_remove_role)
            if not self.is_descendant(store_id, actor_id, removed_id):
                raise RoleError("Actor is not an ancestor of the removed user",
                                RoleErrorTypes.actor_not_ancestor_of_role)
            if self.is_root(store_id, removed_id):
                raise RoleError("Cannot remove the root owner of the store", RoleErrorTypes.cant_remove_founder)

            removed_nodes = self.remove_node(store_id, removed_id)
            for user_id in removed_nodes:
                self.__notifier.notify_removed_management_position(store_id, user_id)
                self.__notifier.unsign_listener(user_id, store_id)
                db.session.query(StoreRole).filter_by(store_id=store_id, user_id=user_id).delete()
                db.session.query(Permissions).filter_by(store_id=store_id, user_id=user_id).delete()
            db.session.commit()

    def get_employees_info(self, store_id: int, actor_id: int) -> Dict[int, str]:
        if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        if not db.session.query(StoreRole).filter_by(store_id=store_id, user_id=actor_id).first():
            raise RoleError("Actor is not a member of the store", RoleErrorTypes.actor_not_member_of_store)

        employees = {}
        roles = db.session.query(StoreRole).filter_by(store_id=store_id).all()
        for role in roles:
            employees[role.user_id] = role.__str__()
        return employees

    def is_system_manager(self, user_id: int) -> bool:
        return db.session.query(SystemManagerModel).filter_by(user_id=user_id).first() is not None

    def add_system_manager(self, actor: int, user_id: int) -> None:
        with self.__system_managers_lock:
            res = db.session.query(SystemManagerModel).filter_by(is_admin=True).first() is not None
            if not self.is_system_manager(actor) and res:
                raise RoleError("Actor is not a system manager", RoleErrorTypes.actor_not_system_manager)
            if self.is_system_manager(user_id):
                return
            system_manager_model = SystemManagerModel(user_id=user_id, is_admin=False)
            db.session.add(system_manager_model)
            db.session.commit()

    def remove_system_manager(self, actor: int, user_id: int) -> None:
        with self.__system_managers_lock:
            if self.__load_system_admin_from_db() == user_id:
                raise RoleError("Cannot remove the system admin", RoleErrorTypes.cant_remove_system_admin)
            if not self.is_system_manager(actor):
                raise RoleError("Actor is not a system manager", RoleErrorTypes.actor_not_system_manager)
            if not self.is_system_manager(user_id):
                raise RoleError("User is not a system manager", RoleErrorTypes.user_not_system_manager)
            db.session.query(SystemManagerModel).filter_by(user_id=user_id).delete()
            db.session.commit()

    def add_admin(self, user_id: int) -> None:
        if self.__load_system_admin_from_db() != -1:
            return

        system_manager_model = SystemManagerModel(user_id=user_id, is_admin=True)
        db.session.add(system_manager_model)
        db.session.flush()

    def __has_permission(self, store_id: int, user_id: int) -> bool:
        role = self.get_role(store_id, user_id)
        if isinstance(role, StoreOwner):
            return True
        if isinstance(role, StoreManager):
            return False
        raise RoleError("Invalid role type", RoleErrorTypes.invalid_role)

    def has_add_product_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except RoleError:
                role = self.get_role(store_id, user_id)
                if isinstance(role, StoreManager):
                    return role.permissions.add_product
                return False

    def has_change_purchase_policy_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except RoleError:
                role = self.get_role(store_id, user_id)
                if isinstance(role, StoreManager):
                    return role.permissions.change_purchase_policy
                return False

    def has_change_purchase_types_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except RoleError:
                role = self.get_role(store_id, user_id)
                if isinstance(role, StoreManager):
                    return role.permissions.change_purchase_types
                return False

    def has_change_discount_policy_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except RoleError:
                role = self.get_role(store_id, user_id)
                if isinstance(role, StoreManager):
                    return role.permissions.change_discount_policy
                return False

    def has_change_discount_types_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except RoleError:
                role = self.get_role(store_id, user_id)
                if isinstance(role, StoreManager):
                    return role.permissions.change_discount_types
                return False

    def has_add_manager_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except RoleError:
                role = self.get_role(store_id, user_id)
                if isinstance(role, StoreManager):
                    return role.permissions.add_manager
                return False

    def has_get_bid_permission(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            try:
                return self.__has_permission(store_id, user_id)
            except RoleError:
                role = self.get_role(store_id, user_id)
                if isinstance(role, StoreManager):
                    return role.permissions.get_bid
                return False

    def is_owner(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            role = self.get_role(store_id, user_id)
            return isinstance(role, StoreOwner)

    def is_manager(self, store_id: int, user_id: int) -> bool:
        with self.__stores_locks[store_id]:
            role = self.get_role(store_id, user_id)
            return isinstance(role, StoreManager)

    def get_store_owners(self, store_id: int) -> Dict[int, str]:
        with self.__stores_locks[store_id]:
            owners = {}
            roles = db.session.query(StoreRole).filter_by(store_id=store_id).all()
            for role in roles:
                owners[role.user_id] = role.__str__()
            return owners

    def get_user_nominations(self, user_id: int) -> Dict[int, RoleNominationDTO]:
        nominations = {}
        db_nominations = db.session.query(Nomination).filter_by(nominee_id=user_id).all()
        for db_nomination in db_nominations:
            nominations[db_nomination.nomination_id] = RoleNominationDTO(
                db_nomination.nomination_id,
                db_nomination.store_id,
                db_nomination.nominator_id,
                db_nomination.nominee_id,
                db_nomination.role.__str__()
            )
        return nominations

    def get_my_stores(self, user_id) -> List[int]:
        stores = []
        roles = db.session.query(StoreRole).filter_by(user_id=user_id).all()
        for role in roles:
            stores.append(role.store_id)
        return stores

    def get_store_role(self, user_id: int, store_id: int) -> str:
        with self.__stores_locks[store_id]:
            role = db.session.query(StoreRole).filter_by(store_id=store_id, user_id=user_id).one_or_none()
            if role:
                if self.is_root(store_id, user_id):
                    return "Founder"
                return role.__str__()
            return "User is not a member of the store"

    def get_user_stores(self, user_id: int) -> List[int]:
        stores = []
        roles = db.session.query(StoreRole).filter_by(user_id=user_id).all()
        for role in roles:
            stores.append(role.store_id)
        return stores

    def get_user_employees(self, user_id, store_id) -> List[UserDTO]:
        if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        with self.__stores_locks[store_id]:
            if not db.session.query(StoreRole).filter_by(store_id=store_id, user_id=user_id).first():
                raise RoleError("User is not a member of the store", RoleErrorTypes.user_not_member_of_store)
            employees = []
            roles = db.session.query(StoreRole).filter_by(store_id=store_id).all()
            for role in roles:
                if self.is_descendant(store_id, user_id, role.user_id) and user_id != role.user_id:
                    if isinstance(role, StoreOwner):
                        employees.append(UserDTO(
                            user_id=role.user_id,
                            role=role.__str__(),
                            is_owner=True,
                            add_product=True,
                            change_purchase_policy=True,
                            change_purchase_types=True,
                            change_discount_policy=True,
                            change_discount_types=True,
                            add_manager=True,
                            get_bid=True
                        ))
                    else:
                        employees.append(UserDTO(
                            user_id=role.user_id,
                            role=role.__str__(),
                            is_owner=False,
                            add_product=role.permissions.add_product,
                            change_purchase_policy=role.permissions.change_purchase_policy,
                            change_purchase_types=role.permissions.change_purchase_types,
                            change_discount_policy=role.permissions.change_discount_policy,
                            change_discount_types=role.permissions.change_discount_types,
                            add_manager=role.permissions.add_manager,
                            get_bid=role.permissions.get_bid
                        ))
            return employees

    def get_employed_users(self, store_id: int) -> List[int]:
        if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        with self.__stores_locks[store_id]:
            roles = db.session.query(StoreRole).filter_by(store_id=store_id).all()
            return [role.user_id for role in roles]

    def get_bid_owners_managers(self, store_id: int) -> List[int]:
        if not db.session.query(StoreRole).filter_by(store_id=store_id).first():
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        with self.__stores_locks[store_id]:
            owners_managers = []
            roles = db.session.query(StoreRole).filter_by(store_id=store_id).all()
            for role in roles:
                if isinstance(role, StoreOwner):
                    owners_managers.append(role.user_id)
                elif isinstance(role, StoreManager) and role.permissions.get_bid:
                    owners_managers.append(role.user_id)
            return owners_managers

    def get_role(self, store_id: int, user_id: int) -> StoreRole:
        return db.session.query(StoreRole).filter_by(store_id=store_id, user_id=user_id).one_or_none()

    def get_permissions(self, store_id: int, user_id: int) -> Permissions:
        return db.session.query(Permissions).filter_by(store_id=store_id, user_id=user_id).one_or_none()

    def is_root(self, store_id: int, user_id: int) -> bool:
        root_node = db.session.query(TreeNode).filter_by(store_id=store_id, is_root=True).one_or_none()
        if not root_node:
            raise StoreError("Store does not exist", StoreErrorTypes.store_not_found)
        return root_node.data == user_id

    def is_descendant(self, store_id: int, ancestor_id: int, descendant_id: int) -> bool:
        tree = Tree.from_db(store_id)
        return tree.is_descendant(ancestor_id, descendant_id)

    def remove_node(self, store_id: int, user_id: int) -> List[int]:
        tree = Tree.from_db(store_id)
        removed_nodes = tree.remove_node(user_id)
        db.session.query(TreeNode).filter(TreeNode.store_id == store_id, TreeNode.data == user_id).delete()
        db.session.commit()
        return removed_nodes

    def is_admin_created(self):
        return self.__load_system_admin_from_db() != -1

    def get_nomination(self, nomination_id: int) -> Nomination:

        nomination = db.session.query(Nomination).filter_by(nomination_id=nomination_id).one_or_none()
        return nomination
