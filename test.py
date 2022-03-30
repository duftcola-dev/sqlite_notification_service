import os
import json
import config.config 
from utils.Filemapper.DirectoryTreeGenerator import TreeExplorer
from models.model_factory import  factory
from utils.RequestModule.Request import Request
from utils.LogsModule.Logs import Logs
from utils.ProcessHandler.Handler import Handler
from utils.drivers.db_driver import driver
config.config.init()
CONFIG = config.config.CONFIG
import unittest


class test_file_mapping(unittest.TestCase):

    client = Request(configuration=CONFIG)
    files_path = os.getcwd()+"/bucket/"
    workplace_path = os.getcwd()+"/workspace/"
    model_factory = factory()
    file_mapper = TreeExplorer()
    logs = Logs(log_file=os.getcwd() + "/Logs/logs.txt")
    db_driver = driver(CONFIG["testdatabase"],logs.GetInstance())
    process_handler = Handler(
        files_path,
        workplace_path,
        file_mapper,
        db_driver,
        client.GetInstance(),
        model_factory,
        logs.GetInstance()
    )

    def test_service_status(self):
        result = self.client.Get(CONFIG["service_host"]+CONFIG["endpoints"]["status"])
        self.assertTrue(result["OK"]==1,"Remote service is down")

    def test_create_test_files(self):
        files = ["test1.txt","test2.txt","test3.txt","test4.txt"]
        for item in files:
            file = open(self.files_path+item,"w")
            file.write("""model,category,pp,transmission,coll,price,hp,lbs,kg/kw,img_url\nAbarth 1500 Biposto Bertone B.A.T 1 '52,Categories unknown,PP ??,FR,?? pts,?? Cr,72,1918.0,12.08 Kg/Hp,https://www.kudosprime.com//gts/images/cars/gts_car_244.jpg?v=gts""")
            file.close()

    def test_map_files(self):
        self.file_mapper.ExploreDirectories(path=self.files_path)
        new_files = self.file_mapper.GetFilesDict()
        self.assertTrue(type(new_files) is dict,"Failed to map files")

    def test_file_content_transfer(self):
        self.file_mapper.ExploreDirectories(path=self.files_path)
        new_files = self.file_mapper.GetFilesDict()
        head = None
        body = None
        for file in new_files:
            head , body = self.process_handler.get_header_content(new_files[file])
            break
        self.assertTrue(type(head) is str,"Failed to get file header")
        self.assertTrue(type(body) is list,"Failed to get file body")

    def test_request_response(self):
        request_model = self.model_factory.create_request_model("Filereceived","testfile.txt","/somepath/","somenewpath/")
        data= request_model
        headers = {'Content-Type': 'application/json'}
        result = self.client.Post(CONFIG["service_host"]+CONFIG["endpoints"]["notifications"],data,header=headers)
        self.assertTrue(type(result) is dict,"Remote service no responding")
        self.assertTrue(result.get("date")!= None,"Missing param date")
        self.assertTrue(result.get("uuid")!= None,"Missing param uuid")
        self.assertTrue(result.get("event-type")!= None,"Missing param event-type")
        self.assertTrue(result.get("event-data")!= None,"Missing param event-data")
        query = self.model_factory.create_query_model(
            result.get("date"),
            result.get("uuid"),
            result.get("event-type"),
            result.get("event-data")
            )
        self.assertTrue(isinstance(query,tuple),"Failed to create query")

    def test_database(self):
        query = (
            "INSERT INTO notifications (date,uuid,eventtype,eventdata) VALUES (?,?,?,?)",
            [
                2022329215613,
                "b201cfe0-da50-4243-b317-88a2150c037a",
                "FILERECEIVED",
                json.dumps({'filename': 'test3.txt', 
                'filepath': '/home/duftcola-dev/Repositories/sqlite_service/bucket/test3.txt', 
                'moved-to': '/home/duftcola-dev/Repositories/sqlite_service/workspace/test3.txt', 
                'received-timestamp': 2022329215613
                })
            ]
        )
        test_driver = driver(CONFIG["testdatabase"])
        test_driver.connect()
        test_driver.insert(query)
        test_driver.close()
        
    def test_main_process(self):
        new_location = self.process_handler.move_files()
        self.assertTrue(type(new_location) is list,"Failed to relocate files")
        self.assertGreater(len(new_location),0, "Failed to fetch files")
        


if __name__ == "__main__":

    unittest.main()