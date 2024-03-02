import csv
import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for, session, Response, jsonify

api_url = 'https://api.usa.gov/crime/fbi/cde/'
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'nplktm8848apicu23mis1237rbs'
# Initialize the maximum login attempts threshold
MAX_LOGIN_ATTEMPTS = 3
us_states_list = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming", "United States"]


def get_data(link):
    response = requests.get(api_url + link + '&API_KEY=yMAh4CVB2EscynftMmBRMAhtY0UQZ5m1fVDMC8gf')

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Failed to retrieve data from the API."


def fetch_data(see_by_what):
    data_list = []

    if see_by_what:
        us_state = request.form.getlist('us_state')
        offense_ = request.form.getlist('offense')
        from_ = request.form.get('from')
        to = request.form.get('to')

        for state in us_state:
            for offense in offense_:
                if "all" in us_state:
                    link = '/estimate/national/' + offense + '?from=' + from_ + '&to=' + to
                    data_list.append(get_data(link))
                else:
                    link = '/estimate/state/' + state + '/' + offense + '?from=' + from_ + '&to=' + to
                    data_list.append(get_data(link))
    else:
        offense_ = request.form.getlist('offense')
        us_state = request.form.getlist('us_state')
        from_ = request.form.get('from')
        to = request.form.get('to')

        for offense in offense_:
            for state in us_state:
                if state == "all":
                    link = '/estimate/national/' + offense + '?from=' + from_ + '&to=' + to
                    data_list.append(get_data(link))
                else:
                    link = '/estimate/state/' + state + '/' + offense + '?from=' + from_ + '&to=' + to
                    data_list.append(get_data(link))

    return data_list


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        # Check if the user has exceeded the maximum login attempts
        if session.get('login_attempts', 0) >= MAX_LOGIN_ATTEMPTS:
            return "Maximum login attempts reached. Please try again later."

        readfile = open("userdetails.txt")
        reader = csv.DictReader(readfile)

        # Initialize separate lists to store index, username, and password values
        index_list = []
        username_list = []
        password_list = []

        for line in reader:
            index_list.append(line['index'])
            username_list.append(line['username'])
            password_list.append(line['password'])

        if username in username_list and password in password_list and username_list.index(username) == password_list.index(password):
            session['logged_in'] = True
            session.pop('login_attempts', None)  # Reset login attempts counter
            return redirect(url_for('home'))  # Redirect to the 'home' page.
        else:
            session['login_attempts'] = session.get('login_attempts', 0) + 1
            return "Invalid credentials. Please try again."

    return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        see_what = request.form.get('see_what')
        see_by_what = request.form.get('see_by_what')

        if see_what == "data":
            return redirect(url_for('data_print', is_state=(see_by_what == "state")))
        elif see_what == "visualization":
            return redirect(url_for('visualization', is_state=(see_by_what == "state")))

    return render_template('home.html')


@app.route('/home/data', methods=['GET', 'POST'])
def data_print():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    is_state = (request.args.get('is_state') == "True")

    if request.method == 'POST':
        return jsonify(fetch_data(is_state))

    return render_template('data.html') if is_state else render_template('data_offense.html')


@app.route('/home/visualization', methods=['GET', 'POST'])
def visualization():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    is_state = (request.args.get('is_state') == "True")

    if request.method == 'POST':
        data = fetch_data(is_state)

        all_states = []
        all_offenses = []
        all_years = []
        all_crime_values = []

        for state_dict in data:
            values = next(iter(state_dict['results'].values()))
            years = list(values.keys())
            crime_values = list(values.values())

            temp_state = next(iter(state_dict['results'].keys()))
            state_names = [state for state in us_states_list if state in temp_state]
            offense_names = [temp_state.replace(state, "") for state in us_states_list if state in temp_state]
            print(state_names)
            all_states.append(state_names)
            all_offenses.append(offense_names)
            all_years.append(list(years))  # Convert to list
            all_crime_values.append(list(crime_values))  # Convert to list

        # Plot the data for each state with different colors
        for i, state_data in enumerate(zip(all_years, all_crime_values, all_states, all_offenses)):
            years, crime_values, state, offense = state_data
            plt.plot(years, crime_values, label=offense[0], color=plt.cm.get_cmap('tab10')(i)) if is_state \
                else plt.plot(years, crime_values, label=state[0], color=plt.cm.get_cmap('tab10')(i))

        plt.title("Crime Data by State: " + state[0]) if is_state else plt.title("Crime Data by Offense:" + offense[0])
        plt.xlabel('Year')
        plt.ylabel('Count')
        plt.xticks(rotation='vertical')
        plt.legend()
        plt.savefig('static/figs/plot.png')  # Save the plot to a file
        plt.clf()  # Clear the plot for the next iteration

        return render_template('see_viz.html')

        if request.form.get('status') == 'back':
            return redirect(url_for('visualization', is_state=is_state))

    return render_template('data.html') if is_state else render_template('data_offense.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
