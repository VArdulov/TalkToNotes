# from llama_index.prompts import PromptTemplate
from llama_index.llms import HuggingFaceLLM
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
hf_chat_model_name = "meta-llama/Llama-2-7b-chat-hf"
if __name__ == "__main__":
    # document_reader = SimpleDirectoryReader(processed_organized_data, recursive=True, filename_as_id=True)
    # print(f"Loading documents from {processed_organized_data}!")
    # documents = document_reader.load_data()
    # print(f"Loaded {len(documents)} documents")  # was averaging about 15 secs

    llm = HuggingFaceLLM(
        # generate_kwargs={"do_sample"},
        # system_prompt=system_prompt,
        # query_wrapper_prompt=query_wrapper_prompt,
        # tokenizer_name="StabilityAI/stablelm-tuned-alpha-3b",
        model_name=hf_chat_model_name,
        # device_map="auto",
        # stopping_ids=[50278, 50279, 50277, 1, 0],
        # tokenizer_kwargs={"max_length": 4096},
    )

    embed_model = HuggingFaceEmbedding(model_name=hf_embed_model_name)
    service_context = ServiceContext.from_defaults(
        llm=llm,  # Since we're just creating the vector store, no llm is necessary for interacting/answering now
        embed_model=embed_model  # Tells llama_index to use our embed model
    )
    # set_global_service_context(service_context)
    storage_context = StorageContext.from_defaults(persist_dir="example_index")
    index = load_index_from_storage(storage_context=storage_context, service_context=service_context)

    query_engine = index.as_query_engine()
    response = query_engine.query("What is an eigenvalue?")
    print(response.response)



