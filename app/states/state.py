from app.libraries.libs import TypedDict, Document, Annotated, add_messages


class State(TypedDict):
    # question: str
    # answer: str
    # documents: list[Document]
    messages: Annotated[list, add_messages]
