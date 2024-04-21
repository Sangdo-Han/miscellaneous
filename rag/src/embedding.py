import os
import sys
from typing import Optional
from langchain.embeddings.huggingface import HuggingFaceEmbeddings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils import singleton

@singleton
def get_huggingface_embedding(model_name="all-MiniLM-L6-v2", **model_kwargs:Optional[dict]):
    embedding_function = HuggingFaceEmbeddings(
            model_name=model_name, model_kwargs=model_kwargs
    )
    return embedding_function
