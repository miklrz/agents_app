from app.libraries.libs import Chroma
from app.database.documents import docs
from app.models.embeddings import setup_embedding_hf, setup_embedding_lm_studio

# embedding = setup_embedding_lm_studio()
embedding = setup_embedding_hf()

db = Chroma.from_documents(
    collection_name="agents_chroma",
    documents=docs,
    embedding=embedding,
)
