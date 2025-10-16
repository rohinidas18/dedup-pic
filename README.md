# dedup-pic

A mini-utility program to find and separate duplicate and near-duplicate images on local directories using ResNet50 embeddings, and Redis as a cache.

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
- Docker engine (optional - to maintain a redis data volume)

Install with:
```sh
pip install torch torchvision scikit-learn pillow redis python-dotenv
```sh

## Configurations

Create a .env file in the project root with Redis connection details:

REDIS_HOST=
REDIS_PORT=
REDIS_PASSWORD=
REDIS_DB=