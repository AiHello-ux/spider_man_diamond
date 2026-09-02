from datetime import datetime

# This list stores all incidents
incidents = []


# Allowed incident types
types = [
    "Robbery",
    "Accident",
    "Fire",
    "Medical Emergency",
    "Missing Person",
    "Suspicious Activity"
]

# Allowed locations
locations = [
    "Queens Street",
    "Midtown School",
    "City Hospital",
    "Park Avenue",
    "Queens Residence",
    "Central Mall",
    "Police Station",
    "Metro Station"
]

# Allowed severity levels
severities = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


# Function to report a new incident
def report_incident():

    print("\n--- REPORT INCIDENT ---")

    # Ask for incident type
    while True:
        incident_type = input("Enter incident type: ").strip()

        if incident_type.lower() in [x.lower() for x in types]:
            # Convert it to the correct spelling
            for x in types:
                if incident_type.lower() == x.lower():
                    incident_type = x
            break
        else:
            print("Invalid incident type. Try again.")

    # Ask for location
    while True:
        location = input("Enter location: ").strip()

        if location.lower() in [x.lower() for x in locations]:
            for x in locations:
                if location.lower() == x.lower():
                    location = x
            break
        else:
            print("Invalid location. Try again.")

    # Ask for severity
    while True:
        severity = input("Enter severity: ").strip().upper()

        if severity in severities:
            break
        else:
            print("Invalid severity. Use LOW, MEDIUM, HIGH or CRITICAL.")

    # Ask for number of people
    while True:
        try:
            people = int(input("Enter people affected: "))

            if people >= 0:
                break
            else:
                print("Number cannot be negative.")

        except:
            print("Please enter a number.")

    # Ask for description
    while True:
        description = input("Enter description: ").strip()

        if description != "":
            break
        else:
            print("Description cannot be empty.")

    # Check for duplicate incident
    for old_incident in incidents:

        if (old_incident["type"] == incident_type and
                old_incident["location"] == location):

            print("\n⚠ POSSIBLE DUPLICATE!")
            print("Existing incident:", old_incident["id"])

            answer = input("Continue anyway? (yes/no): ").lower()

            if answer != "yes":
                print("Incident cancelled.")
                return

    # Create incident ID
    number = len(incidents) + 1
    incident_id = "INC-" + str(number).zfill(3)

    # Get current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create the incident
    incident = {
        "id": incident_id,
        "type": incident_type,
        "location": location,
        "severity": severity,
        "people": people,
        "description": description,
        "time": current_time,
        "status": "REPORTED"
    }

    # Store the incident
    incidents.append(incident)

    print("\n✓ INCIDENT CREATED")
    print("ID:", incident_id)
    print("Status: REPORTED")


# Function to find an incident
def find_incident():

    print("\n--- FIND INCIDENT ---")

    id = input("Enter incident ID: ").upper()

    for incident in incidents:

        if incident["id"] == id:

            print("\n--- INCIDENT DETAILS ---")
            print("ID:", incident["id"])
            print("Type:", incident["type"])
            print("Location:", incident["location"])
            print("Severity:", incident["severity"])
            print("People affected:", incident["people"])
            print("Description:", incident["description"])
            print("Time:", incident["time"])
            print("Status:", incident["status"])

            return

    print("Incident not found.")


# Function to show all incidents
def show_all():

    print("\n--- ALL INCIDENTS ---")

    if len(incidents) == 0:
        print("No incidents available.")
        return

    for incident in incidents:

        print(
            incident["id"],
            "|",
            incident["type"],
            "|",
            incident["location"],
            "|",
            incident["severity"]
        )


# Main program
def main():

    while True:

        print("\n==============================")
        print(" SPIDER-MAN INCIDENT SYSTEM")
        print("==============================")

        print("1. Report Incident")
        print("2. Find Incident")
        print("3. Show All Incidents")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            report_incident()

        elif choice == "2":
            find_incident()

        elif choice == "3":
            show_all()

        elif choice == "4":
            print("Program ended.")
            break

        else:
            print("Invalid choice.")


# Start the program
main()