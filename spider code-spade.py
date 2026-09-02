from dataclasses import dataclass
from typing import List, Optional


# ============================================================
# DATA MODEL
# ============================================================

@dataclass
class Incident:
    """
    Stores the information belonging to one incident.
    """

    incident_id: str
    incident_type: str
    location: str
    severity: int
    people_affected: int
    description: str
    distance: float
    route: str
    status: str = "REPORTED"


# ============================================================
# RESPONSE SYSTEM
# ============================================================

class ResponseSystem:
    """
    Contains the actual incident, priority and mission logic.

    The CommandCentre should NOT calculate priorities or
    manipulate incident business rules directly.
    """

    VALID_STATUSES = {
        "REPORTED",
        "IN_PROGRESS",
        "RESOLVED"
    }

    STATUS_ORDER = {
        "REPORTED": 0,
        "IN_PROGRESS": 1,
        "RESOLVED": 2
    }

    def __init__(self):
        self.incidents: List[Incident] = []
        self.next_id = 1

    # --------------------------------------------------------
    # Incident creation
    # --------------------------------------------------------

    def create_incident(
        self,
        incident_type: str,
        location: str,
        severity: int,
        people_affected: int,
        description: str,
        distance: float,
        route: str
    ) -> Incident:

        incident = Incident(
            incident_id=f"INC-{self.next_id:03d}",
            incident_type=incident_type,
            location=location,
            severity=severity,
            people_affected=people_affected,
            description=description,
            distance=distance,
            route=route
        )

        self.incidents.append(incident)
        self.next_id += 1

        return incident

    # --------------------------------------------------------
    # Incident lookup
    # --------------------------------------------------------

    def find_incident(self, incident_id: str) -> Optional[Incident]:
        """
        Find an incident by its ID.
        Returns None if it does not exist.
        """

        for incident in self.incidents:
            if incident.incident_id.upper() == incident_id.upper():
                return incident

        return None

    # --------------------------------------------------------
    # Active incidents
    # --------------------------------------------------------

    def get_active_incidents(self) -> List[Incident]:
        """
        Active incidents are everything that has NOT been resolved.
        """

        return [
            incident
            for incident in self.incidents
            if incident.status != "RESOLVED"
        ]

    # --------------------------------------------------------
    # Priority calculation
    # --------------------------------------------------------

    def calculate_priority(self, incident: Incident) -> int:
        """
        Calculates an incident priority score.

        Higher severity and more people affected increase priority.
        """

        priority = (
            incident.severity * 10
            + incident.people_affected * 5
        )

        return priority

    # --------------------------------------------------------
    # Mission score
    # --------------------------------------------------------

    def calculate_mission_score(self, incident: Incident) -> float:
        """
        Calculates how suitable an incident is for the next mission.

        Priority increases the score.
        Distance decreases the score.
        """

        priority = self.calculate_priority(incident)

        score = priority - incident.distance

        return round(score, 2)

    # --------------------------------------------------------
    # Response priority list
    # --------------------------------------------------------

    def get_response_priority(self) -> List[Incident]:
        """
        Returns active incidents sorted from highest priority
        to lowest priority.
        """

        active_incidents = self.get_active_incidents()

        return sorted(
            active_incidents,
            key=self.calculate_priority,
            reverse=True
        )

    # --------------------------------------------------------
    # Next mission
    # --------------------------------------------------------

    def get_next_mission(self) -> Optional[Incident]:
        """
        Returns the active incident with the highest mission score.

        Returns None if there are no active incidents.
        """

        active_incidents = self.get_active_incidents()

        if not active_incidents:
            return None

        return max(
            active_incidents,
            key=self.calculate_mission_score
        )

    # --------------------------------------------------------
    # Update status
    # --------------------------------------------------------

    def update_status(
        self,
        incident_id: str,
        new_status: str
    ) -> tuple[bool, str]:

        incident = self.find_incident(incident_id)

        if incident is None:
            return False, "Incident ID not found."

        new_status = new_status.upper()

        if new_status not in self.VALID_STATUSES:
            return False, "Invalid status."

        current_position = self.STATUS_ORDER[incident.status]
        new_position = self.STATUS_ORDER[new_status]

        # Status is only allowed to move forward.
        if new_position != current_position + 1:
            return (
                False,
                f"Invalid status change: "
                f"{incident.status} -> {new_status}"
            )

        incident.status = new_status

        return True, (
            f"{incident.incident_id} status updated to "
            f"{incident.status}."
        )

    # --------------------------------------------------------
    # Dashboard statistics
    # --------------------------------------------------------

    def get_dashboard(self) -> dict:
        """
        Creates the operational summary for the dashboard.
        """

        active = self.get_active_incidents()

        critical = [
            incident
            for incident in active
            if incident.severity >= 5
        ]

        in_progress = [
            incident
            for incident in self.incidents
            if incident.status == "IN_PROGRESS"
        ]

        resolved = [
            incident
            for incident in self.incidents
            if incident.status == "RESOLVED"
        ]

        return {
            "total_incidents": len(self.incidents),
            "active_incidents": len(active),
            "critical_incidents": len(critical),
            "in_progress": len(in_progress),
            "resolved": len(resolved)
        }


