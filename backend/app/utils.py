# Lead Scoring Utility
def calculate_lead_score(model, data):
    probability = model.predict_proba(data)[0][1]
    score = round(probability * 100, 2)
    return score, probability


# =====================================
# LLaMA Email Generator (using Groq - FREE)
# =====================================
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def generate_email_llama2(customer_name, lead_score, quote_value, item_count, use_case_id=None):
    
    # Fetch use case details if provided
    use_case_context = ""
    if use_case_id:
        from app.use_cases import get_use_case_by_id
        use_case = get_use_case_by_id(use_case_id)
        if use_case:
            use_case_context = f"""
            Relevant Use Case: {use_case.title}
            Customer Industry: {use_case.industry}
            Customer Pain Points: {', '.join(use_case.pain_points)}
            Our Solution: {use_case.solution_summary}
            Success Story: {use_case.success_metrics}
            
            INSTRUCTION: Align the email specifically to address the pain points above and mention the solution.
            """

    prompt = f"""
You are a B2B IT sales expert.

Customer Name: {customer_name}
Lead Score: {lead_score}
Quotation Value: {quote_value}
Number of Items: {item_count}

{use_case_context}

Write a professional outbound sales email.
The tone should adapt based on the lead score:
- High score → confident and closing
- Medium score → warm and informative
- Low score → introductory and educational
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30
    )

    result = response.json()

    # Safety fallback
    if "choices" not in result:
        print(f"Groq API Error: {response.status_code} - {response.text}")
        return f"Unable to generate email at this time. Error: {result.get('error', {}).get('message', 'Unknown error')}"

    return result["choices"][0]["message"]["content"]
