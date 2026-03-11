import chromadb
from chromadb.utils import embedding_functions
from app.agents.query_agent import generate_queries
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
    print("Indexing", len(documents), "chunks into Chroma")

def query_chunks(query, n_results=5):

    queries = [
        query,
        query + " login register session",
        "flask authentication login register session user"
    ]

    all_docs = []

    for q in queries:
        results = collection.query(
            query_texts=[q],
            n_results=n_results
        )

        docs = results.get("documents", [[]])[0]
        all_docs.extend(docs)

    return list(set(all_docs))