"""Exercise 1: alien contact reports with custom validation rules."""

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """Allowed contact types."""

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """A contact report with rules that depend on several fields."""

    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_business_rules(self) -> "AlienContact":
        """Business rules, checked once the fields are valid."""
        is_physical = self.contact_type == ContactType.PHYSICAL
        is_telepathic = self.contact_type == ContactType.TELEPATHIC
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')
        if is_physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if is_telepathic and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


def display_contact(contact: AlienContact) -> None:
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")


def display_errors(error: ValidationError) -> None:
    for detail in error.errors():
        print(detail["msg"].removeprefix("Value error, "))


def main() -> None:
    """Show one valid report and one that breaks a rule."""
    separator = "=" * 38
    radio_report: dict[str, Any] = {
        "contact_id": "AC_2024_001",
        "timestamp": "2024-03-15T22:30:00",
        "location": "Area 51, Nevada",
        "contact_type": "radio",
        "signal_strength": 8.5,
        "duration_minutes": 45,
        "witness_count": 5,
        "message_received": "Greetings from Zeta Reticuli",
    }
    telepathic_report: dict[str, Any] = {
        "contact_id": "AC_2024_002",
        "timestamp": "2024-03-16T03:10:00",
        "location": "Roswell, New Mexico",
        "contact_type": "telepathic",
        "signal_strength": 4.2,
        "duration_minutes": 12,
        "witness_count": 1,
    }

    print("Alien Contact Log Validation")
    print(separator)
    try:
        contact = AlienContact(**radio_report)
        print("Valid contact report:")
        display_contact(contact)
    except ValidationError as error:
        display_errors(error)

    print()
    print(separator)
    print("Expected validation error:")
    try:
        AlienContact(**telepathic_report)
        print("No validation error was raised")
    except ValidationError as error:
        display_errors(error)


if __name__ == "__main__":
    main()
