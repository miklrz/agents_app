from typing import Annotated
from typing import Annotated, Literal, Sequence
from dotenv import load_dotenv
import os

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import tools_condition
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain import hub
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools.retriever import create_retriever_tool
from pydantic import BaseModel, Field
from langchain_core.documents import Document
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
from langchain_openai import OpenAIEmbeddings
