import os
import sys
from typing import Optional
from groq import Groq

class LLMHandler:
    def __init__(self, model="llama-3.3-70b-versatile"):
        self.client = None
        # self.api_key = os.getenv("GROQ_API_KEY")
        self.api_key = "insert_groq_key_here"
        self.model = model

    def initialize_llm(self) -> None:
        try:
            if not self.api_key:
                raise ValueError("Groq API Key not found")
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            print(f"Error initializing Groq: {str(e)}")
            sys.exit(1)

    def get_response(self, messages):
        try:
            if self.client is None:
                self.initialize_llm()

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.3
            )
            
            return chat_completion.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error getting Groq response: {str(e)}")
            return None
