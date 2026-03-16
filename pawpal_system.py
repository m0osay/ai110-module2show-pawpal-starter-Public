"""
PawPal+ — Logic Layer
Backend classes for the pet care scheduling system.
"""

from dataclasses import dataclass, field
from typing import List, Optional


PRIORITY_VALUES = {"low": 1, "medium": 2, "high": 3}


# ---------------------------------------------------------------------------
# Core domain classes
# ---------------------------------------------------------------------------


@dataclass
class Task:
    """
    Represents one pet-care activity.

    Required fields match the project prompt:
    - description
    - time
    - frequency
    - completion status

    Extra fields support the scheduler and demo UI.
    """

    description: str
    time: str
    frequency: str
    completed: bool = False
    duration_minutes: int = 15
    priority: str = "medium"
    category: str = "general"

    def __post_init__(self) -> None:
        """Validate task values after the dataclass initializes."""
        self.priority = self.priority.lower()
        if self.priority not in PRIORITY_VALUES:
            raise ValueError("priority must be 'low', 'medium', or 'high'")
        if self.duration_minutes <= 0:
            raise ValueError("duration_minutes must be greater than 0")

    @property
    def title(self) -> str:
        """Compatibility alias for older UI/code that still uses title."""
        return self.description

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not done yet."""
        self.completed = False

    def get_priority_value(self) -> int:
        """Return a numeric sort weight for this task."""
        return PRIORITY_VALUES[self.priority]

    def matches_frequency(self, frequency: str) -> bool:
        """Return True when the task uses the given frequency label."""
        return self.frequency.lower() == frequency.lower()

    def display(self) -> str:
        """Return a human-readable description of the task."""
        status = "done" if self.completed else "pending"
        return (
            f"{self.description} at {self.time} "
            f"({self.frequency}, {self.priority} priority, {status})"
        )


@dataclass
class Pet:
    """Stores one pet and the tasks assigned to that pet."""

    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, description: str) -> None:
        """Remove the first task whose description matches."""
        for index, task in enumerate(self.tasks):
            if task.description == description:
                del self.tasks[index]
                return

    def get_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return this pet's tasks, optionally hiding completed ones."""
        if include_completed:
            return list(self.tasks)
        return [task for task in self.tasks if not task.completed]

    def get_task(self, description: str) -> Optional[Task]:
        """Look up a task by description."""
        for task in self.tasks:
            if task.description == description:
                return task
        return None


class Owner:
    """Represents the user and manages all pets in the household."""

    def __init__(
        self,
        name: str,
        available_minutes_per_day: int,
        preferences: Optional[List[str]] = None,
    ) -> None:
        """Initialize an owner with their schedule constraints and pets."""
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.preferences: List[str] = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Return tasks from every pet this owner manages."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks

    def get_tasks_by_pet(self, include_completed: bool = True) -> dict[str, List[Task]]:
        """Return a mapping of pet name to that pet's task list."""
        return {
            pet.name: pet.get_tasks(include_completed=include_completed)
            for pet in self.pets
        }

    def get_schedule(self, pet_name: Optional[str] = None) -> "DailyPlan":
        """Build a schedule for one pet or the whole household."""
        scheduler = Scheduler(owner=self)
        return scheduler.build_plan(pet_name=pet_name)


# ---------------------------------------------------------------------------
# Scheduling output classes
# ---------------------------------------------------------------------------


@dataclass
class ScheduledItem:
    pet_name: str
    task: Task
    start_time: str
    end_time: str
    reason: str = ""

    def display(self) -> str:
        """Return a human-readable string for this scheduled item."""
        return (
            f"{self.start_time}-{self.end_time}  "
            f"{self.pet_name}: {self.task.description} "
            f"({self.task.priority} priority) - {self.reason}"
        )


class DailyPlan:
    def __init__(self, owner_name: str = "", pet_name: str = "All Pets") -> None:
        """Initialize an empty daily plan for an owner or selected pet."""
        self.owner_name = owner_name
        self.pet_name = pet_name
        self.items: List[ScheduledItem] = []
        self.skipped_tasks: List[tuple[str, Task]] = []
        self.total_minutes_used: int = 0
        self.summary: str = ""

    def add_item(self, item: ScheduledItem) -> None:
        """Append a scheduled item and update the running total."""
        self.items.append(item)
        self.total_minutes_used += item.task.duration_minutes

    def add_skipped(self, pet_name: str, task: Task) -> None:
        """Record a task that was excluded from the plan."""
        self.skipped_tasks.append((pet_name, task))

    def display(self) -> str:
        """Return the full plan as a formatted string."""
        if not self.items:
            return f"No tasks scheduled for {self.pet_name}."

        header = (
            f"Daily Plan for {self.pet_name} "
            f"(owner: {self.owner_name}, {self.total_minutes_used} min total)"
        )
        lines = [header, "-" * 40]
        lines.extend(item.display() for item in self.items)

        if self.skipped_tasks:
            skipped = ", ".join(
                f"{pet_name}: {task.description}" for pet_name, task in self.skipped_tasks
            )
            lines.append(f"Skipped (time ran out): {skipped}")

        if self.summary:
            lines.extend(["-" * 40, self.summary])

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------


