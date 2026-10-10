"""Exercise 2: space mission with a nested list of crew members."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Crew ranks."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """One crew member, validated on its own before the mission."""

    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """A mission and its crew. Each crew item is a CrewMember model."""

    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_safety_requirements(self) -> "SpaceMission":
        """Safety rules that need the whole crew list."""
        leading_ranks = (Rank.COMMANDER, Rank.CAPTAIN)
        leaders = [m for m in self.crew if m.rank in leading_ranks]
        experienced = [m for m in self.crew if m.years_experience >= 5]
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        if not leaders:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365 and len(experienced) * 2 < len(self.crew):
            raise ValueError(
                "Long missions (> 365 days) need 50% experienced crew "
                "(5+ years)"
            )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def display_mission(mission: SpaceMission) -> None:
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")


def display_errors(error: ValidationError) -> None:
    for detail in error.errors():
        print(detail["msg"].removeprefix("Value error, "))


def main() -> None:
    """Show a valid mission, then one without a Commander or Captain."""
    separator = "=" * 41
    launch_date = datetime(2024, 9, 1, 8, 0)

    print("Space Mission Crew Validation")
    print(separator)
    try:
        mars_crew = [
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=45,
                specialization="Mission Command",
                years_experience=20,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=36,
                specialization="Navigation",
                years_experience=9,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=29,
                specialization="Engineering",
                years_experience=4,
            ),
        ]
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=launch_date,
            duration_days=900,
            crew=mars_crew,
            budget_millions=2500.0,
        )
        print("Valid mission created:")
        display_mission(mission)
    except ValidationError as error:
        display_errors(error)

    print()
    print(separator)
    print("Expected validation error:")
    try:
        leaderless_crew = [
            CrewMember(
                member_id="CM004",
                name="Mark Watney",
                rank=Rank.LIEUTENANT,
                age=38,
                specialization="Botany",
                years_experience=10,
            ),
            CrewMember(
                member_id="CM005",
                name="Ellen Ripley",
                rank=Rank.OFFICER,
                age=33,
                specialization="Flight Operations",
                years_experience=7,
            ),
        ]
        SpaceMission(
            mission_id="M2024_LUNA",
            mission_name="Lunar Outpost Resupply",
            destination="Moon",
            launch_date=launch_date,
            duration_days=120,
            crew=leaderless_crew,
            budget_millions=450.0,
        )
        print("No validation error was raised")
    except ValidationError as error:
        display_errors(error)


if __name__ == "__main__":
    main()
