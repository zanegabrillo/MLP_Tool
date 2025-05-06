from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np

# Load the model and encoder from the file
with open('calorie_prediction_model.pkl', 'rb') as f:
    model, encoder = pickle.load(f)

# Setup
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # This is needed for session to work

food_items = list(encoder.categories_[0])  # For dropdown

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    selected_food = ""
    grams = ""
    
    # Initialize food_entries if not already in session
    if 'food_entries' not in session:
        session['food_entries'] = []

    # Process form submission
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            selected_food = request.form["food"].strip().lower()
            grams = float(request.form["grams"])

            # Add the food and grams to the list in session
            session['food_entries'].append((selected_food, grams))
            session.modified = True  # Mark the session as modified so it gets saved

            # Redirect to avoid resubmission
            return redirect(url_for('index'))

        elif action == "remove":
            remove_index = int(request.form["remove_index"])
            # Remove the selected food from the list
            session['food_entries'].pop(remove_index)
            session.modified = True  # Mark the session as modified

            # Redirect to avoid resubmission
            return redirect(url_for('index'))

    # Calculate total calories after form submission or on initial load
    total_calories = 0
    for food_name, grams in session['food_entries']:
        encoded = encoder.transform([[food_name]])
        features = np.concatenate([encoded[0], [grams]])
        total_calories += model.predict([features])[0]

    prediction = round(total_calories, 2)

    return render_template("index.html", food_items=food_items, prediction=prediction,
                           food_entries=session['food_entries'], selected_food=selected_food, grams=grams)

if __name__ == "__main__":
    app.run(debug=True)
