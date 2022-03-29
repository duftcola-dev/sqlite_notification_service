import datetime
import uuid
class response_model:

    def __init__(self,event_type,event_data) -> None:
        self.event_type = event_type
        self.data = event_data

    def get_schema(self):
        schema = {
            "date" : self.__get_int_date(),
            "uuid" : uuid.uuid4(),
            "event-type" : self.event_type,
            "event-data" : self.data
        }
        return schema

    def __get_int_date(self):
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        day = date.day
        hour = date.hour
        minute = date.minute
        second = date.second

        s=f"{year}{month}{day}{hour}{minute}{second}"
        return int(s)

class factory:

    def __init__(self) -> None:
        pass

    def create_response_model(self,event_type,event_data):
        return response_model(event_type,event_data).get_schema()
         