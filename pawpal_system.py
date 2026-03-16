"""
PawPal+ — Logic Layer
Backend classes for the pet care scheduling system.
"""

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data classes (plain data holders — no heavy logic)
# ---------------------------------------------------------------------------

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str          # "low" | "medium" | "high"
    category: str = "general"   # "walk" | "feed" | "meds" | "grooming" | etc.
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def get_priority_value(self) -> int:
        """Return a numeric weight so tasks can be sorted: high=3, medium=2, low=1."""
        return {"low": 1, "medium": 2, "high": 3}.get(self.priority, 0)


@dataclass
class Pet:
    name: str
    species: str           # "dog" | "cat" | "other"
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a task by title (first match)."""
        self.tasks = [t for t in self.tasks if t.title != title]

    def get_tasks(self) -> List[Task]:
        """Return all tasks assigned to this pet."""
        return self.tasks


@dataclass
class ScheduledItem:
    task: Task
    start_time: str        # e.g. "08:00"
    end_time: str          # e.g. "08:20"
    reason: str = ""

    def display(self) -> str:
        """Return a human-readable string for this scheduled item."""
        return f"{self.start_time}–{self.end_time}  {self.task.title} ({self.task.priority} priority) — {self.reason}"


# ---------------------------------------------------------------------------
# Richer classes (hold references + contain real logic)
# ---------------------------------------------------------------------------

class Owner:
    def __init__(self, name: str, available_minutes_per_day: int, preferences: Optional[List[str]] = None):
        self.name = name
        self.available_minutes_per_day = available_minutes_per_day
        self.preferences: List[str] = preferences or []
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_schedule(self, pet: Pet) -> "DailyPlan":
        """Ask the scheduler to build a plan for the given pet."""
        scheduler = Scheduler(owner=self, pet=pet)
        return scheduler.build_plan()


class DailyPlan:
    def __init__(self) -> None:
        self.items: List[ScheduledItem] = []
        self.total_minutes_used: int = 0
        self.summary: str = ""

    def add_item(self, item: ScheduledItem) -> None:
        """Append a scheduled item and update the running total."""
        self.items.append(item)
        self.total_minutes_used += item.task.duration_minutes

    def display(self) -> str:
        """Return the full plan as a formatted string."""
        if not self.items:
            return "No tasks scheduled for today."
        lines = [f"Daily Plan ({self.total_minutes_used} min total)", "-" * 40]
        lines += [item.display() for item in self.items]
        if self.summary:
            lines += ["-" * 40, self.summary]
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet) -> None:
        self.owner = owner
        self.pet = pet
        self.available_time = owner.available_minutes_per_day

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted highest priority first."""
        return sorted(tasks, key=lambda t: t.get_priority_value(), reverse=True)

    def filter_by_priority(self, threshold: str = "low") -> List[Task]:
        """Return only incomplete tasks at or above the given priority threshold."""
        min_value = {"low": 1, "medium": 2, "high": 3}.get(threshold, 1)
        return [t for t in self.pet.get_tasks() if not t.completed and t.get_priority_value() >= min_value]

    def build_plan(self) -> DailyPlan:
        """
        Build a daily plan that fits within the owner's available time.
        Tasks are picked in priority order until time runs out.
        """
        plan = DailyPlan()
        candidates = self.sort_tasks(self.filter_by_priority("low"))
        time_remaining = self.available_time

        # Simple start at 8:00 AM and pack tasks back-to-back
        current_hour, current_minute = 8, 0

        for task in candidates:
            if task.duration_minutes > time_remaining:
                continue  # skip tasks that no longer fit

            start = f"{current_hour:02d}:{current_minute:02d}"
            total_minutes = current_hour * 60 + current_minute + task.duration_minutes
            end = f"{total_minutes // 60:02d}:{total_minutes % 60:02d}"
            reason = f"priority={task.priority}, fits in remaining {time_remaining} min"

            plan.add_item(ScheduledItem(task=task, start_time=start, end_time=end, reason=reason))

            current_hour, current_minute = total_minutes // 60, total_minutes % 60
            time_remaining -= task.duration_minutes

        plan.summary = self.explain_plan(plan)
        return plan

    def explain_plan(self, plan: DailyPlan) -> str:
        """Generate a plain-language summary of why tasks were chosen."""
        if not plan.items:
            return "No tasks fit within the available time today."
        chosen = ", ".join(item.task.title for item in plan.items)
        return (
            f"{self.owner.name} has {self.owner.available_minutes_per_day} min available today. "
            f"Scheduled for {self.pet.name}: {chosen}. "
            f"Tasks were ordered by priority (high → low) and packed until time ran out."
        )
