def choose_llm(query: str) -> str:
    """
    Route query to appropriate LLM based on intent.
    Fast models for lightweight tasks, accurate models for reasoning.
    """
    q = query.lower()

    if any(keyword in q for keyword in ["summarize", "brief", "tl;dr"]):
        return "fast-llm"

    if any(keyword in q for keyword in ["why", "explain", "how", "compare"]):
        return "accurate-llm"

    return "accurate-llm"