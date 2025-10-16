# dedup-pic

A mini-utility program that finds and separates duplicate and near-duplicate images on local directories using ResNet50 embeddings, and Redis data volume as a cache.

## Features
- Extracts image embeddings using a pretrained ResNet50 (final FC removed).
- Normalizes embeddings and compares with cosine similarity.
- Caches embeddings in Redis to avoid reprocessing, and retrieve embeddings faster.
- Moves detected duplicate images to a `duplicates/` folder.

## Requirements
- Python 3.8+
- Redis server (local or remote)
- Python packages:
  - torch
  - torchvision
  - scikit-learn
  - pillow
  - redis
  - python-dotenv
- Docker engine (optional)

## Sample Dataset Images
Source: Kaggle Images Dataset - [here](https://www.kaggle.com/datasets/pavansanagapati/images-dataset)

## Configurations

Create a .env file in the project root with Redis connection details:

```
REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
REDIS_DB=
```
## Important files

> `main.py` — entrypoint and workflow
> 
> `model.py` — embedding extraction and duplicate detection
> 
> `file_handler.py` — scanning folders and detecting new files
> 
> `redis_client.py` — Redis cache wrapper


## My motivation for creating this
- This was a side project I undertook to understand how caching in Redis works.
- I wanted to use the vector database of Redis, but that is only accessible to Redis Cloud users, and I wanted a local, modular implementation of this program. 
- For a long time, I have had a lot of personal images of outings, food, landspaces which were duplicated over the years and manually sorting by their sizes were not effective. When I came across Redis, it was the best choice for fast retrieval of embeddings and reducing the recomputation.
- I chose ResNet50 embeddings as I have worked with its architecture and it would take me the least amount of time to implement a duplicate finder.

## Some things I will be working on
- Including a `requirements.txt` file
- Displaying the duplicates on a UI, with the option to discard/select the ones to keep.
- Implement Image Hashing (pHash - perceptional hashing) which is computationally way faster.
- Removing the double `for` loop for comparing embeddings because nobody wants O(n^2).
