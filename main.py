from redis_client import RedisClient
from file_handler import FileHandler
from model import ResNet50Embedder
import os, shutil

class Main:
    def __init__(self):
        # Initialize Redis Client
        self.redis_client = RedisClient()
        # Initialize File Handler
        self.file_handler = FileHandler()
        # Initialize Model Wrapper
        self.resnet_wrap = ResNet50Embedder()

    def run(self):
        img_dir = input("Please enter the image directory: ")
        image_paths = self.file_handler.get_image_paths(img_dir)
        new_images = self.file_handler.get_new_files(image_paths, self.redis_client.client)

        if new_images:
            print("Extracting embeddings of new images...")
            features_array = self.resnet_wrap.extract_features(new_images)
            print("Finished extracted features for all images!")
            print("Shape of features array:", features_array.shape)

            if self.redis_client.set_cache(new_images, features_array):
                print("Embeddings cached successfully!")
            else:
                print("An error occured while setting the cache. Please retry!")

        print("Retrieving all embeddings...")
        retrieved_emb = self.redis_client.get_cache(image_paths)
        duplicates = self.resnet_wrap.get_duplicates(retrieved_emb, image_paths)
        if duplicates:
            print("Launching Image Picker...")
            try:
                print("Moving duplicate pairs to 'duplicates/' folder...")
                duplicates_dir = os.path.join(os.path.dirname(img_dir), "duplicates")
                os.makedirs(duplicates_dir, exist_ok=True)
                moved = set()
                for pair in duplicates:
                    for img_path in pair:
                        if img_path not in moved:
                            shutil.move(img_path, duplicates_dir)
                            moved.add(img_path)
            except Exception as e:
                print("Could not launch Image Picker. Falling back to console output.")
                for dup in duplicates:
                    print(dup)


if __name__ == "__main__":
    print("Running Duplicate Finder...")
    app = Main()
    app.run()