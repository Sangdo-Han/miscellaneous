# RAG

<p align="center">
 <img src="https://sangdo-han.github.io/docs/research/llm/rag_architecture.png">
</p>

1. 
2. `save_context.py` using chromadb, data will be stored in ./vector_store


## Installation

```bash
git clone https://github.com/Sangdo-Han/research
cd RAG
sh download_model.sh # llama-cpp pretrian
pip install -r requirements.txt
```

## service RAG chat

```bash
python main.py --port
```

## License
In this project, we will mainly use 4 open-sources : service-framework, llm, vectorstore and frontend.   
For llm, we used pretrained llama-2 (cpp) model from [huggingface/TheBloke](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF). Under the commercial-open license from Meta and TheBloke, currently academic and commercial-using is fine, however, it could be changed in the future. For the vectorstore, we used chromadb, which is open-source vector database under Apache 2.0 license. For the framework, we used langchain, which is open-source framework under MIT license. Finally, for the frontend, streamlit is used under Apache 2.0 license.

