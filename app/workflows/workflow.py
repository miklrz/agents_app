from app.libraries.libs import *
from app.models.llms import setup_groq, setup_lm_studio
from app.nodes.state import State
from app.prompts.agentic_prompts import HOTEL_PROMPT


load_dotenv()

llm = setup_groq()

tavily_search_tool = TavilySearch(max_results=2)


def hotel_assistant(state: State):
    question = state["messages"][-1]
    prompt = HOTEL_PROMPT.format(question=question)
    response = llm.invoke(prompt)
    return {"hotel": response}


def restaurant_assistant(state: State):
    pass


workflow = StateGraph(state_schema=State)

workflow.add_node(node="hotel_assistant", action=hotel_assistant)
workflow.add_node(node="restaurant_assistant", action=restaurant_assistant)

workflow.add_edge(START, "hotel_assistant")
workflow.add_edge("restaurant_assistant", END)

workflow.compile()
