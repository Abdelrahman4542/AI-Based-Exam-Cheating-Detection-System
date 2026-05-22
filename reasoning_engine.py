def analyze_behavior(looking_away, tab_switching):

    # Rule-Based Reasoning
    if looking_away and tab_switching:
        return "Suspicious Behavior Detected"

    elif looking_away:
        return "Warning: Looking Away"

    else:
        return "Normal Behavior"