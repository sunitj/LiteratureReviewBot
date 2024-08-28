from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate

# def generate_prompt(question):
#     messages = [
#         {
#             "role": "system",
#             "content_type": "instructions",
#             "content": """
#                 You are an experienced professional biomedical researcher.
#                 You will will be given a question or a statement to respond to.
#                 Identify the keywords in the question or statement and return the keywords separated by commas.
#             """,
#         }
#     ]

#     messages.append({"role": "user", "content_type": "query", "content": {question}})

#     prompt = ""
#     for message in messages:
#         prompt += "{"
#         for key, value in message.items():
#             prompt += f"{key} : {value},"
#         prompt += "}\n"

#     return prompt


class Keywords(BaseModel):
    """Identifying information about entities."""

    kwds: list[str] = Field(
        ...,
        description="All the person, organization, or business entities that "
        "appear in the text",
    )
