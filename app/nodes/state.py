from app.libraries.libs import TypedDict, Document, Annotated, add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    hotel: str
