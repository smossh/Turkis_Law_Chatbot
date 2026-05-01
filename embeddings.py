from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json

embeddings=HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base" )

with open("data.json", "r") as f:
    data = json.load(f)


preprocessed_data = [f"passage: {text}" for text in data]

vector_embeddings = embeddings.embed_documents(preprocessed_data)

docs = [
    Document(
        page_content=f"Soru: {item['question']}\nCevap: {item['answer']}",
        metadata= {
        "madde": item['metadata']['madde']
        }
    )
    for item in data
]

persist_directory = "./chroma_db"
vectorstore= Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=persist_directory,
    collection_name="rag_collection"
)
print(f"Vectorstore created with {len(vector_embeddings)} embeddings.")
