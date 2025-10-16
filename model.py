import numpy as np
import torch
import torchvision.models as models
from torchvision.models import ResNet50_Weights
import torchvision.transforms as transforms
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image

class ResNet50Embedder:
    """
    Wrapper around a ResNet50 model without the final FC layer.
    """

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        base = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        self.model = torch.nn.Sequential(*list(base.children())[:-1])  # remove final layer
        self.model.eval().to(self.device)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
        ])
        self.sim_thresh = 0.95
    
    def extract_features(self, new_image_paths):
        """
        Accepts image file paths and returns np.array of 
        extracted features as a normalized 1-D numpy vector.
        """
        features_list = []
        for image_path in new_image_paths:
            try:
                img = Image.open(image_path).convert('RGB')
                img_t = self.transform(img).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    features = self.model(img_t).squeeze().cpu().numpy()
                norm = np.linalg.norm(features)
                if norm > 0:
                    features /= norm  # normalize
                features_list.append(features)
            except Exception as e:
                print(f"Skipping {image_path} due to error: {e}")

        if len(features_list) == 0:
            return np.emoty((0,))
        
        features_array = np.stack(features_list)
        return features_array
    
    
    def get_duplicates(self, retrieved_embeddings, image_paths):
        """
        Takes input of dictionary of retrieved embeddings
        Construct feature matrix, and compares images that have similarity
        above a very strict threshold, returns list of tuples of images that
        are duplicates or almost duplicates
        """
        print("Searching for duplicates...")
        
        # no guarantee of ordered keys
        aligned_paths = []
        aligned_features = []
        for p in image_paths:
            emb = retrieved_embeddings.get(p)
            aligned_paths.append(p)
            aligned_features.append(emb)

        if len(aligned_features) < 2:
            print("Not emough embeddings to compare.")
            return []
        
        feature_array = np.stack(aligned_features)
        similarity_matrix = cosine_similarity(feature_array)
        duplicates = []
        num_images = len(aligned_paths)
        for i in range(num_images):
            for j in range(i + 1, num_images):
                if similarity_matrix[i][j] > self.sim_thresh and i != j:
                    duplicates.append((image_paths[i], image_paths[j]))

        if len(duplicates) == 0:
            print("No duplicates found!")
        else:
            print(f"{len(duplicates)} found!")
        
        return duplicates
        