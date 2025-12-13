"""
Data Ingestion Script - Run this independently to ingest data into ChromaDB.
This script loads documents from URLs, splits them, and stores embeddings in ChromaDB with caching.

Usage: uv run python ingestion.py
"""
from dotenv import load_dotenv

load_dotenv()
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.embeddings import CacheBackedEmbeddings
from langchain_classic.storage import LocalFileStore
import os

# Configuration
DATA_DIRECTORY = "./.chroma"
CACHE_DIRECTORY = "./.cache/embeddings"
COLLECTION_NAME = "rag-chroma"

urls = [
    # Model Context Protocol (MCP) 
    "https://www.anthropic.com/news/model-context-protocol",
    "https://modelcontextprotocol.io/introduction",
    "https://en.wikipedia.org/wiki/Model_Context_Protocol",
    
    # LLM Quantization and Fine-tuning 
    "https://www.symbl.ai/developers/blog/a-guide-to-quantization-in-llms",
    "https://www.datacamp.com/tutorial/fine-tuning-large-language-models",
    "https://arxiv.org/abs/2403.03775",
    
    # LangChain and LangChain Deep Agents 
    "https://docs.langchain.com/oss/python/langchain/overview",
    "https://docs.langchain.com/oss/python/langchain/agents",
    "https://docs.langchain.com/oss/python/langchain/models",
    "https://docs.langchain.com/oss/python/langchain/tools",
    "https://docs.langchain.com/oss/python/deepagents/overview",
    "https://docs.langchain.com/oss/python/deepagents/harness"
]


def ingest_data():
    """Load documents, split them, and create vector store with cached embeddings."""
    print("Starting data ingestion...")
    
    # Load documents from URLs
    print(f"Loading {len(urls)} URLs...")
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
    print(f"Loaded {len(docs_list)} documents")
    
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)
    print(f"Split into {len(doc_splits)} chunks")
    
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
    
    # Create or skip vector store
    if os.path.exists(DATA_DIRECTORY):
        print(f"Vector store already exists at {DATA_DIRECTORY}")
        print("Delete the directory to re-ingest data")
    else:
        print(f"Creating vector store at {DATA_DIRECTORY}...")
        vectorstore = Chroma.from_documents(
            documents=doc_splits,
            collection_name=COLLECTION_NAME,
            embedding=cached_embeddings,
            persist_directory=DATA_DIRECTORY,
        )
        print("✅ Data ingestion completed successfully!")
        print(f"📁 Vector store: {DATA_DIRECTORY}")
        print(f"💾 Cache: {CACHE_DIRECTORY}")


if __name__ == "__main__":
    ingest_data()
