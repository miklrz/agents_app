from langchain.prompts import PromptTemplate

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
