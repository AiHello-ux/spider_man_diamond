graph = {
    ("Queens Street", "City Hospital"): 6,
    ("City Hospital", "Queens Street"): 6,
    ("Queens Street", "Midtown School"): 4,
    ("Midtown School", "Queens Street"): 4
}

def mission():
    start = "Queens Street"

    incidents = [
        ("City Hospital", 50),
        ("Midtown School", 40)
    ]

    best = ""
    best_score = 0

    for place, priority in incidents:

        if start == place:
            distance = 0
        else:
            distance = graph[(start, place)]

        score = priority - distance

        print(place)
        print("Distance:", distance)
        print("Priority:", priority)
        print("Mission Score:", score)
        print()

        if score > best_score:
            best_score = score
            best = place

    print("Best Mission:", best)

mission()