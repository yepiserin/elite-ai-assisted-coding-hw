# Mice Craft — MVP Plan

This document captures the requirements and implementation plan for the Mice Craft MVP (three-act outline editor). It's intentionally minimal and focused on the user's directions: help novice writers create a three-act outline with a simple card-based left pane and a markdown outline on the right.

## Goal (MVP)
- Provide a simple, persistent, desktop-first web app that helps novice writers build a three-act outline using cards.
- Left: vertical card area grouped by Act 1 & 3, and then Act 2. Cards are created, edited, deleted, and reordered (drag-and-drop) within their section
- Right: a Markdown-rendered bulleted outline generated on-demand via a Refresh button.
- Persistence: server-side using SQLite. No user accounts, no admin, no export, no real-time collaboration.

## Key assumptions (confirmed)
- Backend: AIR (FastAPI-based) with Jinja templates.
- Styling: Tailwind + DaisyUI via CDN.
- Multiple stories supported (user can create/open multiple named stories).
- Cards cannot move across acts. Reordering is only within the same act.
- Deleting a card is permanent (removed from DB).
- Autosave is acceptable; I'll recommend autosave on create/edit/reorder for simplicity.

## Minimal data model
Use SQLite with two tables: `stories` and `cards`.

stories
- id INTEGER PRIMARY KEY
- title TEXT NOT NULL
- description TEXT NULL
- created_at TIMESTAMP
- updated_at TIMESTAMP

cards
- id INTEGER PRIMARY KEY
- story_id INTEGER NOT NULL -- foreign key to stories(id)
- kind TEXT NOT NULL CHECK(kind IN ('mice','act2')) -- 'mice' == Act1&3 card, 'act2' == Try card
- position INTEGER NOT NULL -- ordering within section (1-based)
- title TEXT NOT NULL
- open_body TEXT NULL -- for MICE cards: Act 1 (opening) content, supports Markdown
- close_body TEXT NULL -- for MICE cards: Act 3 (closing) content, supports Markdown
- body TEXT NULL -- for Act2 (Try) cards: Act 2 content, supports Markdown
- created_at TIMESTAMP
- updated_at TIMESTAMP

Indexes: index on (story_id, kind, position) for efficient ordering queries.

Notes:
- No extra metadata or tags in MVP.
- `open_body`, `close_body`, and `body` support Markdown to enable richer card notes and for extracting content for the outline.

## Outline rules (Mice Quotient ordering)
- The outline is generated from the stored cards for a selected story. The outline displays three sections (Act 1, Act 2, Act 3) even though the editor shows two sections.
- Ordering rules and mapping from stored cards to outline:
   - Act 1: produced from all `mice` cards' `open_body` fields, listed in ascending `position` order (these are the openings/intros for each narrative thread).
   - Act 2: produced from all `act2` cards' `body` fields, listed in ascending `position` order (the try/attempt blocks).
   - Act 3: produced from all `mice` cards' `close_body` fields, listed in ascending `position` order. Conceptually Act 3 resolves the Act 1 threads (often in reverse open order), but for MVP the outline will list `close_body` items in stored order. (If you later want Act 3 to auto-order as reverse of Act 1, we can implement that.)
- The Refresh button on the UI will request the server to re-render an outline (server-side) into Markdown, which will then be converted to HTML and displayed on the right.

## API surface (minimal)
- GET /stories — list stories
-- POST /stories — create story (payload: { title, description? })
-- GET /stories/{id} — get story and its cards
-- POST /stories/{id}/cards — create card. Payload depends on card kind:
   - For MICE (Act 1 & 3) cards: { card_kind: 'mice', title, open_body, close_body }
   - For Act2 (Try) cards: { card_kind: 'act2', title, body }
-- PUT /cards/{id} — update card. Payload depends on card kind (mice vs act2) and may include `title`, `open_body`, `close_body`, or `body`.
-- DELETE /cards/{id} — delete card (permanent)
-- POST /stories/{id}/cards/reorder — reorder endpoint (payload: { section: 'mice'|'act2', ordered_card_ids: [id,...] }) — updates `position` values for the section
-- GET /stories/{id}/outline — returns the generated Markdown outline for the story

Notes:
- For simplicity we'll use standard JSON request/response payloads for API endpoints used by client-side JS. The main pages will be Jinja templates plus fetch/XHR calls for create/edit/reorder/delete.

