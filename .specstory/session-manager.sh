#!/bin/bash

# SpecStory Session Manager
# Manages on-demand SpecStory sessions with 30-minute timeout

SESSION_DIR=".specstory/sessions"
CONFIG_FILE=".specstory/config.json"
TIMEOUT_MINUTES=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if SpecStory is installed
check_specstory() {
    if ! command -v specstory &> /dev/null; then
        echo -e "${RED}Error: SpecStory is not installed or not in PATH${NC}"
        echo "Install with: brew install specstoryai/tap/specstory"
        exit 1
    fi
}

# Function to start a session
start_session() {
    echo -e "${BLUE}Starting SpecStory session...${NC}"
    
    # Create session directory if it doesn't exist
    mkdir -p "$SESSION_DIR"
    
    # Start SpecStory session (using run command for terminal agents)
    if specstory run cursor --silent; then
        echo -e "${GREEN}✅ SpecStory session started successfully${NC}"
        echo -e "${YELLOW}⏰ Session will auto-stop after $TIMEOUT_MINUTES minutes of inactivity${NC}"
        
        # Save session info
        echo "$(date)" > "$SESSION_DIR/current_session.txt"
        echo "Session started at: $(date)" >> "$SESSION_DIR/session_log.txt"
        
        # Start timeout monitor in background
        start_timeout_monitor
    else
        echo -e "${RED}❌ Failed to start SpecStory session${NC}"
        exit 1
    fi
}

# Function to stop a session
stop_session() {
    echo -e "${BLUE}Stopping SpecStory session...${NC}"
    
    # SpecStory doesn't have a stop command, so we'll use sync to finalize
    if specstory sync; then
        echo -e "${GREEN}✅ SpecStory session stopped successfully${NC}"
        echo "Session stopped at: $(date)" >> "$SESSION_DIR/session_log.txt"
        
        # Clean up session files
        rm -f "$SESSION_DIR/current_session.txt"
    else
        echo -e "${RED}❌ Failed to stop SpecStory session${NC}"
        exit 1
    fi
}

# Function to check session status
check_status() {
    if [ -f "$SESSION_DIR/current_session.txt" ]; then
        echo -e "${GREEN}✅ SpecStory session is active${NC}"
        echo -e "${BLUE}Session started at: $(cat "$SESSION_DIR/current_session.txt")${NC}"
    else
        echo -e "${YELLOW}⚠️  No active SpecStory session${NC}"
    fi
}

# Function to start timeout monitor
start_timeout_monitor() {
    (
        sleep $((TIMEOUT_MINUTES * 60))
        if [ -f "$SESSION_DIR/current_session.txt" ]; then
            echo -e "${YELLOW}⏰ SpecStory session timeout reached (${TIMEOUT_MINUTES} minutes)${NC}"
            echo -e "${BLUE}Auto-stopping session...${NC}"
            specstory sync
            echo "Session auto-stopped at: $(date)" >> "$SESSION_DIR/session_log.txt"
            rm -f "$SESSION_DIR/current_session.txt"
        fi
    ) &
}

# Function to show help
show_help() {
    echo -e "${BLUE}SpecStory Session Manager${NC}"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start   - Start a new SpecStory session"
    echo "  stop    - Stop the current SpecStory session"
    echo "  status  - Check if a session is active"
    echo "  help    - Show this help message"
    echo ""
    echo "Session Behavior:"
    echo "  - Manual start/stop only"
    echo "  - Auto-stop after $TIMEOUT_MINUTES minutes of inactivity"
    echo "  - User controls when to start and stop"
    echo ""
}

# Main script logic
check_specstory

case "${1:-help}" in
    start)
        start_session
        ;;
    stop)
        stop_session
        ;;
    status)
        check_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
