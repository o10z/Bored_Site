# imports used
from flask import Flask, render_template, request, flash
import requests
import json
import key

# Create a Flask app instance
app = Flask(__name__)

# Key set for session management
app.config['SECRET_KEY'] = key.SECRET_KEY


# Define the route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    # Available activity and participant options
    activitys = ['education', 'recreational', 'social', 'diy', 'charity', 'cooking', 'relaxation', 'music', 'busywork']
    participants = ['1', '2', '3', '4', '5+']

    if request.method == "POST":
        # Retrieve selected activity and number of participant
        selected_activity = request.form.get('activitys')
        if request.form.get('participants') == "5+":
            number_of_participant = '5'
        else:
            number_of_participant = request.form.get('participants')

        # Parameters for API request
        params = {
            "type": selected_activity,
            "participants": number_of_participant,
        }

        # Send request to API
        response = requests.get(url=f'https://www.boredapi.com/api/activity/', params=params)

        # Parse the API response
        answer = json.loads(response.text)
        try:
            flash(answer["activity"])
        except KeyError:
            flash(answer['error'])

    else:
        # Set defalt values for selected_activity and number_of_participant
        selected_activity = ""
        number_of_participant = ""

    # Render the template with data
    return render_template("index.html", activitys=activitys, participants=participants,
                           selected_activity=selected_activity, number_of_participant=number_of_participant)


# Run the app if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
