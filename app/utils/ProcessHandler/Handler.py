import datetime
import json
import os
import io
import app.config.config as conf
import shutil
import pandas
import asyncio

class Handler:

    def __init__(self,files_path:str,workspace_path:str,processed_path:str,metadata_path:str,
    filemapper:object,db_driver:object,client:object,models:object,logs = None) -> None:
        self.file_path = files_path
        self.workspace_path  = workspace_path
        self.filemapper = filemapper
        self.processed_path = processed_path
        self.metadata_path = metadata_path
        self.db_driver = db_driver
        self.logs = logs
        self.client = client
        self.models = models

    async def move_files(self):
        files_list = self.map_files(self.file_path)
        if files_list == False or files_list == {}:
            self.log_message("info","No files to map")
            return
        try:
            self.db_driver.connect()
            tasks = []
            for files in files_list:
                task1 = asyncio.ensure_future(self.move(files_list[files],self.workspace_path+files))
                task2 = asyncio.ensure_future(self.create_notification("FILERECEIVED",files_list[files],self.workspace_path+files,files)) 
                tasks.append(task1) 
                tasks.append(task2) 
            await asyncio.gather(*tasks,return_exceptions=True)
            self.log_message("info","files relocated")
            self.db_driver.close()
        except Exception as err:
            self.log_message("error",err)
            self.db_driver.close()

    async def process_files(self):
        try:
            self.log_message("info","post-processing")
            files_list = self.map_files(self.workspace_path)
            if files_list == False or files_list == {}:
                self.log_message("info","No files to map")
                return
            tasks = []
            for files in files_list:
                task1 = asyncio.ensure_future(self.fetch_csv_data(files,files_list))
                task2 = asyncio.ensure_future(self.create_notification("FILEPROCESSED",files_list[files],self.processed_path+files,files))
                tasks.append(task1)
                tasks.append(task2)
            await asyncio.gather(*tasks,return_exceptions=True)
            self.log_message("info","post-process completed")
        except Exception as err:
            self.log_message("error",err)

    async def fetch_csv_data(self,files,files_list):
        init_time = datetime.datetime.now()
        ds = pandas.read_csv(files_list[files],lineterminator='\n')
        self.quick_make_file(files_list[files])
        new_ds = ds.dropna()
        new_ds = self.upper_case_head(new_ds)
        info = self.format_dataframe_info(new_ds)
        changes = abs(len(ds) - len(new_ds))
        pandas.DataFrame.to_csv(new_ds,self.processed_path+files,index=False)
        self.save_metadata(files,init_time,changes,info)
        if changes != 0:
            await self.create_alert("MISSINGDATA",files_list[files])

    def map_files(self,path:str)->dict:
        self.log_message("info",f"fetching files : {path}")
        self.filemapper.ExploreDirectories(path=path)
        return  self.filemapper.GetFilesDict()
            
    async def create_notification(self,event:str,old_path:str,new_path:str,files):
        new_schema = self.models.create_request_model(event,files,old_path,new_path+files)
        response = self.send_notification(conf.CONFIG["endpoints"]["notifications"],new_schema)
        query = self.create_query(response)
        if event == "FILERECEIVED":
            self.save_notification(query)
        return query

    async def create_alert(self,event:str,old_path:str):
        new_schema = self.models.create_alert_model(event,old_path)
        self.send_notification(conf.CONFIG["endpoints"]["notifications"],new_schema)

    def send_notification(self,endpoint,data):
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

    def log_message(self,e_type,message):
        if self.logs == None:
            print(f"{e_type} | {message}")
        else:
            self.logs.LogMessage(e_type,message)

    def upper_case_head(self,dataframe):
        top = dataframe.head(0)
        for item in top:
            dataframe.rename(columns={item:str(item).upper()},inplace=True)
        return dataframe

    def save_metadata(self,file_name,init_time,changes,info):
        with open(self.metadata_path+file_name+".json","w")  as file:
            meta_model = self.models.create_metadata_registry(init_time,changes,info)
            content = json.dumps(meta_model,indent=4)
            file.write(content)
    
    def quick_make_file(self,path):
        with open(path,"w") as file:
            file.write("")

    def format_dataframe_info(self,dataframe_info):
        buffer = io.StringIO()
        dataframe_info.info(buf=buffer)
        string = buffer.getvalue()
        return string

    async def move(self,old_path,new_path):
        shutil.move(old_path,new_path)