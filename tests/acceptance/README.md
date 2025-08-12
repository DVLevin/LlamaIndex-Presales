# Acceptance Tests - LlamaIndex Pre-sales Pipeline

## Overview
This directory contains **Behavior-Driven Development (BDD)** acceptance tests written in **Gherkin syntax** for manual verification of the LlamaIndex Pre-sales AI Pipeline.

## Test Philosophy
- **User-Centric**: Tests written from the perspective of actual users (sales reps, account managers)
- **Business Value**: Each scenario validates specific business outcomes and value propositions
- **Manual Verification**: Tests can be executed manually by following the Given/When/Then steps
- **End-to-End**: Complete workflows from initial input to final deliverable

## How to Run Acceptance Tests

### Prerequisites
1. **Application Running**: Start the Streamlit application
   ```bash
   streamlit run streamlit_app/main.py
   ```

2. **API Keys Configured**: Ensure OpenRouter and Jina API keys are available in `.env.local`

3. **Browser Access**: Open http://localhost:8501 in your browser

### Test Execution Process
1. **Read the Feature File**: Understand the business scenario being tested
2. **Follow Given Steps**: Set up the test conditions as described
3. **Execute When Steps**: Perform the user actions specified
4. **Verify Then Steps**: Confirm the expected outcomes are achieved
5. **Document Results**: Note pass/fail status and any observations

### Test Categories
- **🎯 Core Workflow**: Complete proposal generation pipeline
- **💾 Project Management**: Project storage, retrieval, and management
- **🔍 Navigation**: Multi-page flow and progress tracking
- **🤖 AI Processing**: Content analysis and agent pipeline execution
- **📋 Document Management**: Artifact creation, editing, and export
- **🚀 Demo & Error Handling**: Edge cases and demonstration features

## Test Data
- Use the provided demo templates and sample content
- Create realistic customer scenarios for thorough testing
- Test with various content types (transcripts, strategic docs, etc.)

## Success Criteria
A test **PASSES** when:
- All Then statements are verified as true
- User experience feels intuitive and professional
- Business value is clearly demonstrated
- No critical errors or broken functionality

A test **FAILS** when:
- Any Then statement cannot be verified
- User encounters confusion or poor UX
- Expected business outcomes are not achieved
- Critical functionality is broken or inaccessible

## Reporting Issues
When tests fail, document:
1. **Scenario**: Which test scenario failed
2. **Step**: Specific Given/When/Then step that failed
3. **Expected**: What should have happened
4. **Actual**: What actually happened
5. **Environment**: Browser, OS, and any relevant details
6. **Screenshots**: Visual evidence of the issue

---

**Ready to validate the LlamaIndex Pre-sales AI Pipeline!**