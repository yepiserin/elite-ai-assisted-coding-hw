# Code Refactoring Recommendations - Round 2

## Completed Refactorings ✅

1. ✅ **Extracted `templates.py`** - Consolidated 3 template endpoints into 1 generic handler, removed ~80 lines
2. ✅ **Extracted `components.py`** - Moved all rendering functions and tooltip constants, removed ~180 lines
3. ✅ **Overall reduction**: 1020 → 725 lines (295 lines removed, 29% reduction)

---

## Current State Analysis

- **main.py**: 725 lines
- **Endpoints**: 20 route handlers
- **Database operations**: 15 `with Session(engine)` blocks scattered across endpoints
- **Form builders**: 4 large form-building functions (~60 lines each = 240 lines total)
- **Helper functions**: 1 small helper (`_info_row`)

---

## New Refactoring Candidates

### 1. Extract Database Operations to `db.py`
**Value: 9/10** | **Complexity Reduction: High** | **Thickness: Thick (data access layer)**

**Current:** Database CRUD scattered across 15 endpoints with repeated patterns

**Proposed:** Create `db.py`:
```python
from sqlmodel import Session, select
from models import MiceCard, TryCard

def get_all_mice_cards(session: Session) -> list[MiceCard]:
    return session.exec(select(MiceCard)).all()

def get_all_try_cards(session: Session) -> list[TryCard]:
    return session.exec(select(TryCard).order_by(TryCard.order_num)).all()

def get_mice_card(session: Session, card_id: int) -> MiceCard | None:
    return session.get(MiceCard, card_id)

def get_try_card(session: Session, card_id: int) -> TryCard | None:
    return session.get(TryCard, card_id)

def create_mice_card(session: Session, code: str, opening: str, closing: str, nesting_level: int) -> MiceCard:
    card = MiceCard(code=code, opening=opening, closing=closing, nesting_level=nesting_level)
    session.add(card)
    session.commit()
    session.refresh(card)
    return card

def update_mice_card(session: Session, card_id: int, code: str, opening: str, closing: str, nesting_level: int) -> MiceCard | None:
    card = session.get(MiceCard, card_id)
    if card:
        card.code = code
        card.opening = opening
        card.closing = closing
        card.nesting_level = nesting_level
        session.commit()
        session.refresh(card)
    return card

def delete_mice_card(session: Session, card_id: int) -> bool:
    card = session.get(MiceCard, card_id)
    if card:
        session.delete(card)
        session.commit()
        return True
    return False

def clear_all_cards(session: Session):
    for card in session.exec(select(MiceCard)):
        session.delete(card)
    for card in session.exec(select(TryCard)):
        session.delete(card)
    session.commit()

def load_template_data(session: Session, mice_data: list[dict], try_data: list[dict]):
    clear_all_cards(session)
    for data in mice_data:
        session.add(MiceCard(**data))
    for data in try_data:
        session.add(TryCard(**data))
    session.commit()

# Similar functions for Try cards...
```

**Benefits:**
- **Centralizes all database access** - one place to understand data operations
- **Removes 15 `with Session(engine)` blocks** from route handlers
- **Routes become pure business logic** - just call db functions
- **Easier to test** - can mock db functions
- **Consistent patterns** - all CRUD follows same structure
- **Clear separation**: routes handle HTTP, db.py handles data
- **Estimated reduction**: ~100-150 lines from main.py

**Tradeoffs:**
- Adds one more file
- But this is a **thick, cohesive abstraction** - all data access in one place
- Very clear purpose and benefit

**Recommendation:** **YES - High value, creates clear data access layer**

---

### 2. Extract Form Builders to `forms.py`
**Value: 7/10** | **Complexity Reduction: Medium-High** | **Thickness: Medium-Thick**

**Current:** 4 large form functions in main.py (~240 lines total):
- `mice_form()` - create new MICE card form (60 lines)
- `mice_edit()` - edit MICE card form (73 lines)
- `try_form()` - create new Try card form (70 lines)
- `try_edit()` - edit Try card form (85 lines)

