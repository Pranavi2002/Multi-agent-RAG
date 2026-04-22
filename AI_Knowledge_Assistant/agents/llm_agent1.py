# uses OpenAI API key

import os
import openai

class LLMAgent:
    def __init__(self, api_key=None):
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")

    def generate_answer(self, query, context_docs):
        context_text = "\n\n".join(context_docs)
        prompt = f"Answer the query based on the following context:\n{context_text}\n\nQuery: {query}\nAnswer:"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0
        )
        return response['choices'][0]['message']['content']