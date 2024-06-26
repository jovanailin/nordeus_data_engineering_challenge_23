# Nordeus Data Engineering Challenge 2023

## Overview

As part of the Nordeus Data Engineering Challenge, this project brings together an ETL notebook, API implementation, and a REST API. The ETL notebook efficiently processes data for use in the API, which interacts with a PostgreSQL database to ensure quick and precise data access. Hosted on Heroku, the REST API features endpoints for detailed user and game statistics. This setup ensures a seamless flow from data processing to end-user accessibility.

### Data Preprocessing

- The ETL notebook in the repository outlines the data extraction, transformation, and loading process.
- The data is initially extracted from a JSON file, processed, and cleaned to ensure accuracy and relevance.
- Key operations in the transformation include normalization of nested JSON structures and the segregation of data into distinct categories for detailed analysis.
- The cleaned and structured data is then loaded into a PostgreSQL database, which the API queries.

### API Implementation Details
- The API, housed in the `/API` directory of the repository, is built using Flask. It serves as the interface for querying the processed data. The implementation details are as follows:
- Structure: The API codebase is organized in the /API directory, which contains all necessary Flask routes and database interaction logic.
- Functionality: It features two main routes `(/user_stats` and `/game_stats)` that allow users to fetch detailed user and game statistics.
- Database Integration: The API interacts with a PostgreSQL database, querying data that has been pre-processed and stored, ensuring efficient data retrieval.
- Deployment: Deployed on Heroku, the API is accessible for real-time data querying and can handle requests with various parameters.

### API Endpoints

#### User Statistics
- Endpoint: `/user_stats`
- Method: `GET`
- Parameters:
  - user_id (required)
  - date (optional)
- Description: Fetches statistics for a specified user. If date is provided, statistics are for that date; otherwise, all-time stats are returned.


#### Game Statistics
- Endpoint: `/game_stats`
- Method: `GET`
- Parameters:
  - date (optional)
  - country (optional)
- Description: Retrieves game-related statistics. Filters by date and/or country if provided.

#### Local Setup
- Clone the repository.
- Install dependencies: `pip install -r requirements.txt`.
- Run the Flask app: `python app.py`.


