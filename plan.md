# Story Builder with MICE Quotient — Product Requirements

This document defines the product requirements for a web-based story outlining tool that helps writers structure narratives using the MICE Quotient framework (Milieu, Inquiry, Character, Event) with Try/Fail cycles.

## Product Vision

A single-page web application that enables novice writers to visually construct story outlines using the MICE Quotient framework. The tool provides an educational, card-based interface where users can create nested story elements and see their narrative structure visualized in real-time.

## Core User Experience

The application presents a three-column layout:

1. **MICE Cards (Left)**: Visual cards representing the four story elements (Milieu, Inquiry, Character, Event). Each card captures both an opening (Act 1) and closing (Act 3) for that narrative thread, plus a nesting level indicating story structure depth.

2. **Try/Fail Cycles (Center)**: Cards representing Act 2 story beats where characters attempt and fail/succeed in various ways. Four types supported:
   - Escalation (No, AND): Failure makes things worse
   - Complication (Yes, BUT): Success creates new problems
   - Revelation (No, BUT): Failure reveals opportunity
   - Resolution (Yes, AND): Success builds momentum

3. **Generated Outline (Right)**: Real-time visualization showing both a nested structure diagram and a linear story flow from Act 1 through Act 3.

### How MICE Threads Weave Through Acts
- **Act 1 (Setup)**: Introduce MICE elements, establish the world, character, question, or conflict
- **Act 2 (Confrontation)**: Try/Fail cycles where characters attempt to resolve the MICE threads
- **Act 3 (Resolution)**: Resolve all MICE threads, showing how each element concludes

### Nesting Levels
- **Level 1**: Main story thread (the primary MICE element)
- **Level 2**: Subplots that support the main thread
- **Level 3**: Character development or world-building details
- **Level 4+**: Minor elements that add depth

## Target Users and Success Metrics

### Primary User Personas
**Novice Writers**: People new to story structure who need guidance
- **Pain Points**: Don't know how to organize story ideas, struggle with pacing
- **Goals**: Create coherent, well-structured stories
- **Success**: Can create a complete story outline in 30 minutes

**Writing Students**: Learning story structure in academic settings
- **Pain Points**: Need to understand different story types, want examples
- **Goals**: Learn MICE framework, practice with different genres
- **Success**: Can identify and create all four MICE types

**Experienced Writers**: Looking for new outlining tools
- **Pain Points**: Current tools are too rigid or too flexible
- **Goals**: Quick, visual story planning
- **Success**: Can prototype story ideas rapidly

### Success Metrics
- **Usability**: User can create their first MICE card in under 2 minutes
- **Completeness**: User can create a full story outline (4 MICE + 3 Try/Fail) in under 15 minutes
- **Educational Value**: User understands MICE framework after using the app
- **Engagement**: User returns to refine their outline multiple times

### 1. MICE Card Management

**Card Types**: Four distinct types representing narrative elements:
- **Milieu (M)**: Stories about exploring a place/setting
- **Inquiry (I)**: Stories driven by seeking answers to questions
- **Character (C)**: Stories about personal transformation
- **Event (E)**: Stories about external conflicts/actions

**Card Properties**:
- MICE type indicator (M, I, C, or E)
- Opening text: What begins this narrative thread (Act 1)
- Closing text: How this thread resolves (Act 3)
- Nesting level: Integer 1-4+ indicating structural depth

**Visual Design**:
- Each MICE type has distinct color coding and icon
- Cards display abbreviated content with tooltips showing full educational details
- Cards are fixed-height (approximately 200px) and fixed-width (approximately 290px)
- Opening and closing text are both visible but truncated with ellipsis

**Card Operations**:
- Add new MICE card via form with type selector, opening/closing textareas, and nesting level input
- Edit existing card inline (replaces card with form)
- Delete card permanently
- No drag-and-drop reordering for MICE cards

### 2. Try/Fail Cycle Management

**Cycle Types**: Four patterns of story progression:
- **Escalation (No, AND)**: Failure that makes things worse
- **Complication (Yes, BUT)**: Success that creates new problems
- **Revelation (No, BUT)**: Failure that reveals opportunity
- **Resolution (Yes, AND)**: Success that builds momentum

**Card Properties**:
- Cycle type indicator
- Order number (explicit sequencing)
- Attempt: What the character tries to do
- Outcome: What actually happens (failure/success)
- Consequence: The result or what's learned

