
"""
This script presents an example of how to run a local embedding model for the purposes of constructing a vector store.
Specifically, since I  am experimenting on an old Intel MacBook Pro, the `sentence-transformers/all-MiniLM-L6-v2'
was chosen since it and the vectors it produces are very small. There's most definitely a trade-off in performance
though.

If you choose to use the default OpenAI model, you need to go and create and API key and then set it as part of your
environmental variables. One way to do that is from your terminal where you plan on running this script from needs to
run the command

export OPENAI_API_KEY=sk-###...###

Or this same line can be added to you shell rc file (e.g. .bashrc or .zshrc)

Or you can do it programmatically inside of this script as:
from os import environ
environ["OPENAI_API_KEY"] = "sk-###...###"

However, just keep in mind that even with this marginally small number of documents (1048 as of writing) managed to hit
the OpenAI basic API rate limit even before the index was fully stored.

To-do: Move this example/write up to an .ipynb for easier collaboration/experimentation in the future
"""

# llama_index imports
from llama_index.embeddings import HuggingFaceEmbedding  # This allows us to download a model from HF hub and use it
from llama_index import (
    SimpleDirectoryReader,  # This is used to load the data into a Document array
    ServiceContext,  # This provides the context of which model and what parameters to if anything isn't default
    VectorStoreIndex  # This is going to construct the actual VectorStore and allow us to save it locally
)

# I want to be able to time how long different processes take
from time import time

# This is where the data is stored and which model to grab from hugging face
processed_organized_data = "../processed_data/"
hf_embed_model_name = "sentence-transformers/all-MiniLM-L6-v2"
if __name__ == "__main__":
    document_reader = SimpleDirectoryReader(processed_organized_data, recursive=True, filename_as_id=True)
    print(f"Loading documents from {processed_organized_data}!")

    s_time = time()
    documents = document_reader.load_data()
    e_time = time()

    time_minutes = (e_time - s_time)//60
    time_seconds = int((e_time - s_time))%60

    print(f"Loaded {len(documents)} in {time_minutes:02}m {time_seconds:02}s")  # was averaging about 15 secs

    # This is the part that sets up the custom embedding model which provides the vectors to the vector store
    embed_model = HuggingFaceEmbedding(model_name=hf_embed_model_name)
    service_context = ServiceContext.from_defaults(
        llm=None,  # Since we're just creating the vector store, no llm is necessary for interacting/answering now
        embed_model=embed_model  # Tells llama_index to use our embed model
    )

    print("Creating Vector Store Index using OpenAI API and gpt-3.5")
    s_time = time()
    index = VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
        show_progress=True
    )
    e_time = time()
    time_minutes = (e_time - s_time)//60
    time_seconds = int((e_time - s_time))%60
    print(f"Indexing is complete in {time_minutes:02}m {time_seconds:02}s")

    print("Saving VectorStoreIndex locally!")
    index.storage_context.persist("example_index")

    # Run a small example query, no answer is currently expected
    query_engine = index.as_query_engine()
    response = query_engine.query("What are eigenvalues?")
    print(response.response)