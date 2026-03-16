"""Terminal demo for the PawPal+ scheduling logic."""

from pawpal_system import Owner, Pet, Scheduler, Task


def build_demo_owner() -> Owner:
    """Create sample data for a quick terminal test."""
    owner = Owner(name="Maya", available_minutes_per_day=90)

    luna = Pet(name="Luna", species="Dog", age=4)
    mochi = Pet(name="Mochi", species="Cat", age=2)

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
    mochi.add_task(
        Task(
            description="Play session",
            time="08:30",
            frequency="daily",
            duration_minutes=20,
            priority="medium",
            category="enrichment",
        )
    )
    medication = Task(
        description="Give medication",
        time="09:00",
        frequency="daily",
        duration_minutes=5,
        priority="high",
        category="health",
    )
    medication.mark_complete()
    mochi.add_task(medication)

    owner.add_pet(luna)
    owner.add_pet(mochi)
    return owner


def print_task_list(title: str, tasks: list[Task]) -> None:
    """Print a compact list of task descriptions for terminal checks."""
    print(title)
    print("-" * len(title))
    for task in tasks:
        print(f"{task.time} | {task.display()}")
    print()


def print_task_pairs(title: str, task_pairs: list[tuple[str, Task]]) -> None:
    """Print pet-task pairs for filtered terminal checks."""
    print(title)
    print("-" * len(title))
    for pet_name, task in task_pairs:
        print(f"{pet_name}: {task.time} | {task.display()}")
    print()


def main() -> None:
    """Generate and print today's schedule."""
    owner = build_demo_owner()
    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    mochi_pending_tasks = scheduler.filter_tasks_by(
        pet_name="Mochi",
        include_completed=False,
    )
    plan = owner.get_schedule()

    print_task_list("Sorted Tasks", sorted_tasks)
    print_task_pairs("Mochi Pending Tasks", mochi_pending_tasks)

    print("Today's Schedule")
    print("=" * 16)
    print(plan.display())


if __name__ == "__main__":
    main()