# ============================================================
# COMMAND CENTRE
# ============================================================

class CommandCentre:
    """
    Handles user interaction.

    It collects input, calls ResponseSystem methods,
    and displays results.

    It does NOT contain the business rules.
    """

    def __init__(self, response_system: ResponseSystem):
        self.response_system = response_system

    # --------------------------------------------------------
    # Main application
    # --------------------------------------------------------

    def run(self):
        """
        Main control loop.
        """

        self.show_startup()

        while True:
            self.show_menu()

            choice = input("\nChoose an option: ").strip()

            if choice == "":
                print("\nPlease enter an option.")
                continue

            if choice == "1":
                self.report_incident()

            elif choice == "2":
                self.view_active_incidents()

            elif choice == "3":
                self.view_response_priority()

            elif choice == "4":
                self.get_next_mission()

            elif choice == "5":
                self.update_incident()

            elif choice == "6":
                self.view_dashboard()

            elif choice == "7":
                self.exit_program()
                break

            else:
                print("\n❌ INVALID OPTION")
                print("Please select an option from the menu.")

    # --------------------------------------------------------
    # Startup
    # --------------------------------------------------------

    def show_startup(self):
        print("\n" + "=" * 60)
        print("🕷 SPIDER-MAN COMMAND CENTRE")
        print("=" * 60)
        print("Neighbourhood Response System")
        print()

    # --------------------------------------------------------
    # Main menu
    # --------------------------------------------------------

    def show_menu(self):
        print("\n" + "-" * 60)
        print("MAIN MENU")
        print("-" * 60)

        print("1. Report Incident")
        print("2. View Active Incidents")
        print("3. View Response Priority")
        print("4. Get Next Mission")
        print("5. Update Incident")
        print("6. View Dashboard")
        print("7. Exit")

    # --------------------------------------------------------
    # 1. Report incident
    # --------------------------------------------------------

    def report_incident(self):
        print("\n--- REPORT INCIDENT ---")

        incident_type = self.get_required_text("Incident type")
        if incident_type is None:
            return

        location = self.get_required_text("Location")
        if location is None:
            return

        severity = self.get_integer(
            "Severity (1-5)",
            minimum=1,
            maximum=5
        )

        if severity is None:
            return

        people_affected = self.get_integer(
            "People affected",
            minimum=0
        )

        if people_affected is None:
            return

        description = self.get_required_text("Description")
        if description is None:
            return

        distance = self.get_float(
            "Distance from Spider-Man (km)",
            minimum=0
        )

        if distance is None:
            return

        route = self.get_required_text("Route")
        if route is None:
            return

        incident = self.response_system.create_incident(
            incident_type=incident_type,
            location=location,
            severity=severity,
            people_affected=people_affected,
            description=description,
            distance=distance,
            route=route
        )

        print("\n✓ INCIDENT CREATED")
        print(f"Incident ID: {incident.incident_id}")

    # --------------------------------------------------------
    # 2. View active incidents
    # --------------------------------------------------------

    def view_active_incidents(self):
        print("\n--- ACTIVE INCIDENTS ---")

        incidents = self.response_system.get_active_incidents()

        if not incidents:
            print("No active incidents.")
            return

        for incident in incidents:
            self.display_incident(incident)

    # --------------------------------------------------------
    # 3. View response priority
    # --------------------------------------------------------

    def view_response_priority(self):
        print("\n--- RESPONSE PRIORITY ---")

        incidents = self.response_system.get_response_priority()

        if not incidents:
            print("No active incidents.")
            return

        for incident in incidents:
            priority = self.response_system.calculate_priority(
                incident
            )

            print(
                f"{incident.incident_id} | "
                f"Severity: {incident.severity} | "
                f"Location: {incident.location} | "
                f"Priority: {priority}"
            )

    # --------------------------------------------------------
    # 4. Get next mission
    # --------------------------------------------------------

    def get_next_mission(self):
        print("\n--- NEXT MISSION ---")

        incident = self.response_system.get_next_mission()

        if incident is None:
            print("No available mission.")
            return

        priority = self.response_system.calculate_priority(
            incident
        )

        mission_score = (
            self.response_system.calculate_mission_score(
                incident
            )
        )

        print(f"Incident : {incident.incident_id}")
        print(f"Location : {incident.location}")
        print(f"Priority : {priority}")
        print(f"Distance : {incident.distance} km")
        print(f"Score    : {mission_score}")
        print(f"Route    : {incident.route}")

    # --------------------------------------------------------
    # 5. Update incident
    # --------------------------------------------------------

    def update_incident(self):
        print("\n--- UPDATE INCIDENT ---")

        incident_id = self.get_required_text("Incident ID")

        if incident_id is None:
            return

        incident = self.response_system.find_incident(
            incident_id
        )

        if incident is None:
            print("\n❌ Invalid incident ID.")
            return

        print(f"\nCurrent status: {incident.status}")

        new_status = self.get_required_text(
            "New status (REPORTED / IN_PROGRESS / RESOLVED)"
        )

        if new_status is None:
            return

        success, message = self.response_system.update_status(
            incident_id,
            new_status
        )

        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n❌ {message}")

    # --------------------------------------------------------
    # 6. Dashboard
    # --------------------------------------------------------

    def view_dashboard(self):
        print("\n--- OPERATIONAL DASHBOARD ---")

        dashboard = self.response_system.get_dashboard()

        print(f"Total incidents : {dashboard['total_incidents']}")
        print(f"Active incidents: {dashboard['active_incidents']}")
        print(f"Critical        : {dashboard['critical_incidents']}")
        print(f"In progress     : {dashboard['in_progress']}")
        print(f"Resolved        : {dashboard['resolved']}")

    # --------------------------------------------------------
    # Display one incident
    # --------------------------------------------------------

    def display_incident(self, incident: Incident):
        priority = self.response_system.calculate_priority(
            incident
        )

        print("\n" + "-" * 45)
        print(f"ID              : {incident.incident_id}")
        print(f"Type            : {incident.incident_type}")
        print(f"Location        : {incident.location}")
        print(f"Severity        : {incident.severity}")
        print(f"People affected : {incident.people_affected}")
        print(f"Status          : {incident.status}")
        print(f"Priority        : {priority}")
        print(f"Description     : {incident.description}")

    # --------------------------------------------------------
    # Input helpers
    # --------------------------------------------------------

    def get_required_text(self, label: str) -> Optional[str]:
        """
        Gets text input and rejects empty input.
        """

        value = input(f"{label}: ").strip()

        if value == "":
            print("Input cannot be empty.")
            return None

        return value

    def get_integer(
        self,
        label: str,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None
    ) -> Optional[int]:

        value = input(f"{label}: ").strip()

        if value == "":
            print("Input cannot be empty.")
            return None

        try:
            number = int(value)
        except ValueError:
            print("Please enter a valid whole number.")
            return None

        if minimum is not None and number < minimum:
            print(f"Value must be at least {minimum}.")
            return None

        if maximum is not None and number > maximum:
            print(f"Value must be at most {maximum}.")
            return None

        return number

    def get_float(
        self,
        label: str,
        minimum: Optional[float] = None
    ) -> Optional[float]:

        value = input(f"{label}: ").strip()

        if value == "":
            print("Input cannot be empty.")
            return None

        try:
            number = float(value)
        except ValueError:
            print("Please enter a valid number.")
            return None

        if minimum is not None and number < minimum:
            print(f"Value must be at least {minimum}.")
            return None

        return number

    # --------------------------------------------------------
    # Exit
    # --------------------------------------------------------

    def exit_program(self):
        print("\nSpider-Man Command Centre shutting down.")
        print("Goodbye.")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

def main():
    response_system = ResponseSystem()
    command_centre = CommandCentre(response_system)

    command_centre.run()


if __name__ == "__main__":
    main()