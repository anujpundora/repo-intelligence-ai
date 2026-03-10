import chromadb
from chromadb.utils import embedding_functions

# Use default embedding model from Chroma
embedding_function = embedding_functions.DefaultEmbeddingFunction()

# Initialize Chroma client
client = chromadb.PersistentClient(path="./chroma_db")

# Create / get collection
collection = client.get_or_create_collection(
    name="repo_chunks",
    embedding_function=embedding_function
)


def index_chunks(chunks):

    documents = []
    ids = []
    metadatas = []

    for i, chunk in enumerate(chunks):

        documents.append(chunk["content"])
        ids.append(str(i))
        metadatas.append({
            "file_path": chunk["file_path"]
        })

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )


def query_chunks(query, n_results=5):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results