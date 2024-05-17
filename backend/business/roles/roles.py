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
            # here you can add fields

    # TODO: when you assign a new role to a user, please use the function "sign_Listener" in the notifier.
    
