import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class DocumentSummarizer:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

    def summarize(self, text: str, summary_type: str = "executive"):

        prompts = {
            "executive":
                "Generate a concise executive summary of the following document.",

            "technical":
                "Generate a detailed technical summary of the following document.",

            "bullet":
                "Summarize the following document into clear bullet points.",

            "key_takeaways":
                "List the key takeaways from the following document."
        }

        instruction = prompts.get(
            summary_type.lower(),
            prompts["executive"]
        )

        prompt = f"""
{instruction}

Document:

{text}

Summary:
"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text