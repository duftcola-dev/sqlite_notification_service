import datetime
import sys
from typing import Optional
from .src.interface.MetaLog import MetaLogMessage
from .src._CheckType import CheckType


# Author: Robin
# Description : This module contains a . 
# A general purpose method for loggin messages .
# A general purpose factory method that returns log class instance.
# A singleton class for an unique implementation of the log class.
# version 3.1
# tested : yes
# last update: 26/12/2021

class Logs(MetaLogMessage):

    """General purpose log class.

        Author : Robin
        version : 3.2
        tested : yes
        last update : 26/12/2021
    
    Description
    -----------

        General purpose log class. This class is a singleton , can only be declared once.
        In order to use this class in an application make a declaration and used the method 
        GetInstance to get  a reference to the instance of this class.

        The class accepts an url to a log file as optional parameter however it makes no validation if the url
        exists, only raises exeption if the logging process fails.

    Parameters
    ----------

        - log_file : str 
            Url to a log file. It needs to be an absolute url. The class doesnt check prevently if the file exists.

    Raises
    ------

        - Custom exeception Exception if the class have been declared more thatn once. This class is a singleton.

        - FileExistsError if the file trying to be used for log messages doesnt exists.

        - Custom exception Exception , unknown error if writing log message in file fails.

    Returns
    -------

        Returns Logs class instance.

    """

    __instance=None

    def __init__(self,log_file:Optional[str] = None) -> None:

        if Logs.__instance != None:
            raise Exception("Logs can only be implemented once")

        self.__message : str=""
        Logs.__instance=self
        self.__log_file : str=log_file
        

    @staticmethod
    def GetInstance():

        """Returns Logs class instance if exists . If it doesnt exists creates a new instance."""

        if Logs.__instance==None:
            Logs("")
        
        return Logs.__instance


    
    def LogMessage(self,message_type : str, message : str)->None:

        """Log message method.
        
        Description
        -----------

            Creates a log message. Messages are shown or casted by the console.
            Each message is compose by a cathegory and a message.

            There are three valid cathegories :

            - warning
            - error
            - info

            If the message doesnt contain a valid cathegory it is not casted.
            Messsages with the cathegory `error` are stored in a log file the log file exists.

            - `example` : `LogMessage("error","some message")`

        """

        self.__type=["warning","error","info"]
    
        if message_type in self.__type:
            
            date=self.__GetDate()
            
            self.__message=""
            self.__message=date+" | "+message_type+" | "+message+"\n"
            
            if message_type == "error" and self.__log_file != None:
                self.__SaveLogMessage(self.__message)

            sys.stdout.write(self.__message)



    def __SaveLogMessage(self, message : str)->None:
        
        try:
            file=open(self.__log_file,"a")
            file.write(message)
            file.close()
        except FileExistsError:

            sys.stdout.write("ERROR , log class cannot find log file ")

        except Exception as err:

            sys.stdout.write("Log class : Unknown error"+str(err)) 



    def __GetDate(self):
        
        x=datetime.datetime.now()
        Year=str(x.year)
        Month=str(x.month)
        Day=str(x.day)
        Hour=str(x.hour)
        Minute=str(x.minute)
        Second=str(x.second)
        
        return Day+"|"+Month+"|"+Year+" - "+Hour+":"+Minute+":"+Second



#General purpose log method
@CheckType
def LogMessage(message:str):

    """Log message method 

    Description:
    ------------

        General purpose log method.  It doenst store the logs and it is meant just to output logs by console.
    
    """

    x=datetime.datetime.now()
    Year=str(x.year)
    Month=str(x.month)
    Day=str(x.day)
    Hour=str(x.hour)
    Minute=str(x.minute)
    Second=str(x.second)
    
    message=Day+"|"+Month+"|"+Year+" - "+Hour+":"+Minute+":"+Second+" | "+message+"\n"

    sys.stdout.write(message)


