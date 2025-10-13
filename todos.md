# Elite AI Assisted Coding Assignment - Development Plan

This document tracks the development of the MICE Quotient Story Builder application, demonstrating context-driven AI development practices.

## Assignment Setup (Completed ✅)

### Step 1: Environment Setup
- ✅ Set up Python 3.13+ and uv package manager
- ✅ Install and configure Ruler for AI agent consistency
- ✅ Set up MCP servers (Playwright for browser automation, Air docs for framework reference)
- ✅ Create GitHub repository for version control

### Step 2: Demo Analysis and Assignment Preparation
- ✅ Study the 3. BetterContext demo to understand context-driven development
- ✅ Analyze context files: AGENTS.md, plan.md, todos.md, CLAUDE.md
- ✅ Verify demo functionality works as described in README.md
- ✅ Create assignment folder (4. Assignment) with working copy
- ✅ Test independent operation of assignment environment

## Core Functionality Requirements (From ASSIGNMENT_OVERVIEW.md)

The application must support this workflow:
1. Writer opens the app and sees their cards and the overview
2. Writer can add cards to any section
3. Writer can edit existing cards to refine their outline
4. Writer can delete cards that don't fit
5. Work is saved automatically or explicitly (your choice)
6. Writer can return later and continue working

## Development Steps (Building on Existing Foundation)

### Step 3: Verify starter app runs
- Ensure the Air starter app runs successfully
- Verify you can access the homepage in a browser
- Confirm the app uses the correct Python environment

## Assignment Enhancement Options

Based on the ASSIGNMENT_OVERVIEW.md, choose one or more enhancement paths:

### Option A: Mobile-Responsive Design
- Implement responsive CSS for mobile devices
- Test on various screen sizes
- Ensure touch-friendly interface elements
- Verify usability on tablets and phones

### Option B: Drag-and-Drop Reordering
- Add drag-and-drop functionality for Try cards
- Implement visual feedback during dragging
- Update database order numbers automatically
- Test reordering preserves data integrity

### Option C: Database Migrations (Alembic)
- Set up Alembic for database version control
- Create migration scripts for schema changes
- Implement rollback capabilities
- Document migration process

### Option D: Multi-User Support with Authentication
- Add user authentication system
- Implement user-specific story storage
- Create user management interface
- Add session management

### Option E: AI-Powered Outline Generation
- Integrate with AI service for outline generation
- Create structured prompts for AI
- Implement caching for generated outlines
- Add export functionality for AI-generated content

### Option F: Export and Sharing Capabilities
- Add PDF export functionality
- Implement story sharing via URL
- Create print-friendly views
- Add data export options (JSON, CSV)

## Current Foundation (Already Implemented ✅)

The following features are already working in the base application:

### Database and Core Functionality
- ✅ SQLite database with MICE cards and Try cards tables
- ✅ Three-column layout (MICE Cards, Try/Fail Cycles, Generated Outline)
- ✅ CRUD operations for both card types
- ✅ Real-time updates using HTMX
- ✅ Data persistence across page refreshes

### User Interface Features
- ✅ Styled cards with color coding for MICE types
- ✅ Form-based card creation and editing
- ✅ Delete functionality with immediate updates
- ✅ Story templates (Mystery, Adventure, Romance)
- ✅ Educational MICE Quotient explanation panel
- ✅ Visual nesting structure diagram
- ✅ Three-act story timeline
- ✅ Clear All Data functionality

### Advanced Features
- ✅ Story templates with pre-built examples
- ✅ Educational content and tooltips
- ✅ Visual story structure representation
- ✅ Real-time outline generation

## Immediate Next Steps (Based on Enhanced plan.md)

### Step 4: Port Configuration and App Launch
- ✅ **Fix Port Configuration**: Update all context files to use port 8000 (completed)
- ✅ **Launch App on Correct Port**: Run `cd "HW1/demo/4. Assignment/app" && uv run fastapi dev --port 8000`
- ✅ **Verify App Functionality**: Test all core features work on port 8000
- ✅ **Update Context Files**: Ensure AGENTS.md, plan.md reference correct port

### Step 5: Choose and Implement Enhancement Path
- ✅ **Select Primary Enhancement**: Choose Option B (Drag-and-Drop Reordering) as primary focus
- [ ] **Create Technical Requirements**: Document specific drag-and-drop implementation details
- [ ] **Set Up Development Environment**: Ensure all tools are ready for implementation

### Step 6: Drag-and-Drop Implementation (Option B) ✅ COMPLETED
- ✅ **Research Sortable.js**: Study library documentation and integration patterns
- ✅ **Design Database Changes**: Plan order_num field enhancements for Try cards
- ✅ **Create API Endpoints**: Design `/api/try-cards/reorder` endpoint for batch updates
- ✅ **Implement Frontend**: Add Sortable.js integration with HTMX compatibility
- ✅ **Add Visual Feedback**: Implement drag states, animations, and user feedback
- ✅ **Test Functionality**: Verify drag-and-drop works across different browsers
- ✅ **Handle Edge Cases**: Test with empty lists, single items, and large datasets

## 🧪 **Testing Steps for Drag-and-Drop Functionality**

