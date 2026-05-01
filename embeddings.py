from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import json

embeddings=HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base" )

data = []
with open("data.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue  
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f"Hata! {i}. satır okunamadı. İçerik: {line[:50]}...")
            print(f"Hata detayı: {e}")

docs = [
    Document(
        
        page_content=f"passage: Soru: {item['question']}\nCevap: {item['answer']}",
        metadata= {
            "idx": item.get("index"),
            "madde": item.get("metadata", {}).get("Madde", None)
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
print(f"Vectorstore created with {len(vectorstore._collection.documents)} embeddings.")
