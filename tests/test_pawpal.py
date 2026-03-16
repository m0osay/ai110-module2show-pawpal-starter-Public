"""Basic tests for the PawPal+ logic layer."""

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
