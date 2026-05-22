def calculate_score(
    looking_away,
    tab_switching
):

    score = 0

    # Looking Away
    if looking_away:
        score += 50

    # Tab Switching
    if tab_switching:
        score += 50

    return score