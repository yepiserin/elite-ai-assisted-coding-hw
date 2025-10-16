# Cursor IDE - Specstory Session Management

## Session Startup Protocol

**MANDATORY**: At the start of every new Cursor session, you MUST:

### 1. Auto-Prompt for Specstory
```
🚀 Development Session Setup

Would you like to start specstory recording for this session?

This will help track your development progress and create documentation.
```

### 2. Root Folder Selection
If user chooses to start specstory, ask:
```
📁 Which root folder should specstory be applied to?

Options:
- Current workspace: [current path]
- Specific assignment: [path to assignment]
- Custom path: [user specifies]

Default: Current workspace root
```

### 3. Start Specstory
Execute the appropriate command:
```bash
specstory start [selected-root-folder] --timeout 30m
```

### 4. Confirm Setup
```
✅ Specstory started successfully
📁 Recording in: [selected folder]
⏰ Auto-stop after: 30 minutes of inactivity
```

## Configuration Details

### Specstory Command Template
```bash
# Start with 30-minute inactivity timeout
specstory start [ROOT_FOLDER] --timeout 30m

# Check status
specstory status

# Stop manually if needed
specstory stop
```

### Timeout Behavior
- **Inactivity detection**: 30 minutes of no user activity
- **Auto-stop**: Specstory automatically stops recording
- **Session persistence**: Recording continues across file changes
- **Manual override**: User can stop manually anytime

## Integration Points

This configuration applies to:
- All Cursor AI agents
- Workspace startup scripts
- Terminal session initialization
- Development workflow automation

## User Experience

### First Time Setup
1. Prompt appears automatically on session start
2. User selects root folder
3. Specstory starts with confirmation
4. Development proceeds with recording

### Subsequent Sessions
1. Check if specstory is already running
2. If not running, prompt to start
3. If running, confirm current status
4. Option to restart with different folder

### Session Management
- **Status checks**: Provide status updates when requested
- **Manual control**: Allow user to stop/restart specstory
- **Folder changes**: Support changing root folder mid-session
- **Timeout handling**: Graceful auto-stop with notification

## Error Handling

### If Specstory Not Available
```
⚠️ Specstory not found

Would you like to:
1. Install specstory first
2. Skip recording for this session
3. Use alternative documentation method
```

### If Permission Issues
```
⚠️ Permission denied for selected folder

Please choose a different folder or check permissions.
```

### If Already Running
```
ℹ️ Specstory already running

Current session: [folder path]
Would you like to:
1. Continue with current session
2. Stop and restart with new folder
3. Check current status
```
