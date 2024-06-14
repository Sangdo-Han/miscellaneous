import argparse
from typing import Optional, List

import chromadb
from chromadb import (Collection,
                      EmbeddingFunction)
from chromadb.utils import embedding_functions

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders.web_base import WebBaseLoader

########################################################
### CONSTANTS ##########################################
## These will be controlled with config in the future ##
########################################################
MAX_INDEX_DIGITS : int = 5
CHUNK_SIZE : int = 250
CHUNK_OVERLAP : int = 0
EMBEDDING_FUNCTION = embedding_functions.\
    SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
) # Embedding function needs to be same as in the service main : easy_rag.py
########################################################

def add_web_doc(collection:Collection,
            web_docs:List[str],
            chunk_size : int = CHUNK_SIZE,
            chunk_overlap : int = CHUNK_OVERLAP,
            idx_offset : int = 0) -> None:

    loader = WebBaseLoader(web_path=web_docs)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                          chunk_overlap=chunk_overlap)

    docs = text_splitter.split_documents(data)
    string_docs = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]
    ids = ["id"+str(idx + idx_offset + 1).zfill(MAX_INDEX_DIGITS) \
           for idx in range(len(docs))]
    
    collection.add(documents=string_docs,
                   ids=ids,
                   metadatas=metadatas)

def get_collection(host:str,
                    port:int,
                    collection_name:str,
                    embedding_function : Optional[EmbeddingFunction] = None) \
                    -> chromadb.Collection:
    
    chroma_client = chromadb.HttpClient(host=host, port=port,)
    collection = chroma_client.get_or_create_collection(
        name=collection_name, 
        embedding_function=embedding_function
    )
    return collection

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--chromadb", type=str, default="localhost:8000"
    )
    parser.add_argument(
        "--collection-name", type=str, default="wiki"
    )
    parser.add_argument(
        "--doc-url", type=str, nargs="*", \
            default="https://sangdo-han.github.io/docs/research/llm/rag.html"
    )
    args = parser.parse_args()

    if ":" not in args.chromadb:
        print("Use default chromadb port: 8000")
        host = args.chromadb
        port = 8000
    else:
        host, port = args.chromadb.split(":")
        port = int(port)

    collection = get_collection(host=host,
                                port=port,
                                collection_name=args.collection_name,
                                embedding_function=EMBEDDING_FUNCTION)
    
    add_web_doc(
        collection=collection,
        web_docs=args.doc_url,
        idx_offset=collection.count()
    )
