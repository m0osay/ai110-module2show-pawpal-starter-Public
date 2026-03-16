"""Terminal demo for the PawPal+ scheduling logic."""

from pawpal_system import Owner, Pet, Task


def build_demo_owner() -> Owner:
    """Create sample data for a quick terminal test."""
    owner = Owner(name="Maya", available_minutes_per_day=90)

    luna = Pet(name="Luna", species="Dog", age=4)
    mochi = Pet(name="Mochi", species="Cat", age=2)

    luna.add_task(
        Task(
            description="Morning walk",
            time="08:00",
            frequency="daily",
            duration_minutes=30,
            priority="high",
            category="exercise",
        )
    )
    luna.add_task(
        Task(
            description="Breakfast",
            time="08:30",
            frequency="daily",
            duration_minutes=10,
            priority="high",
            category="feeding",
        )
    )
    mochi.add_task(
        Task(
            description="Give medication",
            time="09:00",
            frequency="daily",
            duration_minutes=5,
            priority="high",
            category="health",
        )
    )
    mochi.add_task(
        Task(
            description="Play session",
            time="18:00",
            frequency="daily",
            duration_minutes=20,
            priority="medium",
            category="enrichment",
        )
    )

    owner.add_pet(luna)
    owner.add_pet(mochi)
    return owner


def main() -> None:
    """Generate and print today's schedule."""
    owner = build_demo_owner()
    plan = owner.get_schedule()

    print("Today's Schedule")
    print("=" * 16)
    print(plan.display())


if __name__ == "__main__":
    main()
