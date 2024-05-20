
class Address:
    # id of product is productId. It is unique for each physical product
    def __init__(self, addressId, city, country, street, zipCode, houseNumber):
        self.__addressId = addressId
        self.__city= city
        self.__country = country
        self.__street = street
        self.__zipCode = zipCode
        self.__houseNumber= houseNumber

    
    @property
    def getAddressId(self):
        return self.__addressId
    
    @property
    def getCity(self):
        return self.__city
    
    @property
    def getCountry(self):
        return self.__country
    
    @property
    def getStreet(self):
        return self.__street
    
    @property
    def getZipCode(self):
        return self.__zipCode
    
    @property
    def getHouseNumber(self):
        return self.__houseNumber
    
    @property
    def __setAddressId(self, addressId):
        self.__addressId = addressId

    @property
    def __setCity(self, city):
        self.__city = city

    @property
    def __setCountry(self, country):
        self.__country = country

    @property
    def __setStreet(self, street):
        self.__street = street

    @property
    def __setZipCode(self, zipCode):
        self.__zipCode = zipCode

    @property
    def __setHouseNumber(self, houseNumber):
        self.__houseNumber = houseNumber


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
