SEVERITY_SCORES = {
    "LOW": 10,
    "MEDIUM": 20,
    "HIGH": 30,
    "CRITICAL": 40,
}

LOCATION_SCORES = {
    "SCHOOL": 4,
    "HOSPITAL": 4,
    "RESIDENTIAL": 3,
    "PUBLIC": 2,
    "STREET": 1,
}

PEOPLE_MULTIPLIER = 2
def calculate_score(incident):
    """Calculates threat score using standard + and * operators."""
    severity_points = SEVERITY_SCORES[incident["severity"]]
    people_points = incident["people"] * PEOPLE_MULTIPLIER
    location_points = LOCATION_SCORES[incident["location"]]

    return severity_points + people_points + location_points

def get_active_incidents(incidents):
    """Filters out any incidents marked as RESOLVED."""
    active_incidents = []
    for incident in incidents:
        if incident["status"] != "RESOLVED":
            active_incidents.append(incident)
    return active_incidents

def has_higher_priority(incident_a, incident_b):
    """Compares two incidents to see if incident_a should come first."""
    score_a = calculate_score(incident_a)
    score_b = calculate_score(incident_b)

    if score_a > score_b:
        return True
    if score_a < score_b:
        return False

    if incident_a["people"] > incident_b["people"]:
        return True
    if incident_a["people"] < incident_b["people"]:
        return False

    if incident_a["order"] < incident_b["order"]:
        return True
    else:
        return False

def rank_incidents(incidents):
    """Sorts active incidents from highest to lowest priority using a simple bubble sort."""
    active_list = get_active_incidents(incidents)
    total_items = len(active_list)

    for i in range(total_items):
        for j in range(total_items - 1):
            
            if has_higher_priority(active_list[j + 1], active_list[j]):
                temp = active_list[j]
                active_list[j] = active_list[j + 1]
                active_list[j + 1] = temp

    return active_list


incidents = [
    {"id": "INC-001", "severity": "LOW", "people": 0, "location": "RESIDENTIAL", "status": "ACTIVE", "order": 1},
    {"id": "INC-002", "severity": "LOW", "people": 1, "location": "STREET", "status": "ACTIVE", "order": 2},
    {"id": "INC-003", "severity": "HIGH", "people": 3, "location": "SCHOOL", "status": "ACTIVE", "order": 3},
    {"id": "INC-004", "severity": "HIGH", "people": 3, "location": "HOSPITAL", "status": "ACTIVE", "order": 4},
    {"id": "INC-005", "severity": "CRITICAL", "people": 5, "location": "PUBLIC", "status": "ACTIVE", "order": 5},
    {"id": "INC-006", "severity": "MEDIUM", "people": 2, "location": "STREET", "status": "RESOLVED", "order": 6},
]

ranked = rank_incidents(incidents)



for incident in ranked:
    score = calculate_score(incident)
    print(incident["id"])
    print("Severity: " + incident["severity"])
    print("Location: " + incident["location"])
    print("People Affected: " + str(incident["people"]))
    print("Score: " + str(score))
    print("")

print("Best Incident: " + ranked[0]["location"])