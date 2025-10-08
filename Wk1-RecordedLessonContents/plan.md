# Time Zone Converter - Product Requirements Document (PRD)

## Overview
A simple web application that helps users identify good meeting times across multiple global time zones with visual color-coding to quickly assess meeting time viability.

## Technical Stack
- **Framework**: Air (FastAPI-based web framework)
- **Interactivity**: HTMX for dynamic updates
- **Session**: Local session storage (no database, no authentication)
- **UI**: Pico CSS

## Core Features

### 1. Time Zone Selection
- **Source Time Zone**: Dropdown selector for the user's current time zone
- **Default**: Washington, D.C. (America/New_York - EST)
- **Target Time Zones**: Display conversions for 10-12 major global cities (read-only)

### 2. Time Input
- **Format**: 12-hour format with AM/PM
- **Input Type**: Dropdown time picker in 30-minute increments
- **Behavior**: Auto-update conversions on change (HTMX `hx-trigger="change"`)

### 3. Time Zone Coverage
Select 10-12 cities representing major global regions:
- **North America**: San Francisco (PST), Chicago (CST), Washington D.C. (EST)
- **Europe**: London (GMT), Paris (CET), Berlin (CET)
- **Asia**: Manila (PHT), Tokyo (JST), Singapore (SGT)
- **Pacific**: Sydney (AEST)

### 4. Time Display Requirements

#### Format
- **Display**: City name with 12-hour time (e.g., "San Francisco: 4:00 PM")
- **Date Indicator**: Show "Today", "Tomorrow", or "Yesterday" next to times in different calendar days
- **Example**: "Manila: 7:00 AM Tomorrow"

#### Color Coding (Visual Feedback)
Apply background colors to each time zone result based on local business hours:

| Time Range (Local) | Color | Meaning | Hex Color Suggestion |
|-------------------|-------|---------|---------------------|
| 9:00 AM - 4:00 PM | Light Green | Good/Convenient | `#d4edda` or similar |
| 6:00 AM - 9:00 AM<br>4:00 PM - 10:00 PM | Yellow | Inconvenient | `#fff3cd` or similar |
| 10:00 PM - 6:00 AM | Red | Unacceptable | `#f8d7da` or similar |

*Colors should be subtle/light to maintain readability*

### 5. Time Zone Conversion Logic
- **DST**: Ignore daylight saving time for MVP - always use standard time offsets
- **Date Handling**: Calculate day offset when times cross midnight boundaries
- **Validation**: No date selector needed; assume "today" as the base date

## Non-Requirements (Out of Scope for MVP)
- ❌ Multi-user support
- ❌ User authentication
- ❌ Persistent storage/database
- ❌ Daylight Saving Time handling
- ❌ Mobile responsiveness
- ❌ Custom time zone selection (fixed list only)
- ❌ Time zone search/filtering

## User Flow
1. User lands on page with Washington D.C. pre-selected as source time zone
2. User selects a time from dropdown (defaults to current time or first option)
3. Page automatically displays converted times for all target time zones with color coding
4. User changes source time zone → conversions update automatically
5. User changes time → conversions update automatically

## UI/UX Guidelines
- **Layout**: Simple single-page layout, desktop-optimized
- **Clarity**: Each time zone clearly labeled with city name
- **Scanning**: Color-coded results allow quick visual scanning for good meeting times
- **Responsiveness**: HTMX provides seamless updates without page refresh

## Success Criteria
- User can select a time and immediately see what time it is in many global cities
- Color coding makes it obvious at a glance which times are suitable for meetings