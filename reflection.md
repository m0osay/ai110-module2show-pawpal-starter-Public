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

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
