from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from src.config.settings import settings
from src.ingestion.policy_loader import chunk_policy_documents


CHROMA_PERSIST_DIR = "vectorstore/policies"
COLLECTION_NAME = "auto_policy_documents"


def build_policy_vectorstore():
    """
    Build Chroma vector store from policy PDF chunks.
    """
    chunks = chunk_policy_documents()

    texts = [chunk["text"] for chunk in chunks]

    metadatas = [
        {
            "source": chunk["source"],
            "file_path": chunk["file_path"],
            "chunk_id": chunk["chunk_id"],
        }
        for chunk in chunks
    ]

    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )

    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    return vectorstore


def load_policy_vectorstore():
    """
    Load existing Chroma vector store from disk.
    """
    embeddings = OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PERSIST_DIR,
    )

    return vectorstore


def search_policy(query: str, k: int = 5):
    """
    Search policy vector store for relevant policy chunks.
    """
    vectorstore = load_policy_vectorstore()

    results = vectorstore.similarity_search_with_score(query, k=k)

    return results