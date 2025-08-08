from literaturereviewbot import search
from literaturereviewbot.documents import index_documents, retrieve_documents


async def generate_prompt(question):
    _, abstract_arr, ids = await search.query(question)
    if not abstract_arr:
        return "I don't have enough information to answer this question."

    vector_store = index_documents(
        query=question, abstract_arr=abstract_arr, ids_arr=ids
    )
    documents = retrieve_documents(question, vector_store)
    messages = [
        {
            "role": "system",
            "content_type": "instructions",
            "content": """
             You are a professional biomedical researcher.
             You will be given a series of article abstracts.
             The information in your response should exclusively come from the content type 'abstracts'.
             If no relevant information is found in the abstracts, you can say 'I don't have enough information to answer this question'.
            """,
        }
    ]
    for i, doc in enumerate(documents):
        try:
            content = doc.page_content if hasattr(doc, "page_content") else ""
        except Exception:
            print(doc)
            content = ""
            continue
        messages.append(
            {
                "role": "user",
                "content_type": "abstracts",
                "content": f"abstract {i}:\n" + content,
            }
        )

    messages.append({"role": "user", "content_type": "query", "content": {question}})

    prompt = ""
    for message in messages:
        prompt += "{"
        for key, value in message.items():
            prompt += f"{key} : {value},"
        prompt += "}\n"

    return prompt
