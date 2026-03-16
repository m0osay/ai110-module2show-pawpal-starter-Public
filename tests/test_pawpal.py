"""Basic tests for the PawPal+ logic layer."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task(description="Evening walk", time="18:00", frequency="daily")

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(name="Luna", species="Dog", age=4)
    task = Task(description="Breakfast", time="08:00", frequency="daily")

    pet.add_task(task)

    assert len(pet.tasks) == 1


def test_mark_task_complete_creates_next_daily_occurrence() -> None:
    pet = Pet(name="Mochi", species="Cat", age=2)
    task = Task(
        description="Give medication",
        time="09:00",
        frequency="daily",
        due_date=date(2026, 3, 15),
    )
    pet.add_task(task)

    next_task = pet.mark_task_complete("Give medication")

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 3, 16)
    assert len(pet.tasks) == 2


def test_mark_task_complete_creates_next_weekly_occurrence() -> None:
    pet = Pet(name="Luna", species="Dog", age=4)
    task = Task(
        description="Bath",
        time="10:00",
        frequency="weekly",
        due_date=date(2026, 3, 15),
    )
    pet.add_task(task)

    next_task = pet.mark_task_complete("Bath")

    assert next_task is not None
    assert next_task.due_date == date(2026, 3, 22)


def test_sort_by_time_returns_tasks_in_chronological_order() -> None:
    owner = Owner(name="Jordan", available_minutes_per_day=60)
    scheduler = Scheduler(owner)
    tasks = [
        Task(description="Lunch", time="12:00", frequency="daily"),
        Task(description="Morning walk", time="08:00", frequency="daily"),
        Task(description="Medication", time="09:30", frequency="daily"),
    ]

    sorted_tasks = scheduler.sort_by_time(tasks)

    assert [task.time for task in sorted_tasks] == ["08:00", "09:30", "12:00"]


def test_detect_conflicts_flags_duplicate_task_times() -> None:
    owner = Owner(name="Jordan", available_minutes_per_day=60)
    luna = Pet(name="Luna", species="Dog", age=4)
    mochi = Pet(name="Mochi", species="Cat", age=2)

    luna.add_task(Task(description="Breakfast", time="08:30", frequency="daily"))
    mochi.add_task(Task(description="Play session", time="08:30", frequency="daily"))
    owner.add_pet(luna)
    owner.add_pet(mochi)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(scheduler.get_all_tasks())

    assert len(conflicts) == 1
    assert "08:30" in conflicts[0]
    assert "Luna: Breakfast" in conflicts[0]
    assert "Mochi: Play session" in conflicts[0]
