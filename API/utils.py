# utils.py: Utility functions module

def count_sessions(events):
    """
    Counts user sessions based on login and logout events.
    A session is a time between one login and one logout.

    Args:
    events (list of tuples): Each tuple contains an event timestamp and event type.

    Returns:
    int: Number of sessions for a given user
    """
    session_count = 0
    session_start = None

    for timestamp, event_type in events:
        if event_type == 'login':
            session_start = timestamp
        elif event_type == 'logout' and session_start:
            if timestamp - session_start >= 1:  # Check if the session lasted at least 1 second
                session_count += 1
            session_start = None

    return session_count

def calculate_time_spent(events):
    """
    Calculates the total time spent in game based on pairs of login and logout events.

    Args:
    events (list of tuples): Each tuple contains an event timestamp and event type.

    Returns:
    int: Total time spent in the game in seconds.
    """
    total_time = 0
    session_start = None

    for timestamp, event_type in events:
        if event_type == 'login':
            session_start = timestamp
        elif event_type == 'logout' and session_start:
            session_end = timestamp
            session_duration = session_end - session_start
            total_time += session_duration
            session_start = None

    return total_time