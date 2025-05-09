from app.libraries.libs import Chroma
from app.database.documents import docs
from app.models.embeddings import hf

db = Chroma.from_documents(
    collection_name="agents_chroma",
    documents=docs,
    embedding=hf,
)
