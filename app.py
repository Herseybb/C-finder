import streamlit as st
import requests

# ---------------- CONFIG ----------------
BASE_SEARCH_URL = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="
BASE_DETAIL_URL = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Cocktail Finder", layout="wide")
st.title("🍹 Cocktail Finder")
st.markdown("Enter ingredients (e.g., `vodka, rum, orange`) to discover matching drinks.")

# ---------------- USER INPUT ----------------
user_input = st.text_input("Ingredients (comma-separated)", "")

if user_input:
    ingredients = [i.strip() for i in user_input.split(',') if i.strip()]
    found_drinks = {}

    with st.spinner("Searching for cocktails..."):
        for ingredient in ingredients:
            url = f"{BASE_SEARCH_URL}{ingredient}"
            res = requests.get(url)
            if res.status_code != 200 or not res.json().get("drinks"):
                continue
            for drink in res.json()["drinks"]:
                found_drinks[drink["idDrink"]] = drink  # De-duplicate by ID

    if not found_drinks:
        st.warning("😕 No drinks found. Try changing the keywords.")
    else:
        st.success(f"Found {len(found_drinks)} drinks using your ingredients!")

        cols = st.columns(3)
        for i, drink in enumerate(found_drinks.values()):
            detail_res = requests.get(f"{BASE_DETAIL_URL}{drink['idDrink']}")
            if detail_res.status_code != 200 or not detail_res.json().get("drinks"):
                continue

            detail = detail_res.json()["drinks"][0]
            name = detail["strDrink"]
            image = detail["strDrinkThumb"]
            instructions = detail.get("strInstructions", "No instructions available.")

            # Get ingredients
            ingredients_list = []
            for j in range(1, 16):
                ing = detail.get(f"strIngredient{j}")
                measure = detail.get(f"strMeasure{j}")
                if ing:
                    ingredients_list.append(f"- {measure.strip() if measure else ''} {ing.strip()}")

            with cols[i % 3]:
                st.image(image, use_container_width=True)
                st.subheader(name)
                st.markdown("**Ingredients:**")
                st.markdown("\n".join(ingredients_list))
                st.markdown("**Instructions:**")
                st.markdown(instructions)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Made with ❤️ using [TheCocktailDB](https://www.thecocktaildb.com)")
