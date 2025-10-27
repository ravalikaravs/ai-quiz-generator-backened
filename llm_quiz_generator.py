
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import json

# Initialize Gemini model
gemini_client = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=r"C:\Users\HP\desktop\ai-quiz-generator\backened\key.json"
)

def generate_quiz(article_text: str):
    prompt_template = """
Generate a quiz from the following Wikipedia article. Create 5 questions.
Return JSON like this:
{
  "title": "Article Title",
  "summary": "Brief summary of the article.",
  "quiz": [
    {
      "question": "Question text",
      "options": ["Option1","Option2","Option3","Option4"],
      "answer": "Correct option",
      "difficulty": "easy/medium/hard",
      "explanation": "Short explanation."
    }
  ],
  "related_topics": ["Topic1","Topic2"]
}
Text: {text}
"""

    prompt = PromptTemplate(input_variables=["text"], template=prompt_template)
    result = gemini_client.generate([prompt.format(text=article_text)])
    quiz_json = json.loads(result)  # result is a string
    return quiz_json
