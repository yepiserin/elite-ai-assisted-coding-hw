# No Context

This version uses `prompt.md` to try to create an app.

## What happened

I built an app that prompts users. The main page worked, but when I tried to manually create a story to fill in the field, I encountered an error. The page was just a single form, not what I wanted. Instead of letting me create a story, it only allowed me to fill out a form. I decided to continue anyway, hoping the process might work, but it failed with an error.

I tried to give the AI some context about the bug and checked the server logs. When that didn’t help, I looked at the app’s code to see if I could fix it. I realized the form wasn’t what I needed. The app stored everything in memory, with nothing reusable or connected to a database. To make it work, I would have to change all the storage to use SQLite or Postgres.

At this point, I saw that starting over would be faster than trying to fix or reuse the existing code. There wasn’t anything worth salvaging, so I decided not to finish it.