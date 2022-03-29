import abc

class IRequest(metaclass=abc.ABCMeta):


    @classmethod
    def __subclasshook__(cls,subclass):
        return (
            hasattr(subclass,"Ping")and callable(subclass.Ping) and
            hasattr(subclass,"Get")and callable(subclass.Get) and 
            hasattr(subclass,"Post")and callable(subclass.Post) 
        )

    @abc.abstractmethod
    def Ping(self,url:str)->bool:
        """Tests if and url exists, if the result of the request 
        is  != None  then the method returns True else returns False
        """
        raise NotImplementedError

    @abc.abstractmethod
    def Get(self,url:str,header:dict,data:dict)->dict:
        """
        Method uses : url , header , data args

        Get method , accepts data and header in the form of a dictionary.
        The response data is also returned in the form of a dictionary 

        If url is not provided , this method returns False,
        if data in case is provided is not a type dict then returns False.
        Header and params are optional for the get method.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def Post(self,url:str,header:dict,data:dict)->dict:
        """
        Method uses : url , header , data args
        
        Post method , requires data in the form of a dictionary.
        If data is no provided in the form of a dictionary or is not provided at all returns False.
        This method accepts a header as optional argument  in the form of a dictionary
        """
        raise NotImplementedError


    @abc.abstractstaticmethod
    def GetInstance(self):

        """
        Returns the request class instance if exists
        
        """
        raise NotImplementedError

