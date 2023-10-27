from os import environ
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from time import time

processed_organized_data = "../processed_data/"
document_reader = SimpleDirectoryReader(processed_organized_data, recursive=True, filename_as_id=True)
print("Loading document!")
s_time = time()
documents = document_reader.load_data()
e_time = time()
time_minutes = (e_time - s_time)//60
time_seconds = int((e_time - s_time))%60
print(f"Loaded {len(documents)} in {time_minutes:02}m {time_seconds:02}s")

# print("Creating Vector Store Index using OpenAI API and gpt-3.5")
# s_time = time()
# index = VectorStoreIndex.from_documents(documents)
# e_time = time()
# time_minutes = (e_time - s_time)//60
# time_seconds = int((e_time - s_time))%60
# print(f"Indexing is complete in {time_minutes:02}m {time_seconds:02}s")

# query_engine = index.as_query_engine()
# response = query_engine.query("What are eigenvalues?")

# print(response)