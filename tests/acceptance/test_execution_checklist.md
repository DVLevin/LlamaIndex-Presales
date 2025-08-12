# Test Execution Checklist - LlamaIndex Pre-sales Pipeline

## Pre-Test Setup

### ✅ Environment Verification
- [ ] **Application Running**: Streamlit app accessible at http://localhost:8501
- [ ] **API Keys**: OpenRouter and Jina keys configured in `.env.local`
- [ ] **Browser**: Use Chrome/Firefox with developer tools available
- [ ] **Screen Recording**: Optional - record test sessions for review
- [ ] **Test Data**: Have sample transcripts and business content ready

### ✅ Test Categories Priority Order
Execute tests in this priority sequence:

1. **🎯 Core Workflow** (`core_workflow.feature`) - **HIGHEST PRIORITY**
2. **🗺️ Navigation & Progress** (`navigation_and_progress.feature`) - **HIGH PRIORITY** 
3. **💾 Project Management** (`project_management.feature`) - **HIGH PRIORITY**
4. **📋 Document Editing** (`document_editing.feature`) - **MEDIUM PRIORITY**
5. **🤖 AI Processing** (`ai_processing.feature`) - **MEDIUM PRIORITY**
6. **💰 Business Value** (`business_value.feature`) - **VALIDATION PRIORITY**

---

## Core Workflow Test Execution

### Test: `core_workflow.feature`

#### Scenario: End-to-End Customer Transcript to Proposal Package

**🟢 MANUAL EXECUTION STEPS:**

1. **Setup Phase**
   - [ ] Open http://localhost:8501 in browser
   - [ ] Verify application loads without errors
   - [ ] Check that sidebar navigation is visible

2. **Input Phase**
   - [ ] Navigate to Input page (should be default)
   - [ ] Enter the Acme Manufacturing transcript (provided in test)
   - [ ] Set customer name: "Acme Manufacturing Corp"
   - [ ] Set content type: "Customer Transcript"
   - [ ] Click "Save & Continue to Analysis"
   - [ ] **VERIFY**: Redirected to Analysis page
   - [ ] **VERIFY**: Success message appears
   - [ ] **VERIFY**: Input summary shows correct customer name

3. **Analysis Phase**
   - [ ] Click "Analyze Content with AI"
   - [ ] Wait for analysis completion
   - [ ] **VERIFY**: Transcript detection shows "Yes"
   - [ ] **VERIFY**: Manufacturing industry detected
   - [ ] **VERIFY**: Budget indicators show "$500K"
   - [ ] **VERIFY**: Timeline shows "Q2 2025"
   - [ ] **VERIFY**: All agents (Conversa, Conny, ProDy, Marketing) recommended

4. **Processing Phase**
   - [ ] Click "Start AI Processing"
   - [ ] **VERIFY**: Redirected to Processing page
   - [ ] **VERIFY**: Agent sequence visualization appears
   - [ ] Click "Demo Mode (Fast)"
   - [ ] **VERIFY**: Progress updates in real-time
   - [ ] **VERIFY**: Each agent shows processing status
   - [ ] **VERIFY**: Progress reaches 100%
   - [ ] **VERIFY**: Success message appears

5. **Review Phase**
   - [ ] Click "View Results"
   - [ ] **VERIFY**: Redirected to Review page
   - [ ] **VERIFY**: Multiple documents available
   - [ ] Select "Problem Overview" document
   - [ ] **VERIFY**: Document content loads in editor
   - [ ] Modify title to "Acme Manufacturing - Problem Analysis"
   - [ ] Add "## Risk Assessment" section
   - [ ] Click "Save Changes"
   - [ ] **VERIFY**: Success message appears

6. **Completion Phase**
   - [ ] Click "Mark Review Complete"
   - [ ] **VERIFY**: Success message and balloons appear
   - [ ] Click "Export Final Package"
   - [ ] **VERIFY**: Download button appears
   - [ ] **VERIFY**: Filename includes "Acme_Manufacturing_Corp"

7. **Projects Verification**
   - [ ] Navigate to Projects page
   - [ ] **VERIFY**: Project listed with "Acme Manufacturing Corp"
   - [ ] **VERIFY**: Status shows "Completed"
   - [ ] **VERIFY**: Artifact count shows multiple documents

**🎯 SUCCESS CRITERIA:**
- [ ] Complete workflow executes without errors
- [ ] All verification points pass
- [ ] Professional documents are generated
- [ ] Project is properly saved
- [ ] Export functionality works

---

## Navigation & Progress Test Execution

### Test: `navigation_and_progress.feature`

#### Scenario: Multi-Page Navigation Flow with Progress Tracking

**🟢 MANUAL EXECUTION STEPS:**

1. **Initial State Verification**
   - [ ] Open application fresh (no previous session)
   - [ ] **VERIFY**: Sidebar shows Smart Input (💭) as accessible
   - [ ] **VERIFY**: Other pages show as locked
   - [ ] **VERIFY**: Progress shows 0/4 steps completed

2. **Navigation Locking Test**
   - [ ] Try clicking locked "Content Analysis" page
   - [ ] **VERIFY**: Cannot navigate to locked page
   - [ ] **VERIFY**: Remains on current page

