import json
import os
import config.config as conf
import shutil
import asyncio

class Handler:

    def __init__(self,files_path:str,workspace_path:str,filemapper:object,
    db_driver:object,client:object,models:object,logs = None) -> None:
        self.file_path = files_path
        self.workspace_path  = workspace_path
        self.filemapper = filemapper
        self.db_driver = db_driver
        self.logs = logs
        self.client = client
        self.models = models



    async def move_files(self):
        try:
            self.db_driver.connect()
            files_list=await self.map_files(self.file_path)
            for files in files_list:
                shutil.move(files_list[files],self.workspace_path+files)
                await self.create_notification(files_list[files],self.workspace_path+files,files)
            self.log_message("info","files relocated")
            self.db_driver.close()

        except Exception as err:
            self.log_message("error",err)


    # async def process_files(self):
    #     self.filemapper.ExploreDirectories(path=self.workspace_path)
    #     header,content = self.get_header_content(files_list[files])


    # def get_header_content(self,path:str):
    #     file = open(path,"r")
    #     line = file.readline()
    #     line = line.upper()
    #     content =file.readlines()[0:]
    #     file.close()
    #     return line,content

    # def relocate_file(self,path,header,content):
    #     self.new_files_location.append(path)
    #     file = open(path,"a")
    #     file.write(header)
    #     file.writelines(content)
    #     file.close()

    async def map_files(self,path:str):
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