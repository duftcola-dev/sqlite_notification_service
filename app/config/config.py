def init():
    global CONFIG
    CONFIG = {   
        "host":"smtp.gmail.com",
        "port": 465,
        "mail":"duftcoladev@gmail.com",
        "pass":"pythontestservice",
        "database":"mydatabase.db",
        "testdatabase":"testdatabase.db",
        "request":{"json_response":"True"},
        "service_host":"http://localhost:5000/",
        "endpoints":{
            "status":"status",
            "notifications":"notification",
            "alerts":"alert"
        }
    }