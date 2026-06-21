# agents/router.py

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mistralai import ChatMistralAI
from enum import Enum
from dotenv import load_dotenv

load_dotenv();

# ─────────────────────────────────────────
# Task types — used to decide routing
# ─────────────────────────────────────────
class TaskType(str, Enum):
    QUICK_BUG = "quick_bug"
    SECURITY_AUDIT = "security_audit"
    DEEP_REVIEW = "deep_review"
    MENTOR_CHAT = "mentor_chat"
    ANTI_PATTERN = "anti_pattern"


# ─────────────────────────────────────────
# LLM Clients — created once, reused
# ─────────────────────────────────────────

def get_groq_llm(streaming: bool = True):
    return ChatGroq(
     
     model_name="llama-3.1-8b-instant",
        temperature=0.2,        # low temp = consistent, factual code review
        streaming=streaming,
        max_tokens=2048
    )

def get_gemini_llm(streaming: bool = True):
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        max_output_tokens=4096,  # bigger, for deep review
        streaming=streaming
    )

def get_mistral_llm(streaming: bool = True):
    return ChatMistralAI(
      
           model="mistral-large-latest",
        temperature=0.1,        # very low — security needs precision
        streaming=streaming,
        max_tokens=2048
    )


# ─────────────────────────────────────────
# Routing table
# ─────────────────────────────────────────

ROUTING_TABLE = {
    TaskType.QUICK_BUG:      get_groq_llm,      # speed priority
    TaskType.SECURITY_AUDIT: get_mistral_llm,   # security priority
    TaskType.DEEP_REVIEW:    get_gemini_llm,    # context window priority
    TaskType.MENTOR_CHAT:    get_groq_llm,      # fast, conversational
    TaskType.ANTI_PATTERN:   get_groq_llm,      # fast pattern matching
}


# ─────────────────────────────────────────
# Main router function
# ─────────────────────────────────────────

def route(task_type: TaskType, streaming: bool = True):
    """
    Returns the correct LLM client for a given task.

    Usage:
        llm = route(TaskType.SECURITY_AUDIT)
        response = llm.invoke("Check this code for SQL injection...")
    """
    llm_factory = ROUTING_TABLE.get(task_type)

    if llm_factory is None:
        raise ValueError(f"Unknown task type: {task_type}")
    
    print("Routing the llm...")

    return llm_factory(streaming=streaming)


# ─────────────────────────────────────────
# Smart classifier — auto-detect task type from query
# (so you don't always have to manually pass TaskType)
# ─────────────────────────────────────────

def classify_query(user_query: str) -> TaskType:
    """
    Cheap keyword-based classifier.
    Runs locally — no API call needed, instant.
    """
    query_lower = user_query.lower()

    security_keywords = ["sql injection", "xss", "security", "vulnerab",
                          "secret", "auth", "password", "csrf", "owasp"]
    deep_keywords = ["explain in detail", "full review", "architecture",
                      "entire file", "comprehensive", "deep dive"]
    pattern_keywords = ["anti-pattern", "code smell", "refactor", "design pattern"]

    if any(kw in query_lower for kw in security_keywords):
        return TaskType.SECURITY_AUDIT
    elif any(kw in query_lower for kw in deep_keywords):
        return TaskType.DEEP_REVIEW
    elif any(kw in query_lower for kw in pattern_keywords):
        return TaskType.ANTI_PATTERN
    else:
        return TaskType.QUICK_BUG  # default — fastest path


def smart_route(user_query: str, streaming: bool = True):
    """
    One-call convenience function:
    auto-classifies query AND returns the right LLM.
    """
    task_type = classify_query(user_query)
    llm = route(task_type, streaming=streaming)
    print(f"[Router] '{user_query[:40]}...' → {task_type.value}")
    return llm, task_type