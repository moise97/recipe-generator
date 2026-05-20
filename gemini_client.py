from google import genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_recipes(ingredients: list[str], system_prompt: str, dietary_preference: str = "No preference") -> list[dict]:
    ingredients_text = ", ".join(ingredients)
    
    diet_note = ""
    if dietary_preference != "No preference":
        diet_note = f"All recipes must be {dietary_preference}."

    prompt = f"""
    {system_prompt}
    
    {diet_note}
    
    I have these ingredients: {ingredients_text}
    
    Suggest exactly 3 recipes I can make. Return ONLY a valid JSON array with exactly 3 recipe objects.
    Each object must have: name, cook_time, difficulty, ingredients_needed (array), steps (array), nutrition (object with calories, protein, carbs, fat).
    """

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    cleaned = response.text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1]
        cleaned = cleaned.rsplit("```", 1)[0]

    recipes = json.loads(cleaned)
    return recipes


def test_connection():
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents="Say hello in exactly 5 words."
    )
    print("API connected! Gemini says:", response.text)