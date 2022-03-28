import os
import sys



class TreeExplorer():

    """File mapping module.

    Author : Robin Viera 
    Date : 07/05/2021
    Tested : yes
    Last update : 21/10/2021
    
    Description
    -----------

        Mapping module. The main purpose of this module is to map all the files and directories inside an app.
        The urls of the mapped files and directories are stored in several collections. The values in this collections
        can be used to get access to such files and directories inside and app.Directories and files are mapped belop 
        the target directory.

        - GetFilesDict : Returns a dictionary containing the files mapped.

        - GetFilesList : Returns a list of files.

        - GetDirList : Returns a dictionary containing the directories mapped.

        - GetDirList : Returns a list of directories.
 
    Parameters
    ----------

        - path : str (optional)
            Target directory path . Files and directories will be mapped below this directory.

        - mode : str (optional).
            Way in which the path is used. Path can be "absolute" or "relative" . 
            Absolute path uses an absolute path to the target directory.
            Relative path uses a target relative to the current work directory.
            If no path is provided and mode = ""  then the current directory is used as target.

        - ignore : list 
            List of files or directories that will be ignored during the mapping. 

    Raises
    ------

        This module has no exception handler.
        
    """



    def __init__(self):

        self.__Files_Registry={}
        self.__Dir_Registry={}
        self.__Files_List=[]
        self.__Dir_List=[]
        self.__w_slash=""
        self.path=""
        self.new_path=""



    def ExploreDirectories(self,path:str="",mode:str="absolute",ignore:list=[])->bool:
        

        if type(path) is not str:
            return None

        if type(mode) is not str:
            return None

        if type(ignore) is not list:
            return None


        self.__ignore=ignore
        self.__Files_Registry={}
        self.__Dir_Registry={}
        self.__Files_List=[]
        self.__Dir_List=[]


        if sys.platform == "linux":
            self.__w_slash="/"
        else:
            self.__w_slash="\\"

        current_dir=""
        if path=="" and mode=="":  
            current_dir=os.getcwd()
        elif mode=="absolute" and  path !="":
            current_dir=path
        elif mode=="relative" and path !="":
            current_dir=os.getcwd()
            current_dir=current_dir+self.w_slash+path

        if os.path.isdir(current_dir):
            self.path=current_dir
            self.__Create_Directory_Tree()
        else:
            return False



    def GetFilesDict(self):
        return self.__Files_Registry

    def GetFilesList(self):
        return self.__Files_List

    def GetDirDict(self):
        return self.__Dir_Registry

    def GetDirList(self):
        return self.__Dir_List


 
    def Get_Root_Folder_Path(self)->str:
        
        if(self.path != ""):
            return self.path
        else:
            print(" Path not defined ")
            return False




    def __Create_Directory_Tree(self):
        
        self.__Explore_Directories(self.path)
      


    def __Explore_Directories(self,root:str):

        Current_Dir_Entries=os.scandir(root)

        for entry in Current_Dir_Entries:

            self.new_path=root+self.__w_slash+entry.name
            name=str(entry.name)
            path=str(entry.path)

            if entry.is_dir():
                
                if entry.name in self.__ignore:
                    continue

                self.__Dir_Registry.update({name:path})
                self.__Dir_List.append(path)
                self.__Explore_Directories(self.new_path)

            else:

                if entry.name in self.__ignore:
                    continue

                self.__Files_Registry.update({name:path})
                self.__Files_List.append(path)
                
