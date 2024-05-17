from user import UserFacade
from typing import Dict

class Notifier:

    def __init__(self) -> None:  
        self.user_facade : UserFacade = UserFacade.__new__() # Singelton 
        self.listeners : Dict = {} # Would it restart the listeners every time the server restarts?
  
    def notify(self, user_id: int, message: str) -> None:
        '''
        * Parameters: user_id: int, message: str
        * This function sends a message to a single user.
        '''
        self.user_facade.notify_user(user_id, message)
    
    # Notify on new purchase --- for store owner    
    def notify_new_purchase(self, store_id: int, purchase_id: int) -> None:
        ''' 
        * Parameters: store_id: int
        * This function notifies the store owner(s) of a new purchase in the store.
        '''
        if store_id not in self.listeners:
            return Exception("No listeners for the store with ID:", store_id)

        else:
            msg = "New purchase in store: " + str(store_id) + "\n purchase ID: " + str(purchase_id) + "With the info:"
            for ownerID in self.listeners[store_id]:  
                self.notify(ownerID, msg)

    # Notify on a store update (closed or opened) --- for store owner
    def notify_update_store_status(self, store_id: int, AdditionalDetails, isClosed: bool) -> None:
        ''' 
        * Parameters: store_id: int, isClosed: bool
        * isClosed is a boolean - *True* if the store is closed *False* if the store is opened.
        * This function notifies the store owner(s) on a change in the store status (closed or opened).
        '''

        if isClosed:
            update = "closed"
        else:
            update = "opened"

        if store_id not in self.listeners:
            return Exception("No listeners for the store with ID:", store_id)
        else:
            msg = "Store status updated on: " + str(store_id) + "\n Store is now: " + update
            for ownerID in self.listeners[store_id]:  
                self.notify(ownerID, msg)

    # Notify on a removed managment position --- for store owner
    def notify_removed_management_position(self, store_id: int, user_id: int) -> None:
        ''' 
        * Parameters: store_id: int, user_id: int
        * This function notifies a store owner that he was removed from the management position.
        '''
        if store_id not in self.listeners:
            return Exception("No listeners for the store with ID:", store_id)
        else:
            msg = "Management position from store: " + str(store_id) + " was removed from you."
            self.notify(user_id, msg)

    # Notify om a new message --- for member
    def notify_general_message(self, user_id: int, message: str) -> None:
        ''' 
        * Parameters: user_id: int, message: str
        * This function notifies a user on a new message.
        '''
        self.notify(user_id, message)
 
    def sign_Listener(self, user_id: int, store_id: int) -> None:
        ''' 
        * Parameters: user_id: int, store_id: int
        * This function adds a new user (new manager or new owner) to the store listeners.
        * It would alert him to the events that are relevant to the store (new purchase, store update, removed management position)
        '''
        if store_id not in self.listeners:
            self.listeners[store_id] = []
        self.listeners[store_id].append(user_id)
    
    def unsign_Listener(self, user_id: int, store_id: int) -> None:
        ''' 
        * Parameters: user_id: int, store_id: int
        * This function removes a user (manager or owner) from the store listeners.
        '''
        if store_id in self.listeners:
            self.listeners[store_id].remove(user_id)
