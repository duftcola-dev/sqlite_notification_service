import json
import os
import config.config as conf
import shutil
import pandas

class Handler:

    def __init__(self,files_path:str,workspace_path:str,processed_path:str,filemapper:object,
    db_driver:object,client:object,models:object,logs = None) -> None:
        self.file_path = files_path
        self.workspace_path  = workspace_path
        self.filemapper = filemapper
        self.processed_path = processed_path
        self.db_driver = db_driver
        self.logs = logs
        self.client = client
        self.models = models

    async def move_files(self,files_list:dict):
        try:
            self.db_driver.connect()
            for files in files_list:
                shutil.move(files_list[files],self.workspace_path+files)
                await self.create_notification(files_list[files],self.workspace_path+files,files)
            self.log_message("info","files relocated")
            self.db_driver.close()
        except Exception as err:
            self.log_message("error",err)

    async def process_files(self,files_list:dict):
        for files in files_list:
            file_context=pandas.read_csv(files_list[files])
            headers = file_context.info()


    async def map_files(self,path:str)->dict:
        self.filemapper.ExploreDirectories(path=path)
        self.log_message("info","fetching files")
        return  self.filemapper.GetFilesDict()
            
    async def create_notification(self,old_path:str,new_path:str,files,):
        new_schema = self.models.create_request_model("FILERECEIVED",files,old_path,new_path+files)
        response = self.send_notification(conf.CONFIG["endpoints"]["notifications"],new_schema)
        query = self.create_query(response)
        self.save_notification(query)
        
    def send_notification(self,endpoint,data):
        print("sending")
        result = self.client.Post(conf.CONFIG["service_host"]+endpoint,data,header={'Content-Type': 'application/json'})
        return result

    def create_query(self,json_response:json)->str:
        return self.models.create_query_model(
            json_response.get("date"),
            json_response.get("uuid"),
            json_response.get("event-type"),
            json_response.get("event-data")
        )
    
    def save_notification(self,query):
        self.db_driver.insert(query)
        
    def stablish_db_conection(self):
        self.db_driver.connect()

    def log_message(self,e_type,message):
        if self.logs == None:
            print(f"{e_type} | {message}")
        else:
            self.logs.LogMessage(e_type,message)