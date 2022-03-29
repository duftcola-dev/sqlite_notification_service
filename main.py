import os
import config.config
from utils.LogsModule.Logs import Logs
from utils.drivers.db_driver import driver
from utils.Filemapper.DirectoryTreeGenerator import TreeExplorer
from utils.RequestModule.Request import Request
from models.model_factory import factory
from utils.ProcessHandler.Handler import Handler



def main():
    pass
    # result = http_client.Get(CONFIG["service_host"]+"hello")
    # print(result)
    # filemap.ExploreDirectories(os.getcwd() + "/files")
    # print(filemap.GetFilesDict())
    # file_path =  os.getcwd() + "/files/gran_turismo_gt7.csv"
    # file_path2 =  os.getcwd() + "/workspace/gran_turismo_gt7.csv"
    # header,content = get_header(file_path)
    # header = header.upper()
    # os.remove(file_path)
    # file = open(file_path2,"a")
    # file.write(header)
    # file.writelines(content)
    # file.close()


    

   



if __name__ == "__main__":
    
    config.config.init()
    file_path =  os.getcwd() + "/bucket/"
    workspace_path =  os.getcwd() + "/workspace/"
    model_factory = factory()
    logs = Logs(log_file=os.getcwd() + "/Logs/logs.txt")
    db_driver = driver(config.config.CONFIG["database"],logs.GetInstance())
    filemapper = TreeExplorer()
    http_client = Request(config.config.CONFIG,log=logs.GetInstance())
    process_handler = Handler(
    file_path,
    workspace_path,
    filemapper,
    db_driver,
    http_client.GetInstance(),
    model_factory,
    logs.GetInstance()
    )
    main()