# Specstory Session Management Configuration

## Auto-Start Specstory on Session Begin

Every time you start a new session in Cursor or VS Code, you MUST:

1. **Prompt the user**: "Would you like to start specstory recording for this session?"
2. **If yes, ask for root folder**: "Which root folder should specstory be applied to for this session?"
3. **Start specstory**: Run the appropriate specstory command with the selected root folder
4. **Configure timeout**: Set specstory to automatically stop after 30 minutes of inactivity

## Specstory Configuration

### Auto-prompt Template
```
🚀 Session Setup Required

Would you like to start specstory recording for this development session?

If yes, please specify which root folder specstory should be applied to:
- Current workspace root: [current path]
- Specific assignment folder: [path to specific assignment]
- Custom path: [user can specify]

Specstory will automatically stop recording after 30 minutes of inactivity.
```

### Commands to Use
- **Start specstory**: `specstory start [root-folder] --timeout 30m`
- **Check status**: `specstory status`
- **Stop manually**: `specstory stop`

### Timeout Configuration
- **Inactivity timeout**: 30 minutes
- **Auto-stop**: Configure specstory to automatically stop recording after 30 minutes of no activity
- **Session persistence**: Maintain recording across file changes and development work

## Integration Points

This configuration should be applied to:
- `.cursor/rules/` files
- `.vscode/settings.json` 
- Agent-specific configuration files
- IDE startup scripts
- Workspace configuration files

## Session Management

### When to Prompt
- New Cursor/VS Code session start
- New workspace opened
- New terminal session in development environment
- After specstory has been stopped

### What to Ask
1. Start specstory recording? (Yes/No)
2. Which root folder? (Current/Custom)
3. Any specific configuration? (Default: 30min timeout)

### What to Do
1. Start specstory with selected root folder
2. Confirm recording has started
3. Set up inactivity monitoring
4. Provide status updates if requested
