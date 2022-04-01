import json
import redis

class driver:

    def __init__(self) -> None:
        self.base = "notifications"
        self.redis = redis.Redis(host="redis",port=6379,decode_responses=True,password="root")

    async def set_data(self,data:dict)->bool:
        id = data["uuid"]
        valid_data = json.dumps(data)
        self.redis.mset({id:valid_data})
        self.redis.save()
    
    def get_data(self,id):
        return self.redis.get(id)

    def get_all(self):
        return self.redis.keys()