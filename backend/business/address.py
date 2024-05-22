class Address:
    # id of product is productId. It is unique for each physical product
    def __init__(self, address_id, city, country, street, zip_code, house_number):
        self.__address_id = address_id
        self.__city = city
        self.__country = country
        self.__street = street
        self.__zip_code = zip_code
        self.__house_number = house_number

    @property
    def address_id(self):
        return self.__address_id

    @property
    def city(self):
        return self.__city

    @property
    def country(self):
        return self.__country

    @property
    def street(self):
        return self.__street

    @property
    def zip_code(self):
        return self.__zip_code

    @property
    def house_number(self):
        return self.__house_number

    def getLocationConstraints(self):
        pass

    def getLocationCurrency(self):
        pass

    def getLocationTimezone(self):
        pass

    def getLocationLanguage(self):
        pass

    def getLocationWeight(self):
        pass
