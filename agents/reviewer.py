# agents/reviewer.py

from agents.router import smart_route, route, TaskType

def run_full_review(code: str, language: str):
    """
    Runs all 3 specialized chains using the right model for each.
    """

    results = {}

    # Bug scan — fast Groq
    print("Bugg Scan by Groq...")
    bug_llm = route(TaskType.QUICK_BUG)
    results["bugs"] = bug_llm.invoke(
        f"Find bugs in this {language} code:\n```{code}```"
    ).content
    

    # Security — Mistral
    print("Security Scan by Mistral...")
    security_llm = route(TaskType.SECURITY_AUDIT)
    results["security"] = security_llm.invoke(
        f"Audit this {language} code for security issues:\n```{code}```"
    ).content

    # Deep review — Gemini
    print("Deep Analysis Scan by Gemini...")
    deep_llm = route(TaskType.DEEP_REVIEW)
    results["deep_review"] = deep_llm.invoke(
        f"Give a comprehensive architectural review:\n```{code}```"
    ).content

    return results


def handle_followup(user_query: str, context: str):
    """
    Used for chat follow-ups — auto-routes based on what user asks.
    """
    llm, task_type = smart_route(user_query)

    prompt = f"""
Context:
{context}

Developer question: {user_query}
Mentor:"""

    response = llm.invoke(prompt)
    return response.content, task_type