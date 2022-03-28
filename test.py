import os 
from utils.Filemapper.DirectoryTreeGenerator import TreeExplorer
from utils.utils import get_header_content
from utils.RequestModule.Request import Request
from config.config import config as CONFIG
import unittest


class test_file_mapping(unittest.TestCase):

    client = Request(configuration=CONFIG)
    files_path = os.getcwd()+"/files/"
    workplace_path = os.getcwd()+"/workplace/"
    file_mapper = TreeExplorer()

    def test_service_status(self):
        result = self.client.Get(CONFIG["service_host"]+"status")
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

    def test_get_files_header_content(self):
        self.file_mapper.ExploreDirectories(path=self.files_path)
        files_list=self.file_mapper.GetFilesDict()
        for files in files_list:
            header,content = get_header_content(files_list[files])
            header = header.upper()

            os.remove(files_list[files])

            file = open(self.workplace_path+files,"a")
            file.write(header)
            file.writelines(content)
            file.close()
        
    def 


if __name__ == "__main__":

    unittest.main()