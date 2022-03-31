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


class monolitic_test(unittest.TestCase):

    client = Request(configuration=CONFIG)
    bucket_path = os.getcwd()+"/bucket/"
    workplace_path = os.getcwd()+"/workspace/"
    processed_path = os.getcwd()+"/processed_data/"
    metadata_path = os.getcwd()+"/metadata/"
    samples = os.getcwd()+"/samples/"
    model_factory = factory()
    file_mapper = TreeExplorer()
    logs = Logs(log_file=os.getcwd() + "/Logs/logs.txt")
    db_driver = driver(CONFIG["testdatabase"],logs.GetInstance())
    process_handler = Handler(
        bucket_path,
        workplace_path,
        processed_path,
        metadata_path,
        file_mapper,
        db_driver,
        client.GetInstance(),
        model_factory,
        logs.GetInstance()
    )

 
    def test_backend_service(self):
        print("---------->TESTING BACKEND STATUS")
        result = self.client.Get(CONFIG["service_host"]+CONFIG["endpoints"]["status"])
        self.assertTrue(result["OK"]==1,"Remote service is down")

    def test_database_service(self):
        print("---------->TESTING DATABASE SERVICE + BACKEND")
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
        print("---------->TESTING MAIN PROCESS ++ MONO-TEST ++")
        print("---------->CREATION OF SAMPLE FILES")
        self.file_mapper.ExploreDirectories(self.samples)
        files = self.file_mapper.GetFilesDict()
        self.assertTrue(type(files) is dict,"Failed to copy files")
        for file in files:
            shutil.copy(files[file],self.bucket_path+file)
            shutil.copy(files[file],self.workplace_path+file)
        self.file_mapper.ExploreDirectories(path=self.bucket_path)
        new_files = self.file_mapper.GetFilesDict()
        self.assertTrue(type(new_files) is dict,"Failed to map files")

        print("----------->BASIC POSTPROCESS")
        path  = os.getcwd() + "/samples/20220327 annual-number-of-deaths-by-cause.csv"
        path2 = os.getcwd() + "/processed_data/20220327 annual-number-of-deaths-by-cause.csv.csv"
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
        ds = None
        new_ds=None
        os.remove(path2)

        print("------------>POSTPROCESS IN LOOP")
        self.file_mapper.ExploreDirectories(path=self.workplace_path)
        files = self.file_mapper.GetFilesDict()
        for file in files:
            path = str(files[file])
            ds = pandas.read_csv(path,lineterminator='\n')
            new_ds = ds.dropna()
            top = new_ds.head(0)
            for item in top:
                new_ds.rename(columns={item:str(item).upper()},inplace=True)
            pandas.DataFrame.to_csv(new_ds,self.processed_path+file,index=False)
            ds = None
            new_ds = None
        self.file_mapper.ExploreDirectories(path=self.workplace_path)
        processed_files = self.file_mapper.GetFilesDict()
        self.assertTrue(isinstance(processed_files,dict),"Failed to postprocess files" )

        print("--------->TEST MAIN CLASS MAIN FULL PROCESS")
        asyncio.get_event_loop().run_until_complete(self.process_handler.move_files())
        asyncio.get_event_loop().run_until_complete(self.process_handler.process_files())

        print("+++++++++ CLEANING THE MESS +++++++++++++")
        self.file_mapper.ExploreDirectories(path=self.bucket_path)
        bucked = self.file_mapper.GetFilesDict()
        self.file_mapper.ExploreDirectories(path=self.workplace_path)
        work = self.file_mapper.GetFilesDict()
        self.file_mapper.ExploreDirectories(path=self.processed_path)
        processed = self.file_mapper.GetFilesDict()
        self.file_mapper.ExploreDirectories(path=self.metadata_path)
        metadata_files = self.file_mapper.GetFilesDict()
        self.file_mapper.ExploreDirectories(path=self.samples)
        samples = self.file_mapper.GetFilesDict()
       
        for b in bucked:
            if b in list(samples.keys()):
                os.remove(bucked[b])
        for w in work:
            if w in list(samples.keys()):
                os.remove(work[w])
        for p in processed:
            if p in list(samples.keys()):
                os.remove(processed[p])
        for jm in metadata_files:
            for s in list(samples.keys()):
                if jm == s+".json":
                    os.remove(str(metadata_files[jm]))
        print("+++++++++ TEST COMPLETED +++++++++++++")


if __name__ == "__main__":

    unittest.main()