from literaturereviewbot.search_pubmed import query as pubmed_query
from literaturereviewbot.documents import index_documents, retrieve_documents


def generate_prompt(question):
    _, abstract_arr, pubmed_ids = pubmed_query(question)
    vector_store = index_documents(
        query=question, abstract_arr=abstract_arr, ids_arr=pubmed_ids
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
        except:
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
