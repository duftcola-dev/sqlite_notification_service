import datetime
import json
class query_model:
    def __init__(self,date,uuid,eventtype,eventdata) -> None:
        self.date = date
        self.uuid = uuid
        self.eventtype = eventtype
        self.eventdata = eventdata
        
    def get_query(self):
        query = (
            "INSERT INTO notifications (date,uuid,eventtype,eventdata) VALUES (?,?,?,?);",
            [self.date,self.uuid,self.eventtype,json.dumps(self.eventdata)]
        )
        return query

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
                "received-timestamp"  : self.__get_int_date()
            }
        }
        return schema
    
    def __get_int_date(self)->int:
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second

        s=f"{year}{month}{day}{hour}{minute}{second}"
        return int(s)

class alert_model:
    
    def __init__(self,event,old_path) -> None:
        self.event  = event 
        self.old_path = old_path
    
    def get_schema(self):
        schema = {
            "event-type" : self.event,
            "event-data" : {
                "filepath" : self.old_path,
                "received-timestamp"  : self.__get_int_date()
            }
        }
        return schema
        
    def __get_int_date(self)->int:
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second

        s=f"{year}{month}{day}{hour}{minute}{second}"
        return int(s)

class medatdata_model:

    def __init__(self,init_time,changes,info) -> None:
        self.init_time = str(init_time),
        self.end_time = str(datetime.datetime.now())
        self.changes = changes
        self.info = info

    def get_schema(self):
        schema = {
            "task_start_time":self.init_time,
            "task_end_time":self.end_time,
            "changes":self.changes,
            "original_file_info":self.info
        }
        return schema

class factory:
    
    def __init__(self) -> None:
        pass

    def create_request_model(self,event_type,file_name,file_path,new_filepath):
        return request_model(event_type,file_name,file_path,new_filepath).get_schema()

    def create_query_model(self,date,uuid,eventtype,eventdata):
        return query_model(date,uuid,eventtype,eventdata).get_query()

    def create_alert_model(self,event,old_path):
        return alert_model(event,old_path).get_schema()

    def create_metadata_registry(self,init_time,changes,info):
        return medatdata_model(init_time,changes,info).get_schema()