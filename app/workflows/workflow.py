from app.libraries.libs import *

from app.models.llms import setup_groq, setup_lm_studio
from app.nodes.BasicToolNode import BasicToolNode
from app.database.documents import docs
from app.prompts.prompts import prompt
from app.states.state import State
from app.database.db import db

load_dotenv()

llm = setup_groq()

retriever = db.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_france",
    "Retrieve documents",
)

# tools = [retriever_tool]


tavily_search_tool = TavilySearch(max_results=2)
tools = [tavily_search_tool]

tool_node = BasicToolNode(tools=[tavily_search_tool])
llm_with_tools = llm.bind_tools(tools)

chain = LLMChain(
    llm=llm,
    prompt=prompt,
)


def chatbot(state: State):
    answer = {"messages": [llm.invoke(state["question"])]}
    state["answer"] = answer
    return state


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


def route_tools(
    state: State,
):
    pass
    # if isinstance(state, list):
    #     ai_message = state[-1]
    # elif messages := state.get("messages", []):
    #     ai_message = messages[-1]
    # else:
    #     raise ValueError(f"No messages found in input state to tool_edge: {state}")
    # if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
    #     return "tools"
    # return END


workflow = StateGraph(state_schema=State)

# workflow.add_node(node="retrieve", action=retrieve)
# workflow.add_node(node="generate", action=generate)

workflow.add_node(node="chatbot", action=chatbot)
workflow.add_node("tools", tool_node)

workflow.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", END: END},
)
workflow.add_edge("tools", "chatbot")
workflow.add_edge(START, "chatbot")

# workflow.add_edge(start_key=START, end_key="retrieve")
# workflow.add_edge(start_key="retrieve", end_key="generate")
# workflow.add_edge(start_key="generate", end_key=END)

workflow.compile()
