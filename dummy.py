# Example of a nested dictionary
crime_data = {
    'results': {
        'New York Burglary': {'2019': 144.2, '2020': 165.5, '2021': 149.6},
        'United States Burglary': {'2019': 340.5, '2020': 314.2, '2021': 270.9}
    }
}

# Access the first dictionary inside the nested dictionary

state = next(iter(crime_data['results'].keys()))
values = next(iter(crime_data['results'].values()))
years = list(values.keys())
crime_values = list(values.values())

print(state, years, crime_values)
