"""Basic tests for the PawPal+ logic layer."""

from datetime import date

from pawpal_system import Pet, Task


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
