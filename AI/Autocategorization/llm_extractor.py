from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ---------- PROMPT TEMPLATE ----------
SYSTEM_PROMPT = """
You extract ALL expenses mentioned in a paragraph.
Return ONLY a clean JSON list (no extra text).

Each expense must contain:
- amount (number only)
- category (Food, Travel, Groceries, Shopping, Entertainment, Bills, Medical, Education, Other)
- merchant (if available)
- description
- date (if mentioned else use "today")

If multiple expenses are inside one sentence or paragraph, extract ALL of them.
"""

USER_PROMPT = """
Extract all expenses from this paragraph:

{paragraph}
"""


class LLMExtractor:

    def __init__(self):
        self.model = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model="openai/gpt-oss-120b",
            streaming=True,
            temperature=0.5
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_PROMPT),
                ("user", USER_PROMPT)
            ]
        )

    def extract(self, paragraph: str):
        """Run paragraph through Groq LLM and return structured JSON."""

        # Prepare final prompt
        messages = self.prompt.format_messages(paragraph=paragraph)

        # Call the model
        result = self.model.invoke(messages)
        response_text = result.content.strip()

        # Try direct JSON parse
        try:
            return json.loads(response_text)
        except:
            # Fix JSON if model added extra text
            return self._force_json(response_text)

    def _force_json(self, text: str):
        """Extract JSON list even if mixed with extra output."""
        try:
            json_part = text[text.index("[") : text.rindex("]") + 1]
            return json.loads(json_part)
        except:
            return []
