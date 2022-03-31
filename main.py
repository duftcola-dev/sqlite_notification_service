from cgitb import handler
import os
import config.config
import asyncio
from utils.LogsModule.Logs import Logs
from utils.drivers.db_driver import driver
from utils.Filemapper.DirectoryTreeGenerator import TreeExplorer
from utils.RequestModule.Request import Request
from models.model_factory import factory
from utils.ProcessHandler.Handler import Handler


def main(handler:Handler):
    
    asyncio.get_event_loop().run_until_complete(handler.move_files())
    asyncio.get_event_loop().run_until_complete(handler.process_files())


    

   



if __name__ == "__main__":
    
    config.config.init()
    global CONFIG 
    CONFIG = config.config.CONFIG
    file_path =  os.getcwd() + "/bucket/"
    workspace_path =  os.getcwd() + "/workspace/"
    processed_path =  os.getcwd() + "/processed_data/"
    metadata_path = os.getcwd() + "/metadata/"
    model_factory = factory()
    logs = Logs(log_file=os.getcwd() + "/Logs/logs.txt")
    db_driver = driver(CONFIG["database"],logs.GetInstance())
    filemapper = TreeExplorer()
    http_client = Request(CONFIG,log=logs.GetInstance())

    process_handler = Handler(
    file_path,
    workspace_path,
    processed_path,
    metadata_path,
    filemapper,
    db_driver,
    http_client.GetInstance(),
    model_factory,
    logs.GetInstance()
    )
    main(process_handler)