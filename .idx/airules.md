

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
