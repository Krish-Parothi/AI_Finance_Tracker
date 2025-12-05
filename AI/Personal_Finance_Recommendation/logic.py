from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

from data_access import (
    get_category_totals,
    get_hourly_distribution,
    get_weekly_distribution
)

# Initialize LLM via Groq
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    groq_api_key = os.getenv("PFR_GROQ_API_KEY"),
    temperature=0.5,
    streaming=True
)

# -------- Rules --------
def detect_category_spike(category_totals: dict):
    if not category_totals:
        return None
    max_cat = max(category_totals, key=category_totals.get)
    total = sum(category_totals.values())
    if total > 0 and category_totals[max_cat] > 0.4 * total:
        return f"High spending concentration detected in {max_cat}."
    return None

def detect_hour_cluster(hour_data: dict):
    if not hour_data:
        return None
    peak_hour = max(hour_data, key=hour_data.get)
    if peak_hour >= 20:
        return "Frequent late-evening spending detected."
    return None

def detect_weekend_bias(week_data: dict):
    if not week_data:
        return None
    weekend_total = week_data.get(1, 0) + week_data.get(7, 0)
    weekday_total = sum(week_data.values()) - weekend_total
    if weekend_total > weekday_total:
        return "Weekend-heavy spending pattern detected."
    return None

def detect_savings_gap(category_totals: dict, target):
    if not target:
        return None
    total = sum(category_totals.values()) if category_totals else 0
    if total > target:
        return "Spending exceeds target savings threshold."
    return None

# -------- Formatter --------
def build_personalised_tip(triggers: list, summaries: dict):
    try:
        trigger_text = "; ".join([t for t in triggers if t]) or "No anomalies detected."
        prompt = ChatPromptTemplate.from_messages([
            ("user", "User spending indicators: " + trigger_text +
             ". Produce one concise corrective action.")
        ])
        chain = prompt | llm
        result = chain.invoke({})
        return result.content.strip()
    except Exception:
        return "Unable to generate tip."

# -------- Orchestrator --------
async def generate_personalised_tip(user_id, target_savings=None):
    try:
        category_totals = await get_category_totals(user_id)
        hourly = await get_hourly_distribution(user_id)
        weekly = await get_weekly_distribution(user_id)

        triggers = [
            detect_category_spike(category_totals),
            detect_hour_cluster(hourly),
            detect_weekend_bias(weekly),
            detect_savings_gap(category_totals, target_savings),
        ]

        summaries = {
            "category_totals": category_totals,
            "hourly": hourly,
            "weekly": weekly,
        }

        tip = build_personalised_tip(triggers, summaries)
        return tip

    except Exception:
        return "Unable to generate personalised tip."
