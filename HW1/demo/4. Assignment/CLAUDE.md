

<!-- Source: AGENTS.md -->

# Style

I want you to keep in mind the following stylistic choices that I make:
1. Use type hinting where possible to ensure the code is clear and it's understandable what should be passed to things.
2. Things should be refactored to have decent separation of concerns, but not to such an extreme. Any kind of abstraction should be weighed for how thin vs thick it is, how many times it's duplicated, and what's the cost of adding the redirection. An abstraction that only calls another function is not helpful and actually adds complexity. Put code in its appropriate place. For example, Python code goes in Python files, CSS code goes in CSS files, and JavaScript blocks go in JavaScript files. Don't embed massive CSS blocks in a Python string or in a Jinja template just like you wouldn't have massive amounts of JavaScript. Those can be imported.
3.  The next thing I want to keep in mind is that I do not want any error handling. I am first trying to build a feature and make sure it works, and error handling disguises errors, so it's important to me to see the full stack trace and let the app fail. I can decide very surgically in what cases do I want an error not to crash the app. Most of the times I do want it to crash so that I can fix it so that never happens again.
4.  Three, do not mock things as an example for like what it might be like. In production it should be created as if it were the real thing. So if you are not able to do something instead of creating an imitation of that thing stop and ask tell me what you need to do this properly.

# Neccesary Context

In order to complete this, you'll need several pieces of information:

- There's an overall plan in the plan.md file
- There's a specific step by step plan in the todos.md file that dictates how we will build this app together
- If there's any doubt, stop me so that we can proceed forward together
- You should always verify things are being done correctly by checking the documentation of air, which you have tools to inspect.  The best developers reference the documentation a lot.
- After doing something, you should verify that it works. You have access to playwright, and the app is running on port 8000.  Anytime one of the app python files are edited the app auto-reloads so you don't have to worry about refreshing or restarting.
- The air docs are great, you should always look for things in the docs directory to learn about air vs the source code when possible.



<!-- Source: .ruler/AGENTS.md -->

# Elite AI Assisted Coding - Homework Guidelines

This repository contains homework assignments for the Elite AI Assisted Coding Course. All AI agents should follow these guidelines when working on any assignment.

## Project Context

- **Course**: Elite AI Assisted Coding
- **Framework**: FastAPI with Air (Daniel and Audrey Roy Greenfeld)
- **Database**: SQLite with proper schema design
- **Frontend**: HTMX with real-time updates
- **Port**: Applications run on port 8000 (unless specified otherwise)

## Code Quality Standards

### Type Safety & Clarity
- **Type Hinting**: Always use type hints to make code clear and self-documenting
- **Function Parameters**: Every function parameter and return value should have explicit type annotations
- **Variable Types**: Use explicit typing for complex data structures

### Abstraction & Code Organization
- **Abstraction**: Only create abstractions when they provide meaningful value
- **File Structure**: Maintain proper separation of concerns by file type
  - Python code belongs in `.py` files
  - CSS in `.css` files  
  - JavaScript in `.js` files
  - Never embed large blocks of CSS or JavaScript as strings in Python or templates
- **Function Size**: Functions can be longer if they represent a single, cohesive task
- **Duplication**: Some duplication is acceptable - refactor on the third occurrence, not the second

### Error Handling
- **No Defensive Error Handling**: Do not add try/except blocks during initial development
- **Let it Fail**: Let the application fail with full stack traces so bugs can be identified and fixed at their source
- **Error Handling**: Only add error handling surgically in specific cases where graceful degradation is truly needed

### Implementation Standards
- **No Mocks or Placeholders**: Never create mock implementations or placeholder code
- **Real Functionality**: Build real functionality, not examples
- **Dependencies**: Prefer adding well-maintained third-party libraries over writing complex functionality from scratch
- **Design Patterns**: Use the simplest solution that works
- **Paradigm**: Favor functional programming patterns where appropriate (pure functions, immutability for data transformations)

## Assignment-Specific Guidelines

### MICE Quotient Story Builder
- **Database Schema**: Use proper SQLite schema with mice_cards and try_cards tables
- **Drag-and-Drop**: Implement real drag-and-drop functionality using Sortable.js
- **Real-time Updates**: Use HTMX for real-time UI updates
- **Visual Feedback**: Provide clear visual feedback for user interactions

### Verification Requirements
- **Browser Testing**: Always verify work using browser automation (Playwright)
- **App Testing**: Applications run on port 8000 and auto-reload on file changes
- **Documentation**: Reference Air documentation when implementing features

## Development Workflow

1. **Read Requirements**: Always start by reading the assignment requirements in `plan.md` and `todos.md`
2. **Understand Context**: Review the MICE Quotient methodology in `mice.md`
3. **Implement Features**: Build real functionality following the guidelines above
4. **Test Thoroughly**: Use browser automation to verify functionality
5. **Document Changes**: Update relevant documentation files

## File Organization

- **Assignment Structure**: Each assignment follows the pattern `HW1/demo/X. Assignment/`
- **Documentation**: Key files include `plan.md`, `todos.md`, `mice.md`, `AGENTS.md`
- **Application Code**: Lives in the `app/` directory within each assignment
- **Testing**: Use Playwright for browser automation testing

Remember: This is real product development, not toy examples. Build production-quality code that solves real problems.
