# PawPal+ UML Class Diagram

```mermaid
classDiagram
    class Owner {
        +String name
        +int available_minutes_per_day
        +List~String~ preferences
        +add_pet(pet: Pet) void
        +get_schedule() DailyPlan
    }

    class Pet {
        +String name
        +String species
        +int age
        +List~Task~ tasks
        +add_task(task: Task) void
        +remove_task(title: String) void
        +get_tasks() List~Task~
    }

    class Task {
        +String title
        +int duration_minutes
        +String priority
        +String category
        +bool completed
        +mark_complete() void
        +get_priority_value() int
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +int available_time
        +build_plan() DailyPlan
        +filter_by_priority(threshold: String) List~Task~
        +sort_tasks(tasks: List~Task~) List~Task~
        +explain_plan(plan: DailyPlan) String
    }

    class DailyPlan {
        +List~ScheduledItem~ items
        +int total_minutes_used
        +String summary
        +add_item(item: ScheduledItem) void
        +display() String
    }

    class ScheduledItem {
        +Task task
        +String start_time
        +String end_time
        +String reason
        +display() String
    }

    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Scheduler --> Owner : uses
    Scheduler --> Pet : uses
    Scheduler --> DailyPlan : creates
    DailyPlan "1" --> "0..*" ScheduledItem : contains
    ScheduledItem --> Task : wraps
```

## Three Core User Actions

1. **Add a Pet** — The user enters owner info and pet details (name, species, age). An `Owner` object is created with a linked `Pet`.

2. **Add/Manage Care Tasks** — The user adds tasks (e.g., morning walk, feeding, meds) with a duration and priority. Tasks are stored on the `Pet`.

3. **Generate a Daily Schedule** — The user triggers the `Scheduler`, which filters and sorts `Task` objects by priority and available time, then returns a `DailyPlan` explaining what was chosen and why.
