# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

-> The Basics (Task & Pet): These are the building blocks, storing everything from a pet's age to whether a walk was "high priority" or "low priority."

-> The Hub (Owner): This represents the user, keeping track of their pets and how much free time they have in a day.

-> The Brain (Scheduler): This is where the logic lives. it sifts through all the tasks and picks the most important ones that fit into the owner's schedule.

-> The Output (DailyPlan & ScheduledItem): These take the messy backend logic and turn it into a clean, easy-to-read schedule for the day.


**b. Design changes**       

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

-> The initial DailyPlan lacked metadata. By passing the owner and pet context into the object, I made the generated summaries much more descriptive and useful for a multi-pet household.

-> I moved away from "silently dropping" tasks that exceeded the time limit. By capturing those skipped items in a new field, I made the explain_plan() method significantly more robust and honest.

->To make the schedule more efficient, I refined the sort key. Instead of just sorting by priority, it now handles equal priorities by duration, favoring "quick wins" to maximize the number of tasks completed.

->I identified a potential bug where the scheduler was caching available_time. I fixed this by ensuring the logic fetches the owner's time directly from the source during the build process, preventing synchronization issues.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

-> My scheduler mainly considers available minutes per day, task priority, preferred task time, completion status, and whether a task belongs to a specific pet. I also added recurrence rules for daily and weekly tasks so the system keeps generating the next due item after completion.

-> I treated available time and priority as the most important constraints because they directly affect whether a busy pet owner can realistically complete the plan. After that, I used preferred time and pet filtering to make the output feel more organized and useful.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

-> One tradeoff is that my conflict detection only checks for exact matching start times, like two tasks both requesting `08:30`, instead of calculating whether task durations overlap. This is reasonable for the current version because it keeps the logic lightweight, easy to debug, and clear for a classroom-sized project, while still catching the most obvious scheduling conflicts a pet owner would want warned about.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

-> VS Code Copilot was most effective when I used it for focused tasks like generating starter tests, suggesting sorting logic with `sorted()` and lambda keys, and helping me think through recurring-task behavior and conflict detection. Inline suggestions were especially helpful for docstrings and small method cleanups, while chat worked better for planning algorithms and asking what edge cases I should test.

-> The most helpful prompts were specific and scoped, such as asking for a lightweight conflict detection strategy, a test plan for sorting and recurring tasks, or a cleaner way to format schedule output in the terminal. I got the best results when I asked for one small improvement at a time instead of asking AI to redesign the whole app at once.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

-> One example was when I considered making the conflict detection more "Pythonic" with a shorter grouping approach. I decided not to fully adopt that style because the more compact version was harder to read and explain than my straightforward dictionary-based loop.

-> I evaluated AI suggestions by checking whether they matched my class design, whether they kept responsibilities in the right places, and whether I could verify them with terminal runs or `pytest`. If a suggestion made the code shorter but less clear, I chose readability because I still needed to understand and defend the design.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

-> I tested task completion, adding tasks to a pet, chronological sorting, recurring daily and weekly task creation, and conflict detection for duplicate times. These behaviors were important because they cover the core promise of the app: storing pet-care tasks, organizing them intelligently, and helping the owner notice problems before following the schedule.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

-> I am fairly confident in the scheduler because the main happy paths and several edge cases are covered by passing tests, and I also verified the behavior through the terminal demo and Streamlit UI. I would rate my confidence as about 4 out of 5.

-> If I had more time, I would test pets with no tasks, owners with no pets, invalid time formats, overlapping durations instead of just exact matching times, and more recurrence edge cases such as completing a task multiple times in a row.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

-> I am most satisfied with how the project grew from a simple class design into a smarter system with sorting, filtering, recurring tasks, conflict warnings, tests, and a Streamlit interface that actually exposes those features to the user.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

-> In another iteration, I would redesign the scheduling logic to respect preferred times more closely instead of mostly building a back-to-back plan. I would also add stronger validation around time input and support richer conflict detection using overlapping durations.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

-> My biggest takeaway is that AI works best when I stay the lead architect. Copilot was powerful for suggestions, drafts, and brainstorming, but the project only stayed clean when I kept deciding the class boundaries, checked the outputs, and used separate chat sessions for different phases so design, testing, and UI work did not all blur together.
