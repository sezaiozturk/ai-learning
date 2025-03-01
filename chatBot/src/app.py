import ollama
import chromadb


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="documents")

def embed_text(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]

def retrieve_relevant_context(user_input, top_k=3):
    query_embedding = embed_text(user_input)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    
    relevant_context = " ".join([doc["text"] for doc in results["metadatas"][0]])
    
    return relevant_context


while True:
    user_input = input("Sen: ")
    
    if user_input.lower() in ["çık"]:
        print("Chatbot kapatılıyor.")
        break

    context = retrieve_relevant_context(user_input)

    prompt = f"Kullanıcı sorusu: {user_input}\n\nBağlam:\n{context}\n\nYanıt:"
    response = ollama.chat(model="deepseek-r1", messages=[{"role": "user", "content": prompt}])

    print("\nBot:", response["message"]["content"])