**Visual Design**:
- Each cycle type has distinct color coding and icon
- Cards show drag handle (⋮⋮) for reordering
- Cards display order number prominently
- Fixed-height (approximately 175px) and fixed-width
- All three fields (Try/Result/Learn) visible but truncated

**Card Operations**:
- Add new Try card via form with type selector and three text fields
- Edit existing card inline
- Delete card permanently
- Drag-and-drop reordering within the Try cards section only
- Order numbers update automatically after drag-and-drop

### 3. Story Outline Generation & Visualization

**Nesting Structure Diagram**:
- Visual representation showing MICE cards organized by nesting level
- Nested boxes indicating structural depth (level 1 contains level 2, etc.)
- Each box shows abbreviated card content with arrows (↓ for opening, ↑ for closing)
- Automatically updates when MICE cards are added, edited, or deleted

**Story Flow Timeline**:
- Linear three-act view showing narrative progression
- Act 1: Lists all MICE card openings in nesting order (outside-in: 1→2→3→4)
- Act 2: Lists all Try/Fail cycles in order with icon, attempt, and outcome
- Act 3: Lists all MICE card closings in reverse nesting order (inside-out: 4→3→2→1)
- Color-coded sections (green for Act 1, blue for Act 2, purple for Act 3)

**AI-Generated Outline**:
- "Generate Outline" button triggers AI processing
- Sends all cards to AI service with structured prompt
- Returns formatted prose outline displayed in dedicated area
- Outline persists until regenerated

### 4. Educational Features

**MICE Theory Panel**:
- Expandable/collapsible panel explaining the MICE Quotient framework
- Grid display of all four MICE types with:
  - Full name, description, and real-world examples (e.g., "Lord of the Rings" for Milieu)
  - Color-coded boxes matching card design
- Explanation of nesting concept: how stories open outside-in and close inside-out
- Try/Fail cycle explanation with all four types, patterns, and examples

**In-Context Help**:
- Tooltips on MICE cards showing detailed type information and examples
- Tooltips on Try cards showing pattern and example scenario
- Form fields include helper text guiding content creation

### 5. Data Management & Templates

**Sample Data**:
- "Seed Sample Data" button populates database with example story
- Sample includes multiple MICE cards at different nesting levels
- Sample includes 3 Try/Fail cycles demonstrating different types
- Demonstrates a complete story arc (e.g., child at summer camp overcoming shyness)

**Story Templates**:
- Template modal with pre-built story structures:
  - Mystery Story: I-M-C-E structure with detection-focused Try cycles
  - Adventure Story: M-E-C-I structure with quest-focused Try cycles
  - Romance Story: C-M-E-I structure with relationship-focused Try cycles
- Loading template clears existing data and populates with template cards
- Each template includes 4 MICE cards and 3 Try cycles

**Data Reset**:
- "Clear All Data" button with confirmation dialog
- Removes all cards from database
- No undo mechanism

### 6. Data Model

**MICE Cards Table** (`mice_cards`):
- `id`: Auto-incrementing primary key
- `story_id`: Foreign key (currently defaults to 1, multi-story support deferred)
- `code`: MICE type (M, I, C, or E)
- `opening`: Act 1 content (text)
- `closing`: Act 3 content (text)
- `nesting_level`: Integer indicating structural depth

**Try Cards Table** (`try_cards`):
- `id`: Auto-incrementing primary key
- `story_id`: Foreign key (currently defaults to 1)
- `type`: Try/Fail type (full string like "Escalation (No, AND)")
- `attempt`: What character tries (text)
- `failure`: What actually happens (text)
- `consequence`: Result/learning (text)
- `order_num`: Explicit sequence number

# Technical Architecture

### Database Schema
```sql
-- MICE Cards Table
CREATE TABLE mice_cards (
    id INTEGER PRIMARY KEY,
    story_id INTEGER DEFAULT 1,
    code CHAR(1) NOT NULL,  -- M, I, C, or E
    opening TEXT NOT NULL,  -- Act 1 content
    closing TEXT NOT NULL,  -- Act 3 content
    nesting_level INTEGER DEFAULT 1
);

-- Try/Fail Cards Table
CREATE TABLE try_cards (
    id INTEGER PRIMARY KEY,
    story_id INTEGER DEFAULT 1,
    type VARCHAR(20) NOT NULL,  -- Success, Failure, Trade-off, Escalation
    attempt TEXT NOT NULL,     -- What the character tries
    failure TEXT NOT NULL,     -- How it fails
    consequence TEXT NOT NULL, -- What happens next
    order_num INTEGER NOT NULL -- For drag-and-drop ordering
);
```

