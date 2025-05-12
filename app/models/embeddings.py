from app.libraries.libs import HuggingFaceEmbeddings, OpenAIEmbeddings, os


def setup_embedding_hf():
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {"device": "cpu"}
    encode_kwargs = {"normalize_embeddings": False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )
    return hf


def setup_embedding_lm_studio():
    model = OpenAIEmbeddings(
        model="text-embedding-intfloat-multilingual-e5-large-instruct",
        base_url=f"http://{os.getenv('HOST')}:1234/v1",
        check_embedding_ctx_length=False,
        api_key="not-needed",
    )
    return model
