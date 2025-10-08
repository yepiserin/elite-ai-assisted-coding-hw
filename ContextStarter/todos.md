# Time Zone Converter - Development To-Dos

## Step 1: Hello World with Air Framework
- [x] Verify the basic Air app runs successfully
- [x] Test that you can access the app in browser at localhost
- [x] Confirm the "Hello, Air!" message displays correctly

**User Test:** Visit the app URL and see a working web page.

---

## Step 2: Basic Page Structure and Title
- [x] Change page title to "Time Zone Converter"
- [x] Add a descriptive subtitle or tagline
- [x] Switch to Pico CSS layout (as specified in plan)

**User Test:** Page looks like a time zone converter app, not a generic hello world.

---

## Step 3: Source Time Zone Selector
- [x] Add dropdown for source time zone selection
- [x] Populate with 10-12 cities from the plan (San Francisco, Chicago, Washington D.C., London, Paris, Berlin, Manila, Tokyo, Singapore, Sydney)
- [x] Set Washington D.C. (America/New_York) as default selection
- [x] Display selected time zone on the page

**User Test:** Can select a time zone from dropdown and see it reflected on the page.

---

## Step 4: Time Input Selector
- [x] Add time picker dropdown with 30-minute increments
- [x] Use 12-hour format with AM/PM
- [x] Generate all time options (12:00 AM, 12:30 AM, 1:00 AM, etc.)
- [x] Display selected time on the page

**User Test:** Can select a time from dropdown and see it displayed.

---

## Step 5: Display Target Time Zones List
- [ ] Create a list/table showing all 10-12 target cities
- [ ] Display city names in a clean, readable format
- [ ] Show placeholder times (e.g., "12:00 PM") for each city

**User Test:** See all target time zones listed on the page with placeholder times.

---

## Step 6: Basic Time Zone Conversion Logic
- [ ] Implement time zone offset calculation (ignoring DST per plan)
- [ ] Create function to convert source time to target time zones
- [ ] Display actual converted times for all cities based on selected source time and time zone

**User Test:** Select a time zone and time, see accurate converted times for all cities.

---

## Step 7: Add HTMX for Dynamic Updates
- [ ] Add HTMX to the project
- [ ] Make time zone selector trigger auto-update on change
- [ ] Make time picker trigger auto-update on change
- [ ] Conversions update without page refresh

**User Test:** Change time zone or time and see results update instantly without page reload.

---

## Step 8: Date Indicators (Today/Tomorrow/Yesterday)
- [ ] Calculate when converted times cross midnight boundaries
- [ ] Add "Today", "Tomorrow", or "Yesterday" labels next to times
- [ ] Display format: "Manila: 7:00 AM Tomorrow"

**User Test:** Select a late evening time and verify some cities show "Tomorrow".

---

## Step 9: Color Coding for Business Hours
- [ ] Implement business hours logic:
  - Green (9 AM - 5 PM): Good meeting time
  - Yellow (6 AM - 9 AM, 5 PM - 10 PM): Inconvenient
  - Red (10 PM - 6 AM): Unacceptable
- [ ] Apply background colors to each time zone result
- [ ] Ensure colors are subtle and text remains readable

**User Test:** Select different times and visually verify color coding makes sense (e.g., 2 PM should show green for most zones, 2 AM should show red).

---

## Step 10: Polish and Final Testing
- [ ] Test edge cases (midnight, noon, timezone boundaries)

**User Test:** Use the app as intended - select various times and time zones to find good meeting times. Verify the color coding makes decision-making quick and easy.

---

## Completion Checklist
- [ ] All features from plan.md are implemented
- [ ] App runs without errors
- [ ] HTMX provides seamless updates
- [ ] Color coding is intuitive and helpful
- [ ] Ready for demo/presentation