**Persistence Requirements**:
- All card operations (add/edit/delete/reorder) persist immediately to SQLite
- Database survives server restart
- No user accounts or authentication
- Single-user assumption (no concurrency handling needed)

## Interaction Patterns

### MICE Card Workflow
1. User clicks "Add MICE Card" button
2. Form appears above existing cards with type selector, two textareas (opening/closing), and nesting level input
3. User fills form and clicks Save
4. Form disappears, new card appears in grid
5. Nesting diagram automatically updates

### Try Card Workflow
1. User clicks "Add Try Card" button
2. Form appears with cycle type selector, order number input, and three textareas
3. User fills form and clicks Save
4. Form disappears, new card appears in grid
5. Story flow timeline automatically updates

### Drag-and-Drop Workflow
1. User grabs drag handle (⋮⋮) on Try card
2. Card becomes semi-transparent while dragging
3. Other cards shift to show drop position
4. On drop, positions update visually
5. Background request updates database order numbers
6. Story flow timeline automatically updates

### Edit Card Workflow
1. User clicks "Edit" button on card
2. Card is replaced by filled-out form
3. Other cards remain visible
4. User modifies fields and clicks Save
5. Form disappears, updated card appears
6. Relevant visualizations automatically update

### Delete Card Workflow
1. User clicks "Delete" button
2. Card immediately disappears (no confirmation for MVP)
3. Relevant visualizations automatically update

### Outline Generation Workflow
1. User arranges cards as desired
2. User clicks "Generate Outline" button
3. Loading state appears (button disabled or spinner)
4. AI service processes all cards
5. Formatted prose outline appears in dedicated section
6. Outline remains until "Generate Outline" clicked again

## Technical Constraints

- **Browser Support**: Modern evergreen browsers (Chrome, Firefox, Safari, Edge)
- **Database**: SQLite with two tables (mice_cards, try_cards)
- **No Export**: No PDF, document, or data export functionality
- **No Collaboration**: Single user editing at a time
- **No History**: No undo/redo, no version history
- **No Mobile Optimization**: Desktop-first design (responsive not required)
- **AI Dependency**: Outline generation requires external AI service access

## Technical Implementation Requirements (Assignment Enhancements)

### Drag-and-Drop Implementation
- **Frontend**: Sortable.js library for drag-and-drop functionality
- **Backend**: New endpoint `/api/try-cards/reorder` for batch order updates
- **Database**: Batch update queries for order number changes
- **Error Handling**: Rollback mechanism for failed updates
- **Performance**: Optimistic UI updates with server synchronization

### Database Schema Enhancements
- **Try Cards Table**: Enhanced `order_num` field with proper indexing
- **Batch Operations**: Support for multiple order number updates in single transaction
- **Data Integrity**: Constraints to prevent duplicate order numbers
- **Migration Support**: Alembic integration for schema changes (Option C)

### API Endpoints
- `GET /` - Main application page
- `GET /mice-form` - MICE card creation form
- `POST /mice-cards` - Create new MICE card
- `PUT /mice-cards/{id}` - Update MICE card
- `DELETE /mice-cards/{id}` - Delete MICE card
- `GET /try-form` - Try/Fail card creation form
- `POST /try-cards` - Create new Try/Fail card
- `PUT /try-cards/{id}` - Update Try/Fail card
- `DELETE /try-cards/{id}` - Delete Try/Fail card
- `POST /load-template/{template}` - Load story template
- `POST /clear-all` - Clear all data

### Frontend Enhancements
- **JavaScript**: Sortable.js integration with custom event handlers
- **CSS**: Enhanced styling for drag states and transitions
- **Accessibility**: Keyboard navigation and screen reader support
- **Mobile**: Touch-friendly drag interactions
- **Performance**: Debounced API calls and optimistic updates

### Frontend Architecture
- **HTMX Integration**: Real-time updates without page refreshes
- **Template System**: Jinja2 templates for server-side rendering
- **CSS Framework**: Custom CSS with MICE color coding
- **JavaScript**: Minimal JS for drag-and-drop functionality


