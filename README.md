# fbi-data-web-dashboard

This Python script defines a web application using the Flask framework. The application interacts with the FBI Crime Data API to retrieve and display crime statistics for different states and years. The application has features for user authentication, data retrieval, and visualization.

Login mechanism: Users submit a username and password via a login form. The application checks credentials against a CSV file (userdetails.txt). A maximum login attempts threshold is implemented.

**Imports:***

    •  csv: Used for reading CSV files.
    •  json: Used for working with JSON data.
    •  requests: Used for making HTTP requests to the FBI Crime Data API. 
    •  matplotlib: Used for creating visualizations (plots).
    •  Flask: The web framework for building the application. Other Flask-related modules for rendering templates, handling requests, etc.


**Configuration:**

    •  The API endpoint (api_url) for the FBI Crime Data API is specified. This stays constant.
    •  Flask app is initialized. Maximum login attempts threshold (MAX_LOGIN_ATTEMPTS) is defined to prevent potential “unathorized” access.
    •  List of U.S. states (us_states_list) is provided to ensure I can extract only the state name from the data provided by FBI.


**Functions:**

    •  get_data(link): Sends a GET request to the FBI Crime Data API with the specified link and returns the JSON response.
    •  fetch_data(): Retrieves crime data based on user input (selected states, offense, and date range).


**Routes:**

    •  /login: Handles user login. Reads user details from a CSV file (userdetails.txt) and validates credentials.
    •  /home: Main page after login. Allows users to choose between viewing data or visualizations.
    •  /home/data: Displays crime data based on user input.
    •  /home/visualization: Generates and displays crime data visualizations using Matplotlib.


**Data Retrieval and Visualization:**

    •  Users can select states, an offense type, and a date range to fetch crime data.
    •  The application retrieves and displays the data or generates visualizations (plots) based on the selected parameters.

•  Matplotlib is used to create line plots, with each state represented by a different color.

**Run the Application:**

The application runs on localhost (http://127.0.0.1) at port 5000 in debug mode.
