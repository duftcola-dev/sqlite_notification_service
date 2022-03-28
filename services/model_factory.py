import datetime
import uuid
class response_model:

    def __init__(self,event_type,event_data) -> None:
        self.event_type = event_type
        self.data = event_data

    def get_schema(self):
        schema = {
            "date" : datetime.datetime.now(),
            "UUID" : uuid.uuid4(),
            "event-type" : self.event_type,
            "event-data" : self.data
        }
        return schema

class factory:

    def __init__(self) -> None:
        pass

    def create_request_model(self,event_type,event_data):
        return response_model(event_type,event_data)
         