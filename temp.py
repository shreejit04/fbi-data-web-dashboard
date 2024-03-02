import requests
import matplotlib.pyplot as plt

api_url = 'https://api.usa.gov/crime/fbi/cde/'
us_state = ["CT"]
offense_ = ["robbery", "arson", "burglary"]
from_ = "2019"
to = "2021"
see_by_what = False

def get_data(link):
    response = requests.get(api_url + link + '&API_KEY=yMAh4CVB2EscynftMmBRMAhtY0UQZ5m1fVDMC8gf')

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Failed to retrieve data from the API."

data_list = []
if see_by_what:
    for state in us_state:
        for offense in offense_:
            if "all" in us_state:
                link = '/estimate/national/' + offense_ + '?from=' + from_ + '&to=' + to
                data_list.append(get_data(link))
            else:
                link = '/estimate/state/' + state + '/' + offense_ + '?from=' + from_ + '&to=' + to
                data_list.append(get_data(link))
else:
    for offense in offense_:
        for state in us_state:
            if state == "all":
                link = '/estimate/national/' + offense + '?from=' + from_ + '&to=' + to
                data_list.append(get_data(link))
            else:
                link = '/estimate/state/' + state + '/' + offense + '?from=' + from_ + '&to=' + to
                data_list.append(get_data(link))

all_states = []
all_years = []
all_crime_values = []

for state_dict in data_list:
    values = next(iter(state_dict['results'].values()))
    years = list(values.keys())
    crime_values = list(values.values())

    all_states.append(next(iter(state_dict['results'].keys())))
    all_years.append(list(years))  # Convert to list
    all_crime_values.append(list(crime_values))  # Convert to list

# Plot the data for each state with different colors
for i, state_data in enumerate(zip(all_years, all_crime_values, all_states)):
    years, crime_values, state = state_data
    plt.plot(years, crime_values, label=state, color=plt.cm.get_cmap('tab10')(i))

plt.title("Crime Data by State")
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation='vertical')
plt.legend()
plt.show()
