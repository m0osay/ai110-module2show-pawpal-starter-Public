import streamlit as st

from pawpal_system import Owner, Pet, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes_per_day=45)

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps pet owners turn care tasks into a clear daily plan.

Use the form below to add tasks for a pet, then generate a schedule based on
available time and task priority.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner and Pet")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input(
    "Available minutes today", min_value=1, max_value=720, value=45
)

owner = st.session_state.owner
owner.name = owner_name
owner.available_minutes_per_day = int(available_minutes)

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=3)

if st.button("Add pet"):
    existing_pet = owner.get_pet(pet_name)
    if existing_pet is None:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(pet_age)))
        st.success(f"Added {pet_name}.")
    else:
        st.info(f"{pet_name} is already in the owner profile.")

if owner.pets:
    st.write("Registered pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets added yet. Add a pet to start building a schedule.")

st.markdown("### Tasks")
st.caption("Add a few care tasks, then build a schedule.")

if owner.pets:
    selected_pet_name = st.selectbox(
        "Choose a pet for this task",
        [pet.name for pet in owner.pets],
    )

    col1, col2 = st.columns(2)
    with col1:
        task_description = st.text_input("Task description", value="Morning walk")
        task_time = st.text_input("Preferred time", value="08:00")
    with col2:
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], index=0)

    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        pet = owner.get_pet(selected_pet_name)
        if pet is not None:
            pet.add_task(
                Task(
                    description=task_description,
                    time=task_time,
                    frequency=frequency,
                    duration_minutes=int(duration),
                    priority=priority,
                )
            )
            st.success(f"Added task to {selected_pet_name}.")

    tasks_by_pet = owner.get_tasks_by_pet()
    if any(tasks_by_pet.values()):
        st.write("Current tasks:")
        st.table(
            [
                {
                    "pet": current_pet_name,
                    "description": task.description,
                    "time": task.time,
                    "frequency": task.frequency,
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                }
                for current_pet_name, tasks in tasks_by_pet.items()
                for task in tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet before assigning tasks.")

st.divider()

st.subheader("Build Schedule")
st.caption("This uses your backend classes in `pawpal_system.py`.")

if st.button("Generate schedule"):
    if not owner.pets or not owner.get_all_tasks(include_completed=False):
        st.warning("Add at least one pet and one task before generating a schedule.")
    else:
        plan = owner.get_schedule()

        st.success("Schedule generated.")
        st.text(plan.display())
        st.markdown("### Summary")
        st.write(plan.summary)
        if plan.skipped_tasks:
            st.markdown("### Skipped tasks")
            for skipped_pet_name, skipped_task in plan.skipped_tasks:
                st.write(f"- {skipped_pet_name}: {skipped_task.description}")
