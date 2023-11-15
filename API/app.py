from flask import Flask, jsonify, request
from datetime import datetime, timezone
from db import create_db_connection
from utils import count_sessions, calculate_time_spent

app = Flask(__name__)

@app.route('/user_stats', methods=['GET'])
def user_stats():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    conn = create_db_connection()

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    try:
        with conn.cursor() as cursor:
            # Fetch user information
            cursor.execute("""
                SELECT r.country, r.name
                FROM registration r 
                WHERE r.user_id = %s
            """, (user_id,))
            user_info = cursor.fetchone()
            if not user_info:
                return jsonify({"error": "User not found"}), 404

            country, name = user_info

            # Process logic for specific date or all-time stats

            query_date = "AND DATE(to_timestamp(event_timestamp)) = %s" if date else ""
            input_date = datetime.strptime(date, '%Y-%m-%d').date() if date else None

            # Fetch user activity
            cursor.execute(f"""
                SELECT event_timestamp, event_type
                FROM user_activity
                WHERE user_id = %s {query_date}
                ORDER BY event_timestamp
            """, (user_id,) if not date else (user_id, input_date))

            events = cursor.fetchall()
            number_of_sessions = count_sessions(events)
            time_spent = calculate_time_spent(events)

            # Determine the reference date for calculating days since last login
            if date:
                last_date = datetime.strptime(date, '%Y-%m-%d')
                last_date = last_date.replace(tzinfo=timezone.utc)
            else:
                # Fetch the most recent date from the dataset
                cursor.execute("""
                    SELECT MAX(to_timestamp(event_timestamp))
                    FROM user_activity
                """)
                last_date = cursor.fetchone()[0]

            # Fetch number of logins and last login date
            cursor.execute("""
                SELECT COUNT(*), MAX(to_timestamp(event_timestamp))
                FROM user_activity
                WHERE user_id = %s AND event_type = 'login'
            """, (user_id,))
            num_logins, last_login_timestamp = cursor.fetchone()

            # Calculate days since last login
            days_since_last_login = 0
            if last_login_timestamp:
                days_diff = (last_date - last_login_timestamp).days
                days_since_last_login = days_diff if days_diff >= 0 else 0

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({
        "country": country,
        "name": name,
        "number_of_logins": num_logins,
        "days_since_last_login": days_since_last_login,
        "number_of_sessions": number_of_sessions,
        "time_spent_in_game_in_seconds": time_spent
    })


@app.route('/game_stats', methods=['GET'])
def game_stats():
    date = request.args.get('date')
    country = request.args.get('country')
    conn = create_db_connection()

    try:
        with conn.cursor() as cursor:
            # Build base query
            base_query = """
                FROM user_activity ua
                LEFT JOIN registration r ON ua.user_id = r.user_id
                LEFT JOIN transaction t ON ua.user_id = t.user_id
            """

            # Add conditions for date and country
            where_conditions = []
            if date:
                input_date = datetime.strptime(date, '%Y-%m-%d').date()
                where_conditions.append(f"DATE(to_timestamp(ua.event_timestamp)) = '{input_date}'")
            if country:
                where_conditions.append(f"r.country = '{country}'")

            where_clause = 'WHERE ' + ' AND '.join(where_conditions) if where_conditions else ''

            # Query for daily active users and logins
            cursor.execute(f"""
                SELECT COUNT(DISTINCT ua.user_id) as daily_active_users,
                       COUNT(CASE WHEN ua.event_type = 'login' THEN 1 END) as logins
                {base_query}
                {where_clause}
            """)
            daily_stats_result = cursor.fetchone()
            daily_stats = {'daily_active_users': daily_stats_result[0], 'logins': daily_stats_result[1]}

            # Query for total revenue and paid users
            cursor.execute(f"""
                SELECT SUM(CASE 
                               WHEN t.transaction_currency = 'EUR' THEN t.transaction_amount * 1.3 
                               ELSE t.transaction_amount 
                           END) as total_revenue,
                       COUNT(DISTINCT t.user_id) as paid_users
                {base_query}
                {where_clause}
            """)
            financial_stats_result = cursor.fetchone()
            financial_stats = {'total_revenue': financial_stats_result[0], 'paid_users': financial_stats_result[1]}

            # Average numbers of sessions
            cursor.execute(f"""
                SELECT AVG(session_count) FROM
                    (SELECT user_id, COUNT(*) as session_count FROM
                        user_activity
                        WHERE event_type = 'login'
                        GROUP BY user_id) as user_sessions
                    WHERE session_count > 0""")


            avg_sessions_result = cursor.fetchall()
            avg_sessions = {'avg_sessions': float(avg_sessions_result[0][0])}

            # Averagime total time spent in game
            cursor.execute("SELECT event_timestamp, event_type FROM user_activity")
            events = cursor.fetchall()

            total_time_spent = calculate_time_spent(events)

            cursor.execute("SELECT user_id FROM user_activity")
            users = cursor.fetchall()[0]

            user_count = len(users)

            # Calculate average time spent
            average_time_result = total_time_spent / user_count if user_count > 0 else 0
            average_time = {"average_time_spent_in_game: " : average_time_result}
            # Combine results
            stats = {**daily_stats, **financial_stats, **avg_sessions, **average_time}

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify(stats)

if __name__ == '__main__':
    app.run()
