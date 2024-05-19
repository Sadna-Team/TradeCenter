import datetime


class NotificationDTO:
    def __init__(self, notification_id: int, message: str, date: datetime) -> None:
        self.__notification_id: int = notification_id
        self.__message: str = message
        self.__date: datetime = date

    def get_notification_id(self) -> int:
        return self.__notification_id

    def get_message(self) -> str:
        return self.__message

    def get_date(self) -> datetime:
        return self.__date
