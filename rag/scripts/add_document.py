import argparse
from typing import Optional, List

import chromadb
from chromadb import Collection, EmbeddingFunction
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions

#################
### CONSTANTS ###
#################
MAX_INDEX_DIGITS = 5
EMBEDDING_FUNCTION = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
) # This needs to be same as in the main : RAG

def add_web_doc(collection:Collection,
            web_docs:List[str],
            chunk_size : int = 250,
            chunk_overlap : int = 50,
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
        "--host", type=str, default="localhost"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=8000
    )
    parser.add_argument(
        "--collection-name", "-n", type=str, default="wiki"
    )
    parser.add_argument(
        "--web-path", "-w", type=str, nargs="*", \
            default="https://sangdo-han.github.io/docs/research/llm/rag.html"
    )

    args = parser.parse_args()

    collection = get_collection(host=args.host,
                                port=args.port,
                                collection_name=args.collection_name,
                                embedding_function=EMBEDDING_FUNCTION)
    
    assert args.web_path, ValueError("Needs at least one web url")
    add_web_doc(
        collection=collection,
        web_docs=args.web_path,
        idx_offset=collection.count()
    )
