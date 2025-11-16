from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

gemini_client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)

def extract_json(text):
    """Extract the first valid JSON object from LLM output."""
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in LLM response")
    return json.loads(match.group())


def clean_json_markdown(text):
    """Remove ```json ... ``` wrapper if present."""
    return text.replace("```json", "").replace("```", "").strip()


def generate_quiz(article_text: str):
    prompt_template = """
Generate a quiz from the following text. Create 5 questions.
Return ONLY a JSON object in this format:

{{
  "title": "Article Title",
  "summary": "Brief summary of the article.",
  "quiz": [
    {{
      "question": "Question text",
      "options": ["Option1","Option2","Option3","Option4"],
      "answer": "Correct option",
      "difficulty": "easy/medium/hard",
      "explanation": "Short explanation."
    }}
  ],
  "related_topics": ["Topic1","Topic2"]
}}

Text: {text}
"""
    prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

    print("\n--- Sending prompt to Gemini ---\n")
    print(prompt.format(text=article_text))

    response = gemini_client.invoke(prompt.format(text=article_text))
    text_output = response.content[0].text if hasattr(response.content[0], "text") else str(response.content)

    print("\n--- Gemini Raw Output ---\n")
    print(text_output)

    try:
        cleaned = clean_json_markdown(text_output)
        quiz_json = extract_json(cleaned)
        return quiz_json
    except Exception as e:
        print("\n--- JSON Parsing Error ---")
        print(e)
        return None