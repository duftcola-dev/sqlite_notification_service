import datetime

class request_model:

    def __init__(self,event_type,file_name,file_path,new_filepath) -> None:
        self.event_type = event_type
        self.filename = file_name
        self.filepath = file_path
        self.newpath = new_filepath

    def get_schema(self):
        schema = {
            "event-type" : self.event_type,
            "event-data" : {
                "filename" : self.filename,
                "filepath" : self.filepath,
                "moved-to" : self.newpath,
                "received-timestamp"  : datetime.datetime.now()
            }
        }
        return schema

class factory:
    
    def __init__(self) -> None:
        pass

    def create_request_model(self,event_type,file_name,file_path,new_filepath):
        return request_model(event_type,file_name,file_path,new_filepath)