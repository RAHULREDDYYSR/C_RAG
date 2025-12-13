"""
Retriever module - Loads existing Chroma vector store with cached embeddings.
Run ingestion.py first to create the vector store and cache.
"""
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore

# Configuration
DATA_DIRECTORY = "./.chroma"
CACHE_DIRECTORY = "./.cache/embeddings"
COLLECTION_NAME = "rag-chroma"

# Create cache store for embeddings
fs = LocalFileStore(CACHE_DIRECTORY)

# Create underlying embeddings model
underlying_embeddings = OpenAIEmbeddings()

# Wrap embeddings with cache
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    fs,
    namespace=underlying_embeddings.model
)

# Initialize retriever from existing vector store
retriever = Chroma(
    collection_name=COLLECTION_NAME,
    persist_directory=DATA_DIRECTORY,
    embedding_function=cached_embeddings,
).as_retriever()
