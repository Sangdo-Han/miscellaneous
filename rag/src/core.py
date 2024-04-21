import os
import sys
from typing import Optional

from chromadb import HttpClient
from langchain import hub
from langchain.vectorstores.chroma import Chroma

from langchain_community.llms.llamacpp import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from src.embedding import get_huggingface_embedding

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def set_prompt_from_template(template:Optional[str]=None):
    if template is not None:
        prompt = PromptTemplate.from_template(template)
    else:
        prompt = hub.pull("rlm/rag-prompt")
    return prompt

def get_llama_cpp(model_path, **kwargs):
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    llm =LlamaCpp(
        model_path=model_path,
        temperature=kwargs.get("temperature", 0.75),
        max_tokens=kwargs.get("max_token",2000),
        top_p=kwargs.get("top_p", 1),
        callback_manager=callback_manager,
        n_ctx=2048,
        verbose=True,  # Verbose is required to pass to the callback manager
    )
    return llm

def get_langchain(
        llama_cpp_path : str = os.path.join(base_path,
            "lib/llm/llama-2-7b-chat.Q2_K.gguf"),
        hosts : str = 'localhost:8000',
        index_name : str = 'wiki',
        template : Optional[str] = None,
    ):

    prompt = set_prompt_from_template(template=template)
    llm = get_llama_cpp(model_path=llama_cpp_path)

    host, port =hosts.rsplit(":",1)
    client = HttpClient(
        host="localhost",
        port=int(port),
    )
    vector_store = Chroma(
        collection_name=index_name,
        client=client,
        embedding_function=get_huggingface_embedding()
    )
    retriever = vector_store.as_retriever()

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

if __name__ == "__main__":
    x = get_langchain()