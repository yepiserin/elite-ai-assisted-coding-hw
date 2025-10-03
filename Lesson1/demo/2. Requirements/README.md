# Requirements

This verion used good requirements to code with AI, and then dive into the code to understand and refactor it.

Typically you should be refactoring and editing code as you go so your understand it.  But this is to:

1. Get you to see what you can do with good prompting
2. Let you see a clean diff of what I did after AI was done

## What happened

### Context Gathering

1. I used voicepal to transcribe my thoughts for the app.  
2. I then gave that to copilot (GPT-5) and asked it to ask me questions that it would need to know to create a requirements plan based on that.  
3. I then transcribed more.  
4. I asked claude 4.5 to put that into a plan. 
5. I read it and saw it misunderstood the structure
6. I found a blog post about it that I liked, and used the Jina AI reader to conver to markdown
7. I used that as context to improve the plan
8. I heavily edited the plan to what I felt was really great.

### The Coding

I used AI to code.  When it got stuck, I hunter down docs to copy paste doc pages it needed directly into the chat, etc.  I copy console errors, and server errors into the chat.  I told it when things weren't working right.  I gave it critiquest on how it looked when things weren't readable.

## The Assignment

Create a requirement document that describes in detail what you want to build and then use AI to build it. 

This assignment can be scaled in difficulty based on your abilities and experience.  I recommend starting with #1, and progressing as far as you'd like to:

Here's some ideas:

**Level 1**
 Use the context I created, read it, and modify something about the app I created.  Here's some ideas:
    - UI: Make it mobile friendly
    - UI: Allow for re-ordering of the cards within sections.  Arrows or drag and drop
    - UI: Improve the aesthetics of the AI Generated outline.
    - Database: Use an ORM to improve the database management, and set up migrations
    - Feature: Add a create outline with AI feature

**Level 2**

Read the context carefully to understand it, then re-create the context and make this specic app.  I recommend taking notes of the kinds of things you want to include in yours (such as tech stack) while reading my context!  Then, make a new directory and do it without looking at the specific context, just referencing your notes.  You can also rebuild it in the framework of your choosing.

**Level 3**

Do this process for your own app or project!
