import google.generativeai as genai
import requests

# Google Gemini AI API Key
API_KEY = "AIzaSyDM7z8pBmnrkX8e9ycc4CRgWUmJFlgzr6o"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Nutritionix API credentials
app_id = 'f9f1895e'
api_key = 'c8cdaff4b8d656b4b7f9d0e53405f424'

def calculate_bmi(weight, height):
    height_m = height / 100  # converting height to metersd
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

def generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input=None):
    # Construct the prompt for the Gemini AI model
    prompt = (
        f"Hi, {name}! Based on the following details:\n"
        f"Age: {age}\n"
        f"Gender: {gender}\n"
        f"BMI: {bmi}\n"
        f"Diet Preference: {diet_preference}\n"
        f"Location: India\n"  # Specify the location
    )

    if additional_input:
        prompt += f"Additional Input: {additional_input}\n"

    prompt += (
        f"\nPlease provide a personalized diet plan that is nutritionally balanced, "
        f"affordable, and suitable for their health status. Include common and affordable "
        f"Indian food items and easy-to-make recipes that are adaptable to daily life in India."
    )

    # Generate the response using Gemini AI
    response = model.generate_content(prompt)

    return response.text

def get_nutritional_info(food_item):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": app_id,
        "x-app-key": api_key,
        "Content-Type": "application/json"
    }
    body = {
        "query": food_item,
        "timezone": "US/Eastern"
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['foods']:
            food = data['foods'][0]
            return {
                "calories": food.get('nf_calories'),
                "protein": food.get('nf_protein'),
                "carbohydrates": food.get('nf_total_carbohydrate'),
                "fat": food.get('nf_total_fat')
            }
        else:
            return None
    else:
        return None

def main():
    # Taking user input
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    gender = input("Select your gender (Male, Female, Other): ")
    weight = float(input("Enter your weight (kg): "))
    height = float(input("Enter your height (cm): "))
    diet_preference = input("Do you prefer a vegetarian or non-vegetarian diet? (Veg/Non-Veg): ")

    # Additional Input Box for Custom Preferences
    additional_input = input("Enter any additional preferences or restrictions (e.g., allergies, dislikes): ")

    if name and age and weight and height and diet_preference:
        # Calculate BMI
        bmi = calculate_bmi(weight, height)
        print(f"Hello {name}, your BMI is: {bmi}")

        # Generate a personalized diet plan
        diet_plan = generate_diet_plan(bmi, diet_preference, name, age, gender, additional_input)
        print("\nYour Personalized Diet Plan:\n")
        print(diet_plan)
    else:
        print("Please fill in all the details.")

    # Asking for food item to get nutritional information
    food_item = input("\nEnter food item to get nutritional information: ")
    if food_item:
        nutrition = get_nutritional_info(food_item)
        if nutrition:
            print(f"\nNutritional Information for {food_item.title()}:")
            print(f"Calories: {nutrition['calories']} kcal")
            print(f"Protein: {nutrition['protein']} g")
            print(f"Carbohydrates: {nutrition['carbohydrates']} g")
            print(f"Fat: {nutrition['fat']} g")
        else:
            print("Sorry, don't have nutritional information for that food item.")
    else:
        print("Please enter a food item.")

if __name__ == "__main__":
    main()
