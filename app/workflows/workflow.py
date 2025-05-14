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


def choose_flight(from_airport: str, to_airport: str):
    """Choose a flight"""
    # return f"Successfully booked a flight from {from_airport} to {to_airport}."
    pass


def choose_hotel(hotel_name: str):
    """Choose a hotel"""
    # return f"Successfully booked a stay at {hotel_name}."
    pass


def choose_restaurant(from_airport: str, to_airport: str):
    """Choose restaurants"""
    # return f"Successfully booked a flight from {from_airport} to {to_airport}."
    pass


def choose_entertainments(from_airport: str, to_airport: str):
    """Choose entertainments"""
    # return f"Successfully booked a flight from {from_airport} to {to_airport}."
    pass


flight_assistant = create_react_agent(
    model=llm,
    tools=[choose_flight],
    prompt="You are a flight choosing assistant",
    name="flight_assistant",
)

hotel_assistant = create_react_agent(
    model=llm,
    tools=[choose_hotel],
    prompt="You are a hotel choosing assistant",
    name="hotel_assistant",
)
restaurant_assistant = create_react_agent(
    model=llm,
    tools=[choose_restaurant],
    prompt="You are a restaurant choosing assistant",
    name="restaurant_assistant",
)

entertainments_assistant = create_react_agent(
    model=llm,
    tools=[choose_entertainments],
    prompt="You are a entertainments choosing assistant",
    name="entertainments_assistant",
)

supervisor = create_supervisor(
    agents=[
        flight_assistant,
        hotel_assistant,
        restaurant_assistant,
        entertainments_assistant,
    ],
    model=llm,
    prompt=(
        "You manage a flight choosing assistant, "
        "hotel choosing assistant, restaurant choosing assistant and a"
        "entertainments choosing assistant. Assign work to them."
    ),
).compile()


# @tool
# def human_assistance(query: str) -> str:
#     """Request assistance from a human."""
#     human_response = interrupt({"query": query})
#     return human_response["data"]


# tools = [tavily_search_tool, human_assistance]
# tool_node = ToolNode(tools=tools)
# llm_with_tools = llm.bind_tools(tools)

# chain = prompt | llm


# def chatbot(state: State):
#     message = llm_with_tools.invoke(state["messages"])
#     assert len(message.tool_calls) <= 1
#     return {"messages": message}


# memory = MemorySaver()

# workflow = StateGraph(state_schema=State)

# workflow.add_node(node="chatbot", action=chatbot)
# workflow.add_node("tools", tool_node)

# workflow.add_conditional_edges(
#     "chatbot",
#     tools_condition,
# )
# workflow.add_edge("tools", "chatbot")
# workflow.add_edge(START, "chatbot")

# workflow.compile(checkpointer=memory)
