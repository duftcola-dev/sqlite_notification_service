import sys

def CheckType(func):

    def CheckTypeFunc(arg):
        
        if type(arg) is str:
            return func(arg)
        else:
            print("CheckType : Function spects url type:string (str)")
            return None

    return CheckTypeFunc


