import abc


class MetaLogMessage(metaclass=abc.ABCMeta):


    @classmethod
    def __subclasshook__(cls,subclass):
        return (

            hasattr(subclass,"LogMessage") and callable(subclass.LogMessage)
          
        )

    @abc.abstractmethod
    def LogMessage(self,message_type:str,message:str):

        """
        --> messaget_type(str)
        --> message(str)

        <---None

        Description :
        General purpose log method.
        Takes a string as argument indicating the message type : info,error or warning
        and a string containing the message itself.

        If the message type is the type error and the class has acces the url of log file then
        all error type log messages will be written to such file.

        
        """
        raise NotImplementedError

    @abc.abstractstaticmethod
    def GetInstance(self):

        """Returns an instance of the class log """
        raise NotImplementedError