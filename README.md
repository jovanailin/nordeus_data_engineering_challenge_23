# Nordeus Data Engineering Challenge 2023

## Overview

### API Endpoints

#### User Statistics
- Endpoint: `/user_stats`
- Method: `GET`
- Parameters:
-- user_id (required)
-- date (optional)
- Description: Fetches statistics for a specified user. If date is provided, statistics are for that date; otherwise, all-time stats are returned.