**Proposed:** Create `forms.py`:
```python
import air

def mice_card_form(card: MiceCard | None = None) -> air.Form:
    """Build MICE card form for create or edit."""
    is_edit = card is not None

    return air.Form(
        _form_field("Type:", _mice_type_select(card.code if card else None)),
        _form_field("Opening:", _textarea(card.opening if card else "", "opening")),
        _form_field("Closing:", _textarea(card.closing if card else "", "closing")),
        _form_field("Nesting Level:", _number_input(card.nesting_level if card else 1)),
        _form_buttons(is_edit, card.id if card else None, "mice"),
        hx_post=f"/mice-cards" if not is_edit else f"",
        hx_put=f"/mice-cards/{card.id}" if is_edit else "",
        # ... rest of form config
    )

def try_card_form(card: TryCard | None = None) -> air.Form:
    """Build Try card form for create or edit."""
    # Similar structure

# Private helpers for form components
def _form_field(label: str, input_element) -> air.Div:
    ...

def _mice_type_select(selected: str | None) -> air.Select:
    ...
```

**Benefits:**
- Routes become 1-liners: `return mice_card_form(card)`
- Reduces duplication between create/edit forms
- Form logic separated from route handlers
- **Estimated reduction**: ~200 lines from main.py

**Tradeoffs:**
- Forms are somewhat coupled to routes (HTMX targets, etc.)
- Students need to jump between files to see full request flow
- Moderate thickness - forms are UI logic, not just data

**Recommendation:** **YES - Good separation, significant line reduction**

---

### 3. Create `session_context.py` for Database Session Management
**Value: 5/10** | **Complexity Reduction: Low** | **Thickness: Thin**

**Current:** Repeated `with Session(engine) as session:` in every route

**Proposed:** Dependency injection pattern:
```python
# session_context.py
from sqlmodel import Session
from fastapi import Depends

def get_session():
    with Session(engine) as session:
        yield session

# In routes:
@app.get("/mice-cards")
def get_mice(session: Session = Depends(get_session)):
    cards = db.get_all_mice_cards(session)
    ...
```

**Benefits:**
- Slightly cleaner routes
- FastAPI best practice

**Tradeoffs:**
- Adds complexity for beginners (dependency injection concept)
- Thin abstraction - only saves 1-2 lines per route
- Less explicit than current approach
- Harder to understand for students

**Recommendation:** **NO - Too thin, reduces educational clarity**

---

### 4. Extract Sample/Debug Routes to `debug_routes.py`
**Value: 4/10** | **Complexity Reduction: Low** | **Thickness: Medium**

**Current:** Two debug endpoints in main.py:
- `add_sample_mice()` - adds sample MICE card with hardcoded data
- `add_sample_try()` - adds sample Try card with hardcoded data

**Proposed:** Move to separate file or remove entirely

**Benefits:**
- Cleaner main.py
- Separates debugging code from production routes

**Tradeoffs:**
- Only ~60 lines total
- These might not even be used anymore (templates replaced this)
- Could just delete them instead

**Recommendation:** **DELETE THEM** - Templates replaced this functionality

---

### 5. Consolidate MICE and Try CRUD Patterns
**Value: 3/10** | **Complexity Reduction: Low** | **Thickness: N/A**

**Current:** Parallel CRUD routes for MICE and Try cards (10 routes each)

**Proposed:** Generic CRUD handler or route registration

**Benefits:**
- Less code duplication

**Tradeoffs:**
- Over-abstraction for only 2 card types
- Makes code harder to understand
- Students benefit from seeing explicit patterns

**Recommendation:** **NO - Clarity over brevity for educational purposes**

---

### 6. Extract MICE Quotient Educational Content
**Value: 8/10** | **Complexity Reduction: Medium** | **Thickness: Thick (content/data)**

**Current:** ~55 lines of educational content embedded in the index route (lines 96-150)

**Proposed:** Create `help_content.py` or add to `components.py`:
```python
# Option 1: help_content.py (separate file for content)
MICE_HELP_CONTENT = {
    "title": "MICE Quotient Story Structure",
    "intro": "The MICE Quotient is a plotting technique by Orson Scott Card...",
    "types": [
        {
            "code": "M",
            "name": "Milieu",
            "description": "Environment, setting, atmosphere",
            "example": "Character enters a new world → explores → leaves",
            "color": "blue"
        },
        # ... I, C, E
    ],
    "nesting": {
        "title": "Nesting Structure",
        "description": "Act 1 mirrors Act 3 in opposite order..."
    },
    "try_fail": {
        "title": "Try/Fail Cycles (Act 2)",
        "description": "Between setup and resolution...",
        "types": [...]
    }
}

# In components.py:
def render_mice_help_panel() -> air.Div:
    """Render the MICE Quotient educational help panel."""
    return air.Div(
        air.Div(
            air.Button(...),
            class_="mb-2"
        ),
        air.Div(
            # Build from MICE_HELP_CONTENT
            ...
        ),
        class_="mb-4"
    )
```

