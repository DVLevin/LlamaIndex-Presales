# Frontend Acceptance Tests

This directory contains acceptance tests for the LlamaIndex Presales AI frontend application. These tests follow BDD/ATDD principles and are designed for manual verification.

## Prerequisites

Before running acceptance tests:

1. **Install dependencies**:
   ```bash
   cd fe/
   npm install
   ```

2. **Start development server**:
   ```bash
   npm run dev
   ```
   Application will be available at http://localhost:5173

3. **Backend requirement**:
   - For full functionality, the backend WebSocket server should be running on `ws://localhost:8000`
   - Without backend, you can still test UI components but WebSocket features will show connection errors

## Test Structure

Each `.feature` file contains Gherkin-formatted test scenarios:
- **Feature**: High-level functionality description
- **Scenario**: Specific test case with Given/When/Then steps
- **Background**: Common setup steps for all scenarios in a feature

## Running Tests

### Manual Testing Process

1. **Read the feature file** to understand the test scenario
2. **Follow the steps** exactly as written in the Given/When/Then format
3. **Verify expected outcomes** match what you observe
4. **Document any failures** or unexpected behavior

### Test Execution Commands

```bash
# Display acceptance test information
npm run test:acceptance

# Run unit tests (for comparison)
npm test

# Start dev server for testing
npm run dev
```

## Test Coverage

### Core Features Tested
- ✅ Chat interface with message rendering
- ✅ WebSocket connection management
- ✅ Agent status dashboard
- ✅ Real-time message streaming
- ✅ Navigation between chat and agents
- ✅ Error handling and connection status

### Browser Compatibility
Test in the following browsers:
- Chrome (primary)
- Firefox
- Safari
- Edge

### Mobile Testing
Test responsive design on:
- Mobile devices (< 768px)
- Tablets (768px - 1024px) 
- Desktop (> 1024px)

## Reporting Issues

When tests fail, document:
1. **Browser version** and operating system
2. **Steps to reproduce** the issue
3. **Expected vs actual behavior**
4. **Screenshots or console errors** if applicable
5. **Backend connection status** (connected/disconnected)

## Test Data

### Sample Messages
Use these for consistent testing:
- "Research Acme Corp for a potential deal"
- "What's the qualification score for this lead?"
- "Generate a proposal for enterprise software licensing"
- "Review the attached contract terms"

### Sample Agent Names
Expected in the system:
- Research Agent
- Qualification Agent  
- Proposal Agent
- Review Agent

## Success Criteria

All acceptance tests must pass before considering a feature complete. Pay special attention to:

1. **User Experience**: Interface is intuitive and responsive
2. **Real-time Updates**: Messages and agent status update immediately
3. **Error Handling**: Graceful degradation when backend is unavailable
4. **Accessibility**: Components are keyboard navigable and screen reader friendly
5. **Performance**: No noticeable delays or UI blocking during interactions