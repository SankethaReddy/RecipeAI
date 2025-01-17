import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def get_recipe(ingredients):
    """
    Generate recipe suggestions based on available ingredients
    """
    prompt = f"""Given these ingredients: {ingredients}
    Please suggest 2-3 simple recipes that can be made using some or all of these ingredients.
    For each recipe, provide:
    1. Recipe name
    2. Required ingredients from the available list
    3. Any basic ingredients assumed to be available (salt, pepper, water, etc.)
    4. Step-by-step cooking instructions
    5. Approximate cooking time
    
    Format the response in a clear, easy-to-read way."""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful cooking assistant that suggests recipes based on available ingredients. Focus on practical, simple recipes that are easy to follow."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_completion_tokens=1024,
        top_p=1,
        stream=True,
    )
    
    # Collect the streamed response
    response = ""
    for chunk in completion:
        chunk_content = chunk.choices[0].delta.content
        if chunk_content is not None:
            response += chunk_content
            
    return response

# Streamlit UI
def main():
    st.title("🍳 Recipe Suggestion Bot")
    st.write("Enter the ingredients you have available, and I'll suggest some recipes!")

    # Text area for ingredients input
    ingredients = st.text_area(
        "List your ingredients (separate with commas):",
        placeholder="Example: chicken breast, potatoes, onions, garlic, tomatoes",
        height=100
    )

    # Add a button to generate recipes
    if st.button("Generate Recipes", type="primary"):
        if ingredients:
            with st.spinner("Cooking up some recipes... 👩‍🍳"):
                try:
                    recipes = get_recipe(ingredients)
                    st.markdown("### 📖 Suggested Recipes")
                    st.markdown(recipes)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter some ingredients first!")

    # Add some helpful tips in the sidebar
    with st.sidebar:
        st.markdown("### 💡 Tips")
        st.markdown("""
        - List all main ingredients you have available
        - Include common pantry items if possible
        - Separate ingredients with commas
        - Be specific (e.g., 'chicken breast' instead of just 'chicken')
        """)

if __name__ == "__main__":
    main()