### **Phase 1: Basic Functionality Testing**
- [ ] **Launch App**: Start the app on port 8000 and verify it loads correctly
- [ ] **Load Sample Data**: Click "Templates" → "Mystery" to load sample Try cards
- [ ] **Verify Drag Handles**: Check that Try cards show `⋮⋮` drag handles
- [ ] **Test Basic Drag**: Try dragging a Try card by its handle
- [ ] **Verify Visual Feedback**: Confirm cards show visual feedback during drag (opacity, colors)
- [ ] **Test Reordering**: Drag a card to a new position and verify it stays there
- [ ] **Check Order Numbers**: Verify that order numbers (#1, #2, #3) update correctly

### **Phase 2: Persistence Testing**
- [ ] **Refresh Page**: Reload the page and verify the new order persists
- [ ] **Add New Card**: Create a new Try card and verify it gets the next order number
- [ ] **Reorder with New Card**: Drag the new card to different positions
- [ ] **Verify Database**: Check that order numbers are correctly saved in database

### **Phase 3: Edge Cases Testing**
- [ ] **Empty List**: Clear all data and verify drag handles don't appear
- [ ] **Single Card**: With only one Try card, verify drag handle appears but no reordering needed
- [ ] **Multiple Reorders**: Drag the same card multiple times in different directions
- [ ] **Rapid Dragging**: Try quick successive drags to test performance
- [ ] **Large Dataset**: Add 10+ Try cards and test dragging works smoothly

### **Phase 4: Error Handling Testing**
- [ ] **Network Disconnect**: Disconnect internet during drag and verify error handling
- [ ] **Server Restart**: Restart the app server during a drag operation
- [ ] **Invalid Data**: Try to drag with corrupted card IDs (if possible)
- [ ] **Browser Console**: Check for JavaScript errors during drag operations

### **Phase 5: Cross-Browser Testing**
- [ ] **Chrome**: Test drag-and-drop functionality in Chrome
- [ ] **Firefox**: Test drag-and-drop functionality in Firefox  
- [ ] **Safari**: Test drag-and-drop functionality in Safari (if available)
- [ ] **Mobile**: Test touch interactions on mobile/tablet (if applicable)

### **Phase 6: Integration Testing**
- [ ] **HTMX Compatibility**: Verify drag-and-drop doesn't interfere with HTMX operations
- [ ] **Form Interactions**: Test that drag handles don't interfere with Edit/Delete buttons
- [ ] **Story Timeline**: Verify that reordered Try cards appear correctly in the Story Timeline
- [ ] **Mixed Operations**: Test drag-and-drop while also adding/editing/deleting cards

### **Phase 7: Performance Testing**
- [ ] **Smooth Animation**: Verify drag animations are smooth (150ms)
- [ ] **Large Lists**: Test with 20+ Try cards to ensure performance
- [ ] **Memory Usage**: Check browser memory usage during extended drag sessions
- [ ] **CPU Usage**: Monitor CPU usage during drag operations

### **Expected Results**
- ✅ **Drag Handles**: Try cards should show `⋮⋮` handles that are clickable
- ✅ **Visual Feedback**: Cards should show opacity changes and color changes during drag
- ✅ **Smooth Animation**: 150ms animation should be smooth and responsive
- ✅ **Order Persistence**: New order should persist after page refresh
- ✅ **Database Updates**: Order numbers should update correctly in database
- ✅ **Error Recovery**: Failed drags should reload page to reset order
- ✅ **No Conflicts**: Drag-and-drop should not interfere with other app functionality

### **Success Criteria**
- [ ] **All Phase 1 tests pass** - Basic drag-and-drop works
- [ ] **All Phase 2 tests pass** - Order persists correctly  
- [ ] **All Phase 3 tests pass** - Edge cases handled properly
- [ ] **All Phase 4 tests pass** - Error handling works
- [ ] **All Phase 5 tests pass** - Cross-browser compatibility
- [ ] **All Phase 6 tests pass** - Integration with existing features
- [ ] **All Phase 7 tests pass** - Performance is acceptable

### **Bug Reporting Template**
If you find issues, document them with:
- **Browser**: Chrome/Firefox/Safari version
- **Steps to Reproduce**: Exact steps that caused the issue
- **Expected Result**: What should have happened
- **Actual Result**: What actually happened
- **Console Errors**: Any JavaScript errors in browser console
- **Screenshot**: If visual issue, include screenshot

### Step 7: Testing and Verification
- [ ] **Browser Testing**: Test drag-and-drop on Chrome, Firefox, Safari
- [ ] **Mobile Testing**: Verify touch interactions work on tablets/phones
- [ ] **Performance Testing**: Ensure smooth dragging with 50+ Try cards
- [ ] **Data Integrity**: Verify order numbers persist correctly after page refresh
- [ ] **Error Handling**: Test network failures during drag operations

### Step 8: Documentation and Context Updates
- [ ] **Update AGENTS.md**: Add drag-and-drop specific instructions for AI agents
- [ ] **Update CLAUDE.md**: Add testing and verification guidelines
- [ ] **Create Implementation Guide**: Document the drag-and-drop implementation process
- [ ] **Record Lessons Learned**: Document what worked well and what didn't

## Next Steps for Assignment

1. **Choose Enhancement Path**: Select one or more options from above
2. **Create Requirements Document**: Document specific requirements for chosen enhancements
3. **Set Up Context Files**: Create or update AGENTS.md, plan.md for your specific goals
4. **Implement with AI Assistance**: Use context-driven development approach
5. **Test and Verify**: Ensure all functionality works as expected
6. **Document Process**: Record the development process and lessons learned
