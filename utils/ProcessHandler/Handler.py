import json
import os
import config.config as conf


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
        self.new_files_location = []


    def move_files(self):
        try:
            self.db_driver.connect()
            self.filemapper.ExploreDirectories(path=self.file_path)
            self.log_message("info","fetching files")
            files_list=self.filemapper.GetFilesDict()
            self.new_files_location = []
            self.log_message("info","relocating files")
            query = None
            for files in files_list:
                header,content = self.get_header_content(files_list[files])
                os.remove(files_list[files])
                self.relocate_file(self.workspace_path+files,header,content)
                new_schema = self.models.create_request_model("FILERECEIVED",files,files_list[files],self.workspace_path+files)
                response = self.send_notification(conf.CONFIG["endpoints"]["notifications"],new_schema)
                if isinstance(response,dict):
                    query = self.create_query(response)
                    self.save_notification(query)
                else:
                    self.log_message("error","Backend down!")
                    raise Exception("Backend down , aborting relocation")
                
            
            self.log_message("info","files relocated")
            self.db_driver.close()
            return self.new_files_location

        except Exception as err:
            self.log_message("error",err)




    def log_message(self,e_type,message):
        if self.logs == None:
            print(f"{e_type} | {message}")
        else:
            self.logs.LogMessage(e_type,message)

    def get_header_content(self,path:str):
        file = open(path,"r")
        line = file.readline()
        line = line.upper()
        content =file.readlines()[0:]
        file.close()
        return line,content

    def relocate_file(self,path,header,content):
        self.new_files_location.append(path)
        file = open(path,"a")
        file.write(header)
        file.writelines(content)
        file.close()

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
        