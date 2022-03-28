
def to_upercase(string:str):

    return string.upper()

def get_header_content(path:str):

    file = open(path,"r")
    line = file.readline()
    content =file.readlines()[1:]
    file.close()
    return line,content
