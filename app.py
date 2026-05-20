import gradio as gr
from gemini_client import get_recipes
from prompts import RECIPE_SYSTEM_PROMPT

def generate_recipes(ingredients_text, dietary_preference):
    if not ingredients_text.strip():
        return "Please enter at least one ingredient."
    
    ingredients = [i.strip() for i in ingredients_text.split(",")]
    
    try:
        recipes = get_recipes(ingredients, RECIPE_SYSTEM_PROMPT, dietary_preference)
        
        output = ""
        for i, recipe in enumerate(recipes, 1):
            output += f"## Recipe {i}: {recipe['name']}\n"
            output += f"⏱ {recipe['cook_time']} | Difficulty: {recipe['difficulty']}\n\n"
            output += f"**Ingredients:**\n"
            for ing in recipe['ingredients_needed']:
                output += f"- {ing}\n"
            output += f"\n**Steps:**\n"
            for j, step in enumerate(recipe['steps'], 1):
                output += f"{j}. {step}\n"
            output += f"\n**Nutrition:** {recipe['nutrition']['calories']} cal | "
            output += f"Protein: {recipe['nutrition']['protein']} | "
            output += f"Carbs: {recipe['nutrition']['carbs']} | "
            output += f"Fat: {recipe['nutrition']['fat']}\n\n"
            output += "---\n\n"
        
        return output
    
    except Exception as e:
        return f"Something went wrong: {str(e)}"

demo = gr.Interface(
    fn=generate_recipes,
    inputs=[
        gr.Textbox(
            label="What ingredients do you have?",
            placeholder="e.g. chicken, rice, garlic, olive oil, lemon",
            lines=2
        ),
        gr.Dropdown(
            choices=["No preference", "Vegetarian", "Vegan", "Gluten-free", "Low-carb"],
            label="Dietary preference",
            value="No preference"
        )
    ],
    outputs=gr.Markdown(label="Your Recipes"),
    title="AI Recipe Generator",
    description="Enter ingredients you have at home and get 3 instant recipe ideas powered by Gemini AI.",
    examples=[
        ["chicken, rice, garlic, olive oil, lemon", "No preference"],
        ["eggs, cheese, spinach, mushrooms", "Vegetarian"],
        ["salmon, broccoli, soy sauce, ginger", "Low-carb"]
    ]
)

if __name__ == "__main__":
    demo.launch()