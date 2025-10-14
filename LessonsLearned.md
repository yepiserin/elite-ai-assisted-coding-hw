# Lessons Learned - Elite AI Assisted Coding

## SpecStory Session Management - October 13, 2025

### **The Issue**
During a significant development session on October 13, 2025, we completed major work but failed to capture it with SpecStory:

- ✅ **Completed Work**: Full drag-and-drop implementation for MICE and Try cards
- ✅ **Database Changes**: Added `order_num` field and reorder functionality  
- ✅ **API Development**: Created batch update endpoints
- ✅ **Problem Solving**: Fixed FastAPI route ordering issues
- ✅ **Git Operations**: Repository setup, merging, and upstream integration
- ✅ **Testing**: Verified functionality with curl commands

### **What Went Wrong**
1. **Missed the Prompt**: AI assistant didn't follow the `AGENTS.md` instruction to prompt for SpecStory session
2. **Infrastructure Only**: Set up SpecStory folders and config but never started actual session
3. **No Session Capture**: All development work went undocumented in SpecStory
4. **Manual Log Only**: Only had a basic development log, not comprehensive session data

### **Root Cause**
The AI assistant got caught up in technical implementation and forgot to follow the established workflow:

> **From AGENTS.md**: "Before starting any development work, you MUST ask the user if they want to start a SpecStory session"

### **Impact**
- **Lost Documentation**: No captured session of the development process
- **Missed Learning**: Can't review the problem-solving approach used
- **No Artifacts**: Missing the detailed interaction history that SpecStory provides
- **Process Gap**: Inconsistent with established workflow

### **Lessons Learned**

#### **For AI Assistants**
1. **Always Prompt First**: Before any development work, ask about SpecStory session
2. **Follow Established Workflows**: Don't skip process steps even when focused on technical work
3. **Session Management**: Ensure SpecStory is actually started, not just configured
4. **Regular Checks**: Verify session is active during long development sessions

#### **For Development Workflow**
1. **Process Discipline**: Stick to established workflows even when excited about technical work
2. **Session Verification**: Confirm SpecStory is running before starting development
3. **Documentation Value**: SpecStory captures valuable problem-solving approaches
4. **Retrospective Value**: Session data helps improve future development

### **Prevention Strategies**
1. **Explicit Prompts**: AI must always ask about SpecStory at session start
2. **Workflow Reminders**: Include SpecStory status in regular check-ins
3. **Session Verification**: Confirm SpecStory is active before major work
4. **Process Documentation**: Keep workflows visible and accessible

### **Key Takeaway**
**Process discipline is as important as technical implementation.** Even when focused on exciting technical work, following established workflows ensures we capture valuable development insights and maintain consistent documentation practices.

---

## FastAPI Server Restart Issues - October 13, 2025

### **The Problem**
During development of the MICE Quotient Story Builder, we encountered a critical issue where MICE cards were not displaying despite:
- ✅ Database containing 4 MICE cards with correct data
- ✅ Database functions working correctly (verified with direct testing)
- ✅ Render functions working correctly (verified with direct testing)
- ✅ Air framework working correctly
- ✅ All components working individually

### **Root Cause**
The issue was **server process management**, not code problems:
1. **Multiple Server Processes**: Multiple FastAPI processes were running on port 8000
2. **Port Conflicts**: New server couldn't start due to "Address already in use" errors
3. **Stale Processes**: Old server processes weren't properly terminated
4. **Database Connection**: Server was using cached/incorrect database connections

### **The Solution**
**Complete server process cleanup and restart:**

```bash
# 1. Kill all processes using port 8000
lsof -ti:8000 | xargs kill -9

# 2. Kill any remaining FastAPI processes
pkill -f "fastapi dev"

# 3. Restart server cleanly
cd "/path/to/app" && uv run fastapi dev main.py --port 8000
```

### **Key Debugging Steps**
1. **Database Verification**: Used direct Python script to verify database functions
2. **Component Testing**: Tested render functions independently
3. **Server Logs**: Added debug output to track card retrieval
4. **Process Management**: Identified multiple server processes as the issue

### **Lessons Learned**

#### **For Development**
1. **Process Management**: Always check for existing processes before starting new ones
2. **Clean Restarts**: Use proper process termination, not just Ctrl+C
3. **Port Conflicts**: Check for port usage with `lsof -ti:PORT`
4. **Debug Strategy**: Test components independently when issues arise

#### **For FastAPI Development**
1. **Process Cleanup**: Use `lsof` and `pkill` for thorough cleanup
2. **Port Management**: Verify port is free before starting server
3. **Database Connections**: Ensure server uses correct database file
4. **Auto-reload Issues**: Sometimes manual restart is needed for database changes

### **Prevention Strategies**
1. **Process Check**: Always verify no existing processes before starting server
2. **Clean Shutdown**: Use proper termination methods
3. **Port Verification**: Check port availability before starting
4. **Database Path**: Ensure server runs from correct directory with correct database

### **Key Takeaway**
**Server process management is critical for FastAPI development.** Multiple processes can cause silent failures where code works but server doesn't reflect changes. Always ensure clean process management for reliable development.

---
*Date: October 13, 2025*  
*Context: HW1 - 4. Assignment Development*  
*Impact: High - Lost significant development session documentation*
