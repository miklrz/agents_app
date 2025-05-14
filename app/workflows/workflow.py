from app.libraries.libs import *

from app.models.llms import setup_groq, setup_lm_studio

from app.database.documents import docs
from app.prompts.prompts import prompt
from app.nodes.state import State

# from app.database.db import db

# from app.nodes.BasicToolNode import BasicToolNode

load_dotenv()

llm = setup_lm_studio()

# retriever = db.as_retriever()
# retriever_tool = create_retriever_tool(
#     retriever,
#     "retrieve_france",
#     "Retrieve documents",
# )
# tools = [retriever_tool]

tavily_search_tool = TavilySearch(max_results=2)


@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human."""
    human_response = interrupt({"query": query})
    return human_response["data"]


tools = [tavily_search_tool, human_assistance]
tool_node = ToolNode(tools=tools)
llm_with_tools = llm.bind_tools(tools)

chain = prompt | llm


def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    assert len(message.tool_calls) <= 1
    return {"messages": message}


memory = MemorySaver()

workflow = StateGraph(state_schema=State)

workflow.add_node(node="chatbot", action=chatbot)
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges(
    "chatbot",
    tools_condition,
)
workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")

workflow.compile(checkpointer=memory)


# def retrieve(state: State) -> None:
#     question = state["question"]
#     documents = retriever.get_relevant_documents(query=question)
#     return {"documents": documents}


# def generate(state: State) -> None:
#     question = state["question"]
#     documents = state["documents"]
#     answer = chain.invoke(
#         input={
#             "question": question,
#             "documents": "\n\n".join([doc.page_content for doc in documents]),
#         }
#     )
#     return {"answer": answer}


# workflow.add_node(node="retrieve", action=retrieve)
# workflow.add_node(node="generate", action=generate)

# workflow.add_edge(start_key=START, end_key="retrieve")
# workflow.add_edge(start_key="retrieve", end_key="generate")
# workflow.add_edge(start_key="generate", end_key=END)