**Benefits:**
- **Separates content from code structure** - educational text is data, not logic
- **Easier to update help content** - no need to touch route code
- **Could be translated** - structured data makes i18n possible
- **Reduces index route complexity** - route focuses on page structure
- **Clear separation of concerns** - content vs presentation vs routing
- **Estimated reduction**: ~50-55 lines from main.py

**Tradeoffs:**
- Adds another file OR expands components.py
- Content structure needs careful design

**Recommendation:** **YES - Add `render_mice_help_panel()` to components.py, keep structured content in same file**

Rationale: This is educational content that's semantically part of the UI components. Keeping it with components.py makes sense since:
- It's rendered UI content
- It's used in exactly one place
- It's cohesive with other rendering functions
- Don't need a separate file just for help text

---

### 7. Move `_info_row` Helper to `components.py`
**Value: 2/10** | **Complexity Reduction: Minimal** | **Thickness: Thin**

**Current:** Small helper function in main.py for debug views

**Proposed:** Move to components.py since it's UI rendering

**Benefits:**
- Slightly cleaner main.py
- Groups all UI helpers together

**Tradeoffs:**
- Only 6 lines
- Only used in debug views that might get deleted
- Barely worth the import

**Recommendation:** **MAYBE - Only if keeping debug routes**

---

## Recommended Refactoring Plan - Round 2

### Phase 1: High-Value, Clear Benefit

1. **Extract `db.py`** (Value: 9/10) ⭐
   - Move all database CRUD operations
   - Create clean data access layer
   - Routes become HTTP handlers only
   - **Estimated reduction: ~100-150 lines**

2. **Extract MICE help panel to `components.py`** (Value: 8/10) ⭐
   - Create `render_mice_help_panel()` function
   - Separate educational content from route structure
   - **Estimated reduction: ~50-55 lines**

3. **Extract `forms.py`** (Value: 7/10) ⭐
   - Move all form-building functions
   - Consolidate create/edit form logic
   - **Estimated reduction: ~200 lines**

4. **Delete debug routes** (Value: 4/10)
   - Remove `add_sample_mice()` and `add_sample_try()`
   - Templates already provide this functionality
   - **Estimated reduction: ~60 lines**

**Total estimated reduction: ~410-465 lines**
**New main.py size: ~260-315 lines** (down from 725)

### Phase 2: Optional Polish

5. Move `_info_row` to components.py if still needed after deleting debug routes

---

## After Phase 1, Expected Structure

```
app/
├── main.py          (~260-315 lines - route handlers only)
├── db.py            (~150 lines - database operations)
├── forms.py         (~200 lines - form builders)
├── components.py    (~290 lines - UI components + help panel)
├── templates.py     (165 lines - template data)
├── models.py        (existing - database models)
└── layouts.py       (existing - page layout)
```

---

## Key Principles Maintained

1. **Thick over thin** - db.py and forms.py are cohesive, meaningful units
2. **Clear file purposes** - easy to know where to look for functionality
3. **Educational value** - separation makes each concern easier to understand
4. **Minimal file jumping** - related functionality grouped logically

---

## Summary

**Top Priority:**
1. Create `db.py` for database operations (Value: 9/10)
2. Extract MICE help panel to `components.py` (Value: 8/10)
3. Create `forms.py` for form builders (Value: 7/10)
4. Delete unused debug routes (Value: 4/10)

**Reject:**
- Session dependency injection (too thin, reduces clarity)
- Generic CRUD consolidation (over-abstraction)
- Session context manager (educational anti-pattern)

This round of refactoring would bring main.py from **725 → ~260-315 lines** (a **57-64% reduction!**) while maintaining clear, educational code structure.
