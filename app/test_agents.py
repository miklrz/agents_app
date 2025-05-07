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
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools.retriever import create_retriever_tool
from pydantic import BaseModel, Field


load_dotenv()


def setup_groq():
    GROQ_API_KEY = os.getenv("GROQ_KEY")
    model_name = "llama-3.1-8b-instant"
    llm = ChatGroq(temperature=0, model_name=model_name, groq_api_key=GROQ_API_KEY)
    return llm


def setup_lm_studio():
    llm = ChatOpenAI(
        temperature=0.0,
        base_url=f"http://{os.getenv('HOST')}:1234/v1",
        api_key="not-needed",
    )
    return llm


llm = setup_lm_studio()


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
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_france",
    "Retrieve documents",
)

# tools = [retriever_tool]
# llm_with_tools = llm.bind_tools(tools)


class State(TypedDict):
    question: str
    answer: str
    documents: list[Document]


prompt = PromptTemplate(
    input_variables=["question", "documents"],
    template="""
    Use the following documents to answer the question.

    Documents:
    {documents}

    Question: {question}

    Answer:
    """,
)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
)


def retrieve(state: State) -> None:
    question = state["question"]
    documents = retriever.get_relevant_documents(query=question)
    return {"documents": documents}


def generate(state: State) -> None:
    question = state["question"]
    documents = state["documents"]
    answer = chain.invoke(
        input={
            "question": question,
            "documents": "\n\n".join([doc.page_content for doc in documents]),
        }
    )
    return {"answer": answer}


workflow = StateGraph(state_schema=State)

workflow.add_node(node="retrieve", action=retrieve)
workflow.add_node(node="generate", action=generate)

workflow.add_edge(start_key=START, end_key="retrieve")
workflow.add_edge(start_key="retrieve", end_key="generate")
workflow.add_edge(start_key="generate", end_key=END)

workflow.compile()


# from fastapi import APIRouter

# router = APIRouter()

# @router.powt()
# async def get_response():
