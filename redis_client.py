from dotenv import load_dotenv
import pickle
import redis
import os

try:
    load_dotenv()
except Exception:
    print("Please create an environment file.")
    pass

class RedisClient:
    def __init__(self):
        """
        Initialize a Redis client from environment variables.
        """ 
        host = os.environ.get("REDIS_HOST")
        port = int(os.environ.get("REDIS_PORT", 6379))
        password = os.environ.get("REDIS_PASSWORD")
        db = int(os.environ.get("REDIS_DB", 0))

        self.client = redis.Redis(host=host,port=port,password=password,db=db)
    
    def set_cache(self, new_image_list, feature_array):
        """
        Sets the cache in the Redis client for the features extracted 
        from new images. Returns a boolean, True if all ok, False if not.
        """
        try:
            for path, emb in zip(new_image_list, feature_array):
                self.client.set(path, pickle.dumps(emb))
            return True
        except Exception as e:
            print(e)
            return False
        
    def get_cache(self, old_image_paths):
        """
        Retrieves embeddings of old images.
        Returns a dictionary of file paths mapped against their unpickled embeddings.
        """
        restored = {}
        for path in old_image_paths:
            data = self.client.get(path)
            if data is not None:
                emb = pickle.loads(data)
                restored[path] = emb
        return restored
