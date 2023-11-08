# from llama_index.prompts import PromptTemplate
from llama_index.llms import LlamaCPP
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import (
    ServiceContext,
    StorageContext,
    SimpleDirectoryReader,
    load_index_from_storage,
    set_global_service_context
)

system_prompt = """
"""

# This will wrap the default prompts that are internal to llama-index
# query_wrapper_prompt = PromptTemplate("<|USER|>{query_str}<|ASSISTANT|>")

processed_organized_data = "../processed_data/"
hf_embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
# hf_chat_model_name =  "meta-llama/Llama-2-7b-chat-hf"  # Too large to run locally
llama_cpp_model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/blob/main/llama-2-7b-chat.Q5_K_M.gguf"
llama_cpp_model_path = "models/llama-2-7b-chat.Q5_K_M.gguf"
if __name__ == "__main__":
    embed_model = HuggingFaceEmbedding(model_name=hf_embed_model_name)
    llm = LlamaCPP(
        model_path=llama_cpp_model_path,
        temperature=0,
        max_new_tokens=256,
        context_window=3900,
        model_kwargs={"n_gpu_layers": 0},
        generate_kwargs={},
        # messages_to_prompt=None,
        # completion_to_prompt=None,
        verbose=True
    )
    service_context = ServiceContext.from_defaults(
        llm=llm,  # Since we're just creating the vector store, no llm is necessary for interacting/answering now
        embed_model=embed_model,  # Tells llama_index to use our embed model
    )

    storage_context = StorageContext.from_defaults(persist_dir="example_index")
    index = load_index_from_storage(storage_context=storage_context, service_context=service_context)

    query_engine = index.as_query_engine()
    response = query_engine.query("What are eigenvalues and eigenvectors? Please cite the lectures that cover them", )
    print(response.response)



