# AI/Assistant/engine/llm_engine.py

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# -----------------------------
# LLM INITIALIZATION
# -----------------------------
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
    temperature=0.2
)

# -----------------------------
# PROMPT TEMPLATE
# -----------------------------
FINANCE_PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     """
     You are an AI Finance Assistant.
     You receive:
       - the user's natural language query
       - the user's complete expense history from the database

     Your tasks:
     1. Understand the user's request (week total, category analysis, predictions, spikes, trends, etc.)
     2. Analyze ONLY the provided expense data.
     3. Compute correct totals or insights.
     4. Give a short, clear answer.
     5. NEVER hallucinate missing data.
     """
    ),
    ("human",
     "User question: {query}\n\nUser expense data: {data}")
])


# -----------------------------
# MAIN AI ENGINE FUNCTION
# -----------------------------
def run_ai_engine(query: str, user_data: list):
    """
    Runs LangChain + Groq LLM using prompt + user expense history.
    """
    chain = FINANCE_PROMPT | llm
    result = chain.invoke({
        "query": query,
        "data": user_data
    })
    return result.content
