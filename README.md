# Air Quality Checker
This project is a Python-based application that provides air quality information for user-specified locations. 
Users can check air quality ratings near their current location, within a specified range, or for any chosen location worldwide. 
Data is retrieved and processed from APIs like PurpleAir and Nominatim, allowing users to filter results based on specific parameters.

Features
- Retrieve real-time air quality data for any location or region.
- Filter data based on range, air quality threshold, and maximum results.
- Display data in a structured, readable format, including AQI and geographical coordinates.
- Option to use either APIs (PurpleAir, Nominatim) or local files for data retrieval.

Usage
Run the program by executing the main script. You will be prompted to provide the following details:

- Center: Specify a center location in the format (NOMINATIM <location> or FILE <path>).
- Range: The search radius in miles.
- Threshold: AQI threshold for filtering results.
- Max Results: The maximum number of results to display.
- AQI Source: Specify PURPLEAIR <api_key> or FILE <path> for air quality data.
- Reverse Source: Specify NOMINATIM <location> or FILES <list_of_paths> for reverse location lookup.


Project Structure

- api_classes.py: Handles API requests to PurpleAir and Nominatim, including data collection and filtering.
- file_classes.py: Manages file-based data retrieval and processing, allowing users to access data without relying on live API calls.
- functions_page.py: Contains helper functions for AQI calculations, distance measurement, data sorting, and display formatting.
- user_class.py: Manages user inputs and validates sources (e.g., API or file) for retrieving AQI data.
