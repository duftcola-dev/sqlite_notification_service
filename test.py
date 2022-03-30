import os
import json
from random import sample
import config.config 
import shutil
from utils.Filemapper.DirectoryTreeGenerator import TreeExplorer
from models.model_factory import  factory
from utils.RequestModule.Request import Request
from utils.LogsModule.Logs import Logs
from utils.ProcessHandler.Handler import Handler
from utils.drivers.db_driver import driver
config.config.init()
CONFIG = config.config.CONFIG
import unittest
import asyncio
import pandas


class test_file_mapping(unittest.TestCase):

    client = Request(configuration=CONFIG)
    bucket_path = os.getcwd()+"/bucket/"
    workplace_path = os.getcwd()+"/workspace/"
    processed_path = os.getcwd()+"/processed_data/"
    samples = os.getcwd()+"/samples/"
    model_factory = factory()
    file_mapper = TreeExplorer()
    logs = Logs(log_file=os.getcwd() + "/Logs/logs.txt")
    db_driver = driver(CONFIG["testdatabase"],logs.GetInstance())
    process_handler = Handler(
        bucket_path,
        workplace_path,
        processed_path,
        file_mapper,
        db_driver,
        client.GetInstance(),
        model_factory,
        logs.GetInstance()
    )

    # def test_service_status(self):
    #     result = self.client.Get(CONFIG["service_host"]+CONFIG["endpoints"]["status"])
    #     self.assertTrue(result["OK"]==1,"Remote service is down")

    # def test_create_test_files(self):
    #     self.file_mapper.ExploreDirectories(self.samples)
    #     files = self.file_mapper.GetFilesDict()
    #     self.assertTrue(type(files) is dict,"Failed to copy files")
    #     for file in files:
    #         shutil.copy(files[file],self.bucket_path+file)

    # def test_map_files(self):
    #     self.file_mapper.ExploreDirectories(path=self.bucket_path)
    #     new_files = self.file_mapper.GetFilesDict()
    #     self.assertTrue(type(new_files) is dict,"Failed to map files")

    # def test_request_response(self):
    #     request_model = self.model_factory.create_request_model("Filereceived","testfile.txt","/somepath/","somenewpath/")
    #     data= request_model
    #     headers = {'Content-Type': 'application/json'}
    #     result = self.client.Post(CONFIG["service_host"]+CONFIG["endpoints"]["notifications"],data,header=headers)
    #     self.assertTrue(type(result) is dict,"Remote service no responding")
    #     self.assertTrue(result.get("date")!= None,"Missing param date")
    #     self.assertTrue(result.get("uuid")!= None,"Missing param uuid")
    #     self.assertTrue(result.get("event-type")!= None,"Missing param event-type")
    #     self.assertTrue(result.get("event-data")!= None,"Missing param event-data")
    #     query = self.model_factory.create_query_model(
    #         result.get("date"),
    #         result.get("uuid"),
    #         result.get("event-type"),
    #         result.get("event-data")
    #         )
    #     self.assertTrue(isinstance(query,tuple),"Failed to create query")

    # def test_database(self):
    #     query = (
    #         "INSERT INTO notifications (date,uuid,eventtype,eventdata) VALUES (?,?,?,?)",
    #         [
    #             2022329215613,
    #             "b201cfe0-da50-4243-b317-88a2150c037a",
    #             "FILERECEIVED",
    #             json.dumps({'filename': 'test3.txt', 
    #             'filepath': '/home/duftcola-dev/Repositories/sqlite_service/bucket/test3.txt', 
    #             'moved-to': '/home/duftcola-dev/Repositories/sqlite_service/workspace/test3.txt', 
    #             'received-timestamp': 2022329215613
    #             })
    #         ]
    #     )
    #     test_driver = driver(CONFIG["testdatabase"])
    #     test_driver.connect()
    #     test_driver.insert(query)
    #     test_driver.close()
    
    def test_na_detection(self):
        path  = os.getcwd() + "/samples/missing_values.csv"
        path2 = os.getcwd() + "/processed_data/missing_values.csv"
        file = open(path2,"w")
        file.write("")
        file.close()
        ds = pandas.read_csv(path)
        new_ds = ds.dropna()
        top = new_ds.head(0)
        for item in top:
            new_ds.rename(columns={item:str(item).upper()},inplace=True)
        self.assertNotEqual(len(ds),len(new_ds),"files are different, but no difference was detected")
        #send message
        pandas.DataFrame.to_csv(new_ds,path2,index=False)
    
        
        
    # async def test_main_process(self):
    #     files_list = await self.process_handler.map_files(self.process_handler.file_path)
    #     asyncio.run(self.process_handler.move_files(files_list))
        
    # def test_clean_test_environ(self):
    #     self.file_mapper.ExploreDirectories(path=self.bucket_path)
    #     bucked = self.file_mapper.GetFilesDict()
    #     self.file_mapper.ExploreDirectories(path=self.workplace_path)
    #     work = self.file_mapper.GetFilesDict()
    #     self.file_mapper.ExploreDirectories(path=self.samples)
    #     samples = self.file_mapper.GetFilesDict()
    #     sample_keys = samples.keys()
    #     print(sample_keys)
    #     for b,w in zip(bucked,work):
    #         if b in sample_keys:
    #             os.remove(bucked[b])
    #         if w in sample_keys:
    #             os.remove(work[w])


if __name__ == "__main__":

    unittest.main()