class Scheduler:
    """The planner that retrieves, organizes, and schedules owner tasks."""

    def __init__(self, owner: Owner) -> None:
        """Store the owner whose pets and tasks will be scheduled."""
        self.owner = owner

    def get_all_tasks(self, include_completed: bool = False) -> List[tuple[str, Task]]:
        """Retrieve tasks from every pet through the Owner object."""
        tasks: List[tuple[str, Task]] = []
        for pet in self.owner.pets:
            for task in pet.get_tasks(include_completed=include_completed):
                tasks.append((pet.name, task))
        return tasks

    def get_tasks_for_pet(
        self, pet_name: str, include_completed: bool = False
    ) -> List[tuple[str, Task]]:
        """Retrieve tasks for one named pet."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            return []
        return [(pet.name, task) for task in pet.get_tasks(include_completed=include_completed)]

    def filter_tasks(
        self,
        tasks: List[tuple[str, Task]],
        threshold: str = "low",
        frequency: Optional[str] = None,
    ) -> List[tuple[str, Task]]:
        """Keep only tasks that meet the priority threshold and optional frequency."""
        minimum = PRIORITY_VALUES.get(threshold.lower(), PRIORITY_VALUES["low"])
        filtered: List[tuple[str, Task]] = []

        for pet_name, task in tasks:
            if task.completed:
                continue
            if task.get_priority_value() < minimum:
                continue
            if frequency is not None and not task.matches_frequency(frequency):
                continue
            filtered.append((pet_name, task))

        return filtered

    def sort_tasks(self, tasks: List[tuple[str, Task]]) -> List[tuple[str, Task]]:
        """Order tasks by time, then priority, then shorter duration."""
        return sorted(
            tasks,
            key=lambda entry: (
                entry[1].time,
                -entry[1].get_priority_value(),
                entry[1].duration_minutes,
                entry[0],
            ),
        )

    def build_plan(
        self,
        pet_name: Optional[str] = None,
        threshold: str = "low",
        frequency: Optional[str] = None,
        start_hour: int = 8,
    ) -> DailyPlan:
        """Build a daily plan for one pet or the whole household."""
        tasks = (
            self.get_tasks_for_pet(pet_name)
            if pet_name is not None
            else self.get_all_tasks()
        )

        plan_label = pet_name if pet_name is not None else "All Pets"
        plan = DailyPlan(owner_name=self.owner.name, pet_name=plan_label)
        candidates = self.sort_tasks(self.filter_tasks(tasks, threshold=threshold, frequency=frequency))

        time_remaining = self.owner.available_minutes_per_day
        current_minutes = start_hour * 60

        for current_pet_name, task in candidates:
            if task.duration_minutes > time_remaining:
                plan.add_skipped(current_pet_name, task)
                continue

            start_time = self._format_minutes(current_minutes)
            current_minutes += task.duration_minutes
            end_time = self._format_minutes(current_minutes)
            reason = (
                f"{task.frequency} task at {task.time}, "
                f"{time_remaining} min available before scheduling"
            )

            plan.add_item(
                ScheduledItem(
                    pet_name=current_pet_name,
                    task=task,
                    start_time=start_time,
                    end_time=end_time,
                    reason=reason,
                )
            )
            time_remaining -= task.duration_minutes

        plan.summary = self.explain_plan(plan)
        return plan

    def explain_plan(self, plan: DailyPlan) -> str:
        """Generate a plain-language explanation of the plan."""
        if not plan.items:
            return "No tasks fit within the available time today."

        scheduled = ", ".join(
            f"{item.pet_name}: {item.task.description}" for item in plan.items
        )
        summary = (
            f"{self.owner.name} has {self.owner.available_minutes_per_day} minutes available today. "
            f"Scheduled tasks: {scheduled}. "
            f"Tasks were retrieved from the owner's pets, filtered to incomplete items, "
            f"then ordered by time, priority, and duration."
        )

        if plan.skipped_tasks:
            skipped = ", ".join(
                f"{pet_name}: {task.description}" for pet_name, task in plan.skipped_tasks
            )
            summary += f" Skipped because time ran out: {skipped}."

        return summary

    @staticmethod
    def _format_minutes(total_minutes: int) -> str:
        """Convert a minute count into HH:MM 24-hour time."""
        hour = total_minutes // 60
        minute = total_minutes % 60
        return f"{hour:02d}:{minute:02d}"