3. **Progressive Unlocking Test**
   - [ ] Complete Input phase with any content
   - [ ] **VERIFY**: Input shows ✅ in sidebar
   - [ ] **VERIFY**: Analysis page becomes unlocked
   - [ ] **VERIFY**: Progress shows 1/4 completed
   - [ ] Complete Analysis phase
   - [ ] **VERIFY**: Analysis shows ✅ in sidebar
   - [ ] **VERIFY**: Processing page unlocks
   - [ ] **VERIFY**: Progress shows 2/4 completed

4. **Quick Actions Test**
   - [ ] Click "🆕 New Project" in sidebar
   - [ ] **VERIFY**: Progress resets to 0/4
   - [ ] **VERIFY**: All pages reset to appropriate state
   - [ ] **VERIFY**: Redirected to Input page

5. **Demo Mode Test**
   - [ ] Click "🎭 Demo Mode" in sidebar
   - [ ] **VERIFY**: Sample data loads automatically
   - [ ] **VERIFY**: Balloons or celebration appears
   - [ ] **VERIFY**: Input marked as completed
   - [ ] **VERIFY**: Redirected to Analysis with sample data

**🎯 SUCCESS CRITERIA:**
- [ ] Navigation locking/unlocking works correctly
- [ ] Progress tracking updates accurately
- [ ] Quick actions function as expected
- [ ] Demo mode provides complete sample workflow

---

## Project Management Test Execution

### Test: `project_management.feature`

#### Scenario: Create and Save Complete Project with All Artifacts

**🟢 MANUAL EXECUTION STEPS:**

1. **Project Creation**
   - [ ] Complete a full workflow (use demo mode for speed)
   - [ ] Ensure project gets saved with customer name

2. **Projects Page Verification**
   - [ ] Navigate to Projects page
   - [ ] **VERIFY**: Project listed with correct details:
     - Customer name
     - Status (Completed)
     - Artifact count
     - Creation date

3. **Project Detail View**
   - [ ] Click "👁️ View" on the project
   - [ ] **VERIFY**: Detailed project view opens
   - [ ] **VERIFY**: All artifacts listed
   - [ ] **VERIFY**: Original input preserved
   - [ ] **VERIFY**: Project metadata correct

4. **Export Functionality**
   - [ ] Click "📦 Export Project"
   - [ ] **VERIFY**: ZIP file downloads
   - [ ] Extract ZIP and verify contains:
     - project_info.json
     - original_input.txt
     - artifacts/ folder with .md files

5. **Project Resume**
   - [ ] Create a new project but stop at Analysis phase
   - [ ] Navigate to Projects page
   - [ ] Click "✏️ Resume" on the incomplete project
   - [ ] **VERIFY**: Redirected to Analysis page
   - [ ] **VERIFY**: Previous input/analysis loaded
   - [ ] **VERIFY**: Can continue workflow

**🎯 SUCCESS CRITERIA:**
- [ ] Projects save automatically with all artifacts
- [ ] Project details view shows complete information
- [ ] Export creates proper ZIP package
- [ ] Resume functionality restores session state

---

## Test Results Documentation

### Test Session: [Date/Time]
**Tester**: [Name]  
**Environment**: [Browser/OS]  
**Application Version**: [Git commit or date]

#### Overall Results Summary
- [ ] **Core Workflow**: ✅ Pass / ❌ Fail / ⚠️ Partial
- [ ] **Navigation & Progress**: ✅ Pass / ❌ Fail / ⚠️ Partial  
- [ ] **Project Management**: ✅ Pass / ❌ Fail / ⚠️ Partial
- [ ] **Document Editing**: ✅ Pass / ❌ Fail / ⚠️ Partial
- [ ] **AI Processing**: ✅ Pass / ❌ Fail / ⚠️ Partial
- [ ] **Business Value**: ✅ Pass / ❌ Fail / ⚠️ Partial

#### Critical Issues Found
| Issue | Scenario | Severity | Description |
|-------|----------|----------|-------------|
| [ID] | [Test name] | High/Med/Low | [Description] |

#### Performance Observations
- **Workflow Completion Time**: [X] minutes
- **Page Load Performance**: Fast/Acceptable/Slow
- **Demo Mode Performance**: [X] seconds
- **UI Responsiveness**: Excellent/Good/Poor

#### User Experience Notes
- **Intuitive Navigation**: Yes/No - [Comments]
- **Clear Instructions**: Yes/No - [Comments]  
- **Error Handling**: Good/Poor - [Comments]
- **Professional Appearance**: Yes/No - [Comments]

#### Business Value Validation
- **30% Time Reduction**: Achieved/Not Achieved - [Measurement]
- **Professional Output**: Yes/No - [Assessment]
- **Customer-Ready Documents**: Yes/No - [Assessment]

#### Recommendations
1. [Priority] - [Recommendation]
2. [Priority] - [Recommendation]
3. [Priority] - [Recommendation]

---

## Quick Smoke Test (5 Minutes)

For rapid validation, execute this minimal test:

1. [ ] Open application
2. [ ] Load demo mode
3. [ ] Run through complete workflow (Input → Analysis → Processing → Review)
4. [ ] Verify documents generate
5. [ ] Check Projects page shows saved project
6. [ ] Export project package

**Result**: ✅ Pass / ❌ Fail

**Notes**: [Any critical issues or observations]

---

**Ready to validate the LlamaIndex Pre-sales AI Pipeline!** 🚀