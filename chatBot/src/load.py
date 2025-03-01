import ollama
import chromadb
import fitz

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="documents")

def embed_text(text):
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]

def add_document(id, text):
    embedding = embed_text(text)
    collection.add(ids=[id], embeddings=[embedding], metadatas=[{"text": text}])

def load_pdf_and_store(file_path):
    doc = fitz.open(file_path)
    
    for page_num, page in enumerate(doc):
        text = page.get_text("text").strip()
        
        paragraphs = text.split("\n\n")
        
        for i, paragraph in enumerate(paragraphs):
            clean_paragraph = paragraph.strip()
            if clean_paragraph:
                doc_id = f"page_{page_num}_para_{i}"
                add_document(doc_id, clean_paragraph)

("belge.pdf")

print("Başarılı!")
