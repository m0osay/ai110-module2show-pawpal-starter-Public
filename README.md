# PawPal+ (Module 2 Project)

<a href="/course_images/ai110/img.png" target="_blank"><img src='/course_images/ai110/img.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

PawPal+ includes a small but meaningful scheduling layer designed to help a pet owner stay organized:

- **Sorting by time:** Tasks are ordered by `HH:MM` so the daily plan is generated in chronological order even if tasks were entered out of sequence.
- **Filtering by pet and status:** The scheduler can focus on one pet at a time and hide completed tasks so the owner sees what still needs attention.
- **Priority-aware scheduling:** When multiple tasks exist, the planner sorts by time, then priority, then shorter duration to build a more practical daily plan.
- **Daily and weekly recurrence:** Completing a recurring task automatically creates the next occurrence using the correct next due date.
- **Conflict warnings:** If two tasks request the same time slot, the scheduler raises a warning instead of failing, helping the owner adjust the schedule.
- **Skipped-task reporting:** If the owner runs out of available time, unscheduled tasks are recorded and shown instead of disappearing silently.
- **Readable schedule output:** The app presents sorted task tables, schedule summaries, and warnings through the Streamlit interface.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The current tests cover core scheduler behaviors including task completion, adding tasks to pets, chronological sorting, recurring daily and weekly task creation, and lightweight conflict detection for duplicate times.

Confidence Level: `★★★★☆` (4/5) based on the current passing test results and coverage of the main happy paths plus a few important edge cases.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
