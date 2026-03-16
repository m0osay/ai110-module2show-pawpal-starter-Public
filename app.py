import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

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
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=3)

st.markdown("### Tasks")
st.caption("Add a few care tasks, then build a schedule.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2 = st.columns(2)
with col1:
    task_description = st.text_input("Task description", value="Morning walk")
    task_time = st.text_input("Preferred time", value="08:00")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], index=0)

priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    st.session_state.tasks.append(
        {
            "description": task_description,
            "time": task_time,
            "frequency": frequency,
            "duration_minutes": int(duration),
            "priority": priority,
        }
    )

if st.button("Clear tasks"):
    st.session_state.tasks = []

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This uses your backend classes in `pawpal_system.py`.")

if st.button("Generate schedule"):
    if not st.session_state.tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        owner = Owner(name=owner_name, available_minutes_per_day=int(available_minutes))
        pet = Pet(name=pet_name, species=species, age=int(pet_age))

        for item in st.session_state.tasks:
            pet.add_task(
                Task(
                    description=item["description"],
                    time=item["time"],
                    frequency=item["frequency"],
                    duration_minutes=item["duration_minutes"],
                    priority=item["priority"],
                )
            )

        owner.add_pet(pet)
        plan = Scheduler(owner).build_plan()

        st.success("Schedule generated.")
        st.text(plan.display())
        st.markdown("### Summary")
        st.write(plan.summary)
        if plan.skipped_tasks:
            st.markdown("### Skipped tasks")
            for skipped_pet_name, skipped_task in plan.skipped_tasks:
                st.write(f"- {skipped_pet_name}: {skipped_task.description}")
