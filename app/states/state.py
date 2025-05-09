from app.libraries.libs import TypedDict, Document


class State(TypedDict):
    question: str
    answer: str
    documents: list[Document]
