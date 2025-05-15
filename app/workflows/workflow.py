from app.libraries.libs import *

from app.models.llms import setup_groq, setup_lm_studio

from app.database.documents import docs
from app.prompts.prompts import prompt
from app.nodes.state import State


load_dotenv()

llm = setup_groq()


tavily_search_tool = TavilySearch(max_results=2)


def choose_hotel(city: str):
    """Choose a hotel"""
    return f"Suggested hotels in city {city}"


def choose_restaurant(city: str):
    """Choose restaurants"""
    return f"Suggested restaurants in city {city}"


# from langgraph.prebuilt import create_react_agent
# from langgraph_swarm import create_swarm, create_handoff_tool

# transfer_to_hotel_assistant = create_handoff_tool(
#     agent_name="hotel_assistant",
#     description="Transfer user to the hotel-suggesting assistant.",
# )
# transfer_to_restaurant_assistant = create_handoff_tool(
#     agent_name="restaurant_assistant",
#     description="Transfer user to the restaurant-suggesting assistant.",
# )


# hotel_assistant = create_react_agent(
#     model=llm,
#     tools=[choose_hotel, transfer_to_restaurant_assistant],
#     prompt="You are a hotel choosing assistant",
#     name="hotel_assistant",
# )
# restaurant_assistant = create_react_agent(
#     model=llm,
#     tools=[choose_restaurant, transfer_to_hotel_assistant],
#     prompt="You are a restaurant choosing assistant",
#     name="restaurant_assistant",
# )

# supervisor = create_supervisor(
#     agents=[
#         hotel_assistant,
#         restaurant_assistant,
#     ],
#     model=llm,
#     prompt=(
#         "You manage a hotel choosing assistant and a"
#         "restaurant choosing assistant. Assign work to them."
#     ),
# ).compile()

from langgraph.types import Command
from langchain_core.tools import Tool


def hotel_assistant(state: State):
    print(state, type(state))
    if isinstance(state, str):
        location = state
    prompt = hotel_prompt.format(location=location)
    response = hotel_llm.invoke(prompt)
    return Command(
        goto="supervisor",
        update={"messages": [response]},
    )


def restaurant_assistant(state: State):
    response = restaurant_llm.invoke(state["messages"])
    return Command(
        goto="supervisor",
        update={"messages": [response]},
    )


# def supervisor_fn(state: State):
#     response = supervisor_llm.invoke(state["messages"])
#     return Command(goto=response("next_agent"))


supervisor_tools = [
    Tool(
        name="hotel_assistant",
        func=hotel_assistant,
        description="Handles hotel-related queries",
    ),
    Tool(
        name="restaurant_assistant",
        func=restaurant_assistant,
        description="Handles restaurant-related queries",
    ),
]

supervisor_llm = llm.bind_tools(supervisor_tools)


restaurant_tools = [
    Tool(
        name="restaurant_tavily_search_tool",
        func=tavily_search_tool,
        description="Search for restaurants",
    ),
]

restaurant_llm = llm.bind_tools(restaurant_tools)

restaurant_prompt = PromptTemplate(
    input_variables=["location"],
    template="""
        User wants to find restaurants in the following place: {location}.

        Suggest restaurant in this this place.
    """,
)

hotel_tools = [
    Tool(
        name="hotel_tavily_search_tool",
        func=tavily_search_tool,
        description="Search for hotels",
    ),
]

hotel_llm = llm.bind_tools(hotel_tools)

hotel_prompt = PromptTemplate(
    input_variables=["location"],
    template="""
        User wants to find hotels in the following place: {location}.

        Suggest hotels in this this place.
    """,
)


supervisor = create_react_agent(supervisor_llm, supervisor_tools)

workflow = StateGraph(state_schema=State)

workflow.add_node(node="supervisor", action=supervisor)
workflow.add_node(node="hotel_assistant", action=hotel_assistant)
workflow.add_node(node="restaurant_assistant", action=restaurant_assistant)

workflow.add_edge(START, "supervisor")


def route_supervisor(state):
    # Предположим, что последнее сообщение — это ответ LLM с tool_call
    msg = state["messages"][-1]
    print(msg)
    print(msg.tool_calls)
    if msg.tool_calls:
        tool_name = msg.tool_calls[0]["name"]
        if tool_name == "route_to_hotel":
            return "hotel_assistant"
        elif tool_name == "route_to_restaurant":
            return "restaurant_assistant"
    return END


workflow.add_conditional_edges(
    "supervisor",
    route_supervisor,
    {
        "hotel_assistant": "hotel_assistant",
        "restaurant_assistant": "restaurant_assistant",
        END: END,
    },
)

# Циклы — после ассистентов возвращаемся к supervisor
workflow.add_edge("hotel_assistant", "supervisor")
workflow.add_edge("restaurant_assistant", "supervisor")

workflow.compile()
# supervisor = workflow.compile()


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
