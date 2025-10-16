import os

class FileHandler:
    def __init__(self):
        self.VALID_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp"]

    def get_image_paths(self, folder):
        paths = []
        for filename in os.listdir(folder):
            ext = os.path.splitext(filename)[1].lower()
            if ext in self.VALID_EXTENSIONS:
                paths.append(os.path.join(folder, filename))
        print(f"Scanned and loaded {len(paths)} images.")
        return paths

    def get_new_files(self, image_paths, redis_client):
        pipe = redis_client.pipeline()
        for path in image_paths:
            pipe.exists(path)
        exists_flags = pipe.execute()
        missing_paths = [path for path, exists in zip(image_paths, exists_flags) if not exists]
        print(f"Found {len(missing_paths)} new images.")
        return missing_paths
    