from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import streamlit as st


function = {
    "name": "create_quiz",
    "description": "function that takes a list of questions and answers and returns a quiz",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                        },
                        "answers": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "answer": {
                                        "type": "string",
                                    },
                                    "correct": {
                                        "type": "boolean",
                                    },
                                },
                                "required": ["answer", "correct"],
                            },
                        },
                    },
                    "required": ["question", "answers"],
                },
            }
        },
        "required": ["questions"],
    },
}


llm = ChatOpenAI(
    temperature=0.1,
).bind(
    function_call={
        "name": "create_quiz",
    },
    functions=[
        function,
    ],
)

prompt = PromptTemplate.from_template("Make a quiz about {city}")

chain = prompt | llm

response = chain.invoke({"city": "rome"})


response = response.additional_kwargs["function_call"]["arguments"]

st.write(response)
