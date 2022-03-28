import os
from config.config import config as CONFIG
from utils.LogsModule.Logs import Logs
from utils.drivers.db_driver import driver
from utils.utils import to_upercase,get_header
from utils.Filemapper.DirectoryTreeGenerator import TreeExplorer
from utils.RequestModule.Request import Request

logs = Logs(log_file=os.getcwd() + "/Logs/logs.txt")
db_driver = driver(CONFIG["database"],logs.GetInstance())
filemap = TreeExplorer()
http_client = Request(CONFIG,log=logs.GetInstance())

def main():
    result = http_client.Get(CONFIG["service_host"]+"hello")
    print(result)
    # filemap.ExploreDirectories(os.getcwd() + "/files")
    # print(filemap.GetFilesDict())
    # file_path =  os.getcwd() + "/files/gran_turismo_gt7.csv"
    # file_path2 =  os.getcwd() + "/workplace/gran_turismo_gt7.csv"
    # header,content = get_header(file_path)
    # header = header.upper()
    # os.remove(file_path)
    # file = open(file_path2,"a")
    # file.write(header)
    # file.writelines(content)
    # file.close()


    

   



if __name__ == "__main__":

    main()