## UI layout and behavior
Pages / Templates:
- `index.html` — shows list of stories with Create button and link to each story.
-- `story_edit.html` — main editor for a story; left column: cards grouped into two sections (Act 1 & 3 combined as MICE cards, and Act 2 as Try cards); right column: outline area with Refresh button.

Story editor details (left column):
- Left column shows two stacked sections (vertical scroll): first "Act 1 & 3 (MICE cards)" and then "Act 2 (Try cards)". The whole left area scrolls vertically.
- The "Act 1 & 3" section contains MICE-style cards. Each MICE card represents a narrative thread with an opening (Act 1) and a closing (Act 3). The MICE card stores an `open_body` (Act 1 content) and a `close_body` (Act 3 content).
- The "Act 2" section contains Try cards. Each Try card stores a single `body` (Act 2 content).
- Each section shows its cards in order. Each card shows `title` and truncated preview of the relevant body (for MICE cards show a short preview of `open_body`).
- Controls for each card: Edit (inline or small expand), Delete.
- A small "New Card" control per section (creates a new card at the end of that section). When creating a card in the "Act 1 & 3" section the UI should collect both opening and closing text (can be separate fields or a single editor with explicit open/close areas).
- Reordering: drag-and-drop enabled only within a section (MICE or Act2). When reorder completes, client calls `POST /stories/{id}/cards/reorder` with the section and the new ordered IDs for that section; server updates `position` and returns success.
- Editing: clicking a card opens an inline editor (expand to reveal the relevant textareas and a text input for `title`) — on blur or on Save the client POSTs update; server persists and returns updated card.

Outline area (right column):
- Shows a Refresh button at top. When clicked, it GETs `/stories/{id}/outline` and replaces the right column with rendered HTML of the returned Markdown.
- Simple styling: bulleted list; Markdown headings for acts (e.g., "Act 1") and card titles/body as nested bullets.

## Save strategy
- Autosave recommended: create/edit/delete/reorder operations are persisted immediately with API calls. This minimizes UI complexity and eliminates an explicit Save button.
- The Refresh button only controls outline (presentation), not persistence.

## Deletion semantics
- Deleting a card permanently removes it from the `cards` table. There is no trash for MVP.

## Seed content
- Recommend providing a single demo story with a few example cards to illustrate the three-act flow. This will help new users understand the Mice Quotient structure.

## Implementation milestones (small, 1–2 week total for a single developer)
1. Project scaffolding and wiring (1–2 days)
   - Create AIR/FastAPI app, SQLite setup, basic Jinja templating, static assets for Tailwind & DaisyUI via CDN.
2. Data model & DB migrations (1 day)
   - Implement `stories` and `cards` tables and small migration script or SQL init.
3. Stories CRUD + list page (1 day)
   - Implement `/stories` endpoints and `index.html`.
4. Story editor UI + cards CRUD (2–3 days)
   - Create `story_edit.html` with left cards grouped into two sections (Act1&3 MICE cards, and Act2 Try cards), create/edit/delete card endpoints, inline editor and autosave.
5. Drag-and-drop within-act reorder (1–2 days)
   - Implement JS drag-and-drop (native HTML5 or lightweight lib) and `/cards/reorder` endpoint.
6. Outline generation + Refresh button (0.5–1 day)
   - Implement `/stories/{id}/outline` to render Markdown from DB content and show it in the right column.
7. Polish, seed content, tests (1–2 days)
   - Add a demo story, basic unit tests (pytest) for models and outline generation, small smoke test for endpoints.

## Acceptance criteria
- Create, open, and delete multiple stories.
-- Create/edit/delete MICE and Act2 cards; edits persist immediately.
-- Drag-and-drop reorders cards within their section and reorder persists.
- Right column renders the outline when Refresh is clicked and reflects persisted card order and content.
- No user accounts required; everything stored server-side in SQLite and survives server restart.

## Edge cases and notes
- When reordering, positions should be normalized (1..N) for that act to avoid gaps.
- Concurrency: With no user accounts and low user counts, last-write-wins is acceptable. If multiple clients edit the same story concurrently, changes may overwrite each other.
- Large story sizes are not going to be a concern in MVP
- AI features, export, sharing, mobile-first UI, or admin UI are out of scope for MVP.