# SpecStory Configuration for Elite AI Assisted Coding Assignment

## Overview
This directory contains SpecStory configuration and captured session data for the MICE Quotient Story Builder project.

## SpecStory Session Management (On-Demand)

### New Workflow
- **Manual Start/Stop**: Sessions are started and stopped manually
- **30-Minute Timeout**: Sessions auto-stop after 30 minutes of inactivity
- **AI Agent Prompting**: AI agents will always ask if you want to start a session
- **User Control**: You decide when to capture development work

### How to Use

#### Starting a Session
```bash
# Option 1: Use the session manager script
./.specstory/session-manager.sh start

# Option 2: Use SpecStory directly
specstory start
```

#### Stopping a Session
```bash
# Option 1: Use the session manager script
./.specstory/session-manager.sh stop

# Option 2: Use SpecStory directly
specstory stop
```

#### Checking Status
```bash
# Option 1: Use the session manager script
./.specstory/session-manager.sh status

# Option 2: Use SpecStory directly
specstory status
```

### AI Agent Integration
Your AI agents (Cursor, VS Code) will now:
1. **Always ask**: "Would you like to start a SpecStory session to capture this development work?"
2. **Respect your choice**: Start session only if you confirm
3. **Remind about timeout**: Alert you when approaching 30-minute limit
4. **Offer extensions**: Ask if you want to extend the session

### What SpecStory Captures
- **Chat History**: All conversations with AI assistants
- **Code Changes**: File modifications and code generation
- **File Operations**: File creation, deletion, and movement
- **Development Sessions**: Complete development workflow documentation

### Session Behavior
- **No Auto-Capture**: Sessions only start when you explicitly start them
- **Timeout Protection**: Sessions auto-stop after 30 minutes of inactivity
- **User Control**: You decide when to capture development work
- **Prompt Integration**: AI agents always ask before starting sessions

### Viewing Captured Data
- Sessions are saved in markdown format for easy reading
- Each session includes timestamps and context
- Code changes are tracked with before/after comparisons
- Check `.specstory/history/` directory for captured sessions

## Project Context
This project implements:
- MICE Quotient Story Builder application
- Drag-and-drop functionality for Try cards
- FastAPI backend with SQLite database
- HTMX frontend with real-time updates

## Configuration
The `config.json` file contains:
- Manual session control settings
- 30-minute timeout configuration
- Output format preferences
- Session naming conventions
- Project metadata

## Troubleshooting
If SpecStory isn't working:
1. Ensure SpecStory is installed: `brew install specstoryai/tap/specstory`
2. Check session status: `specstory status`
3. Verify configuration: Check `config.json` settings
4. Use session manager: `./.specstory/session-manager.sh help`
