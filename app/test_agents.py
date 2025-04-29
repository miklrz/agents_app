from typing import Annotated
from typing import Annotated, Literal, Sequence
from dotenv import load_dotenv
import os

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_KEY")
model_name = "llama-3.1-8b-instant"
llm = ChatGroq(temperature=0, model_name=model_name, groq_api_key=GROQ_API_KEY)


model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
hf = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

docs = [
    Document(
        page_content="Paris is the capital of France.",
        metadata={
            "source": "1",
            "url": "https://example.com/france",
            "title": "France Facts",
            "author": "John Doe",
            "date": "2023-10-01",
        },
    ),
    Document(
        page_content="The Eiffel Tower is located in Paris.",
        metadata={
            "source": "2",
            "url": "https://example.com/eiffel",
            "title": "Eiffel Tower Info",
            "author": "Jane Smith",
            "date": "2023-10-02",
        },
    ),
    Document(
        page_content="France is known for its wine and cuisine.",
        metadata={
            "source": "3",
            "url": "https://example.com/french-cuisine",
            "title": "French Culture",
            "author": "Pierre Leclerc",
            "date": "2023-10-03",
        },
    ),
]

db = Chroma.from_documents(
    collection_name="agents_chroma",
    documents=docs,
    embedding=hf,
)

retriever = db.as_retriever()

from langchain.tools.retriever import create_retriever_tool

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_blog_posts",
    "Search and return information about Lilian Weng blog posts on LLM agents, prompt engineering, and adversarial attacks on LLMs.",
)

tools = [retriever_tool]


class State(TypedDict):
    # messages: Annotated[list, add_messages]
    question: str
    answer: str
    documents: list[Document]


def chatbot(state: State):
    answer = {"messages": [llm.invoke(state["question"])]}
    state["answer"] = answer
    return state


def retrieve(state: State) -> None:
    pass
    # question = state["question"]
    # documents = []
    # return {"documents": documents}


def generate(state: State) -> None:
    pass
    # answer = "paris"
    # return {"answer": answer}


workflow = StateGraph(state_schema=State)

workflow.add_node(node="chatbot", action=chatbot)
workflow.add_node(node="retrieve", action=retrieve)
workflow.add_node(node="generate", action=generate)

# workflow.add_edge(start_key=START, end_key="retrieve")
# workflow.add_edge(start_key="retrieve", end_key="generate")
# workflow.add_edge(start_key="generate", end_key=END)

workflow.add_edge(start_key=START, end_key="chatbot")
workflow.add_edge(start_key="chatbot", end_key=END)

workflow.compile()


# from fastapi import APIRouter

# router = APIRouter()

# @router.powt()
# async def get_response():
