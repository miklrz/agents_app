from langchain_core.documents import Document

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
