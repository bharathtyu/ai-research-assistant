import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class DocumentComparator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found.")

        self.client = genai.Client(api_key=api_key)

    def compare(self, document1: str, document2: str):

        prompt = f"""
Compare the following two documents.

Provide:

1. Summary of Document 1
2. Summary of Document 2
3. Similarities
4. Differences
5. Overall conclusion

Document 1:
{document1}

-------------------------------------

Document 2:
{document2}
"""

        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text