### Testing Requirements
- **Unit Tests**: Database operations and API endpoints
- **Integration Tests**: End-to-end drag-and-drop workflows
- **UI Tests**: Visual feedback and user interactions
- **Performance Tests**: Large dataset handling
- **Accessibility Tests**: Keyboard navigation and screen readers

## Assignment Enhancement Requirements

Based on the assignment goals, the following enhancements are now in scope:

### Core Functionality Requirements (From ASSIGNMENT_OVERVIEW.md)
The application must support this specific workflow:
1. **Writer opens the app and sees their cards and the overview** - ✅ Already implemented
2. **Writer can add cards to any section** - ✅ Already implemented  
3. **Writer can edit existing cards to refine their outline** - ✅ Already implemented
4. **Writer can delete cards that don't fit** - ✅ Already implemented
5. **Work is saved automatically or explicitly (your choice)** - ✅ Already implemented (automatic)
6. **Writer can return later and continue working** - ✅ Already implemented (data persistence)

### Option B: Enhanced Drag-and-Drop Reordering
**Detailed Requirements for Try Cards Drag-and-Drop:**

**Visual Feedback System**:
- Drag handle (⋮⋮) becomes highlighted on hover
- Card becomes semi-transparent (opacity: 0.7) while dragging
- Drop zones show visual indicators (highlighted borders or background)
- Smooth animations for card movement and position updates
- Visual feedback for valid/invalid drop zones

**Technical Implementation**:
- Use HTML5 drag-and-drop API or JavaScript library (Sortable.js recommended)
- Implement touch support for mobile devices
- Real-time position updates during drag operation
- Automatic database updates on drop completion
- Optimistic UI updates with rollback on failure

**Database Integration**:
- Update `order_num` field in `try_cards` table immediately on drop
- Batch update all affected cards to maintain sequence integrity
- Handle concurrent updates gracefully
- Preserve data integrity during reordering operations

**User Experience Enhancements**:
- Smooth visual transitions during reordering
- Clear visual hierarchy showing new order
- Undo functionality for accidental reorders (optional)
- Keyboard navigation support for accessibility
- Touch-friendly drag handles for mobile users

**Error Handling**:
- Graceful handling of failed database updates
- Visual feedback for failed operations
- Automatic retry mechanism for network issues
- Fallback to manual order number editing if drag-and-drop fails

### Additional Enhancement Options

**Option A: Mobile-Responsive Design**
- Responsive CSS grid system for mobile devices
- Touch-friendly interface elements (larger buttons, better spacing)
- Mobile-optimized card layouts
- Swipe gestures for card operations
- Progressive Web App (PWA) capabilities

**Option C: Database Migrations (Alembic)**
- Alembic configuration for database version control
- Migration scripts for schema changes
- Rollback capabilities for failed migrations
- Automated migration testing
- Documentation for migration process

**Option D: Multi-User Support with Authentication**
- User authentication system (OAuth, JWT, or session-based)
- User-specific story storage and isolation
- User management interface
- Session management and security
- Multi-tenant database architecture

**Option E: AI-Powered Outline Generation**
- Integration with AI services (OpenAI, Anthropic, etc.)
- Structured prompt engineering for consistent outputs
- Caching system for generated outlines
- Export functionality for AI-generated content
- Customizable AI prompts per story type

**Option F: Export and Sharing Capabilities**
- PDF export with professional formatting
- Story sharing via unique URLs
- Print-friendly views with optimized layouts
- Data export options (JSON, CSV, Markdown)
- Social sharing integration

## Out of Scope (Original MVP)

- Multiple stories/projects (story_id exists but only ID=1 used) - *Now in scope for Option D*
- User accounts, authentication, authorization - *Now in scope for Option D*
- Sharing or collaboration features - *Now in scope for Option F*
- Export to PDF, Word, or other formats - *Now in scope for Option F*
- Mobile-responsive design - *Now in scope for Option A*
- Undo/redo functionality - *Enhanced in Option B*
- Auto-save indicators or status - *Enhanced in Option B*
- Offline mode
- Print-friendly views - *Now in scope for Option F*
- Keyboard shortcuts - *Enhanced in Option B*
- Accessibility features beyond basic HTML semantics - *Enhanced in Option B*
- Admin interface or analytics