# Nordeus Data Engineering Challenge 2023

## Overview

This project provides a REST API to process and query data related to user and game statistics. The API is built using Flask and deployed on Heroku.

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

#### How to Use
- API is live at: (https://shielded-lake-74666.herokuapp.com/)
- Make GET requests to the endpoints with the required parameters.

#### Local Setup
- Clone the repository.
- Install dependencies: `pip install -r requirements.txt`.
- Run the Flask app: `python app.py`.

- 
