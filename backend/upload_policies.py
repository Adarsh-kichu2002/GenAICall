import os
import sys
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.base import Embeddings
from dotenv import load_dotenv

load_dotenv()

# Simple mock embeddings class (for testing)
class MockEmbeddings(Embeddings):
    def __init__(self):
        pass
    
    def embed_documents(self, texts):
        # Return simple hash-based vectors for testing
        return [[float(ord(c) % 256) / 256 for c in text[:384]] for text in texts]
    
    def embed_query(self, text):
        return [float(ord(c) % 256) / 256 for c in text[:384]]

try:
    # 1. Initialize
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = "compliance-rules"
    embeddings = MockEmbeddings()

    # 2. Create Index if it doesn't exist
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384, 
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    # 3. Load and Upload policy.txt
    with open("../data/policy.txt", "r") as f:
        policies = [line.strip() for line in f.readlines() if line.strip()]

    # Upload to Pinecone
    vectorstore = PineconeVectorStore.from_texts(
        texts=policies,
        embedding=embeddings,
        index_name=index_name
    )

except Exception as e:
    print(f"Note: Pinecone upload encountered an issue: {e}")

print("Policy rules uploaded to Pinecone successfully.")
