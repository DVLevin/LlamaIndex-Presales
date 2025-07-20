# Requirement Extraction Tool

## Tool Purpose
Extract structured business and technical requirements from customer conversations, documents, or discovery sessions.

## Input Format
**Source Material**: [Transcript, document, or conversation notes]
**Analysis Focus**: [Specific areas to focus on - functional, non-functional, constraints, etc.]
**Priority Level**: [High/Medium/Low priority requirements only, or all requirements]

## Output Structure

### Functional Requirements
**Format**: [REQ-F-001] [Requirement Statement]
- **Description**: [Detailed requirement description]
- **Business Rationale**: [Why this requirement is needed]
- **Acceptance Criteria**: [How to verify requirement is met]
- **Priority**: [Must Have/Should Have/Could Have/Won't Have]
- **Source**: [Quote or reference from source material]

**Example**:
[REQ-F-001] System must integrate with existing CRM platform
- **Description**: The solution must seamlessly integrate with Salesforce to sync customer data and opportunity information in real-time
- **Business Rationale**: Sales team relies on Salesforce as single source of truth for customer relationships
- **Acceptance Criteria**: Bi-directional sync with <5 minute latency, 99.9% data accuracy
- **Priority**: Must Have
- **Source**: "We absolutely need this to work with Salesforce - that's non-negotiable" (Sales Director, transcript line 45)

### Non-Functional Requirements
**Format**: [REQ-NF-001] [Requirement Statement]
- **Category**: [Performance/Security/Usability/Reliability/Scalability]
- **Specification**: [Measurable requirement details]
- **Testing Criteria**: [How requirement will be validated]
- **Priority**: [Must Have/Should Have/Could Have/Won't Have]
- **Source**: [Quote or reference from source material]

**Example**:
[REQ-NF-001] System must support 500 concurrent users
- **Category**: Performance
- **Specification**: Peak load of 500 concurrent users with <2 second response time for 95% of requests
- **Testing Criteria**: Load testing with 500 simulated users performing typical workflows
- **Priority**: Must Have
- **Source**: "We have about 400 people who would use this daily, with spikes up to 500" (IT Manager, transcript line 78)

### Business Requirements
**Format**: [REQ-B-001] [Requirement Statement]
- **Business Objective**: [What business goal this supports]
- **Success Metrics**: [How success will be measured]
- **Stakeholder**: [Who owns or benefits from this requirement]
- **Priority**: [Must Have/Should Have/Could Have/Won't Have]
- **Source**: [Quote or reference from source material]

**Example**:
[REQ-B-001] Reduce customer onboarding time by 50%
- **Business Objective**: Improve customer experience and reduce operational costs
- **Success Metrics**: Average onboarding time reduced from 14 days to 7 days within 6 months
- **Stakeholder**: Customer Success Manager
- **Priority**: Must Have
- **Source**: "Our biggest pain point is how long it takes to get new customers up and running" (CSM, transcript line 23)

### Constraints
**Format**: [CON-001] [Constraint Statement]
- **Type**: [Technical/Budget/Timeline/Regulatory/Organizational]
- **Description**: [Detailed constraint explanation]
- **Impact**: [How this constraint affects the solution]
- **Negotiability**: [Fixed/Flexible/Negotiable]
- **Source**: [Quote or reference from source material]

**Example**:
[CON-001] Must comply with SOX financial reporting requirements
- **Type**: Regulatory
- **Description**: Solution must maintain audit trails and controls for all financial data processing
- **Impact**: Requires enhanced security, logging, and approval workflows
- **Negotiability**: Fixed
- **Source**: "We're a public company so SOX compliance isn't optional" (CFO, transcript line 156)

## Extraction Guidelines

### Requirement Quality Criteria
- **Specific**: Requirement is precisely defined, not vague
- **Measurable**: Success criteria can be objectively verified  
- **Achievable**: Requirement is technically and practically feasible
- **Relevant**: Requirement supports business objectives
- **Time-bound**: Implementation timeline or performance criteria specified

### Analysis Techniques
1. **Direct Requirements**: Explicitly stated needs and specifications
2. **Implied Requirements**: Needs inferred from context and problems described
3. **Derived Requirements**: Requirements that emerge from analysis of stated needs
4. **Stakeholder Analysis**: Requirements from different user perspectives

### Prioritization Framework
- **Must Have (M)**: Critical requirements without which the solution fails
- **Should Have (S)**: Important requirements that add significant value
- **Could Have (C)**: Nice-to-have requirements that enhance the solution
- **Won't Have (W)**: Requirements explicitly excluded from current scope

## Usage Instructions

### Step 1: Source Analysis
1. **Read through source material** completely to understand context
2. **Identify all stakeholders** mentioned and their roles
3. **Note explicit statements** about needs, problems, and constraints
4. **Look for implied requirements** from problem descriptions

### Step 2: Requirement Extraction
1. **Extract functional requirements** - what the system must do
2. **Identify non-functional requirements** - how well the system must perform
3. **Document business requirements** - what business outcomes are needed
4. **Capture all constraints** - limitations and restrictions

### Step 3: Requirement Analysis
1. **Assess requirement quality** using SMART criteria
2. **Assign priorities** based on business impact and stakeholder emphasis
3. **Identify conflicts** between requirements from different stakeholders
4. **Flag assumptions** that need validation

### Step 4: Validation
1. **Cross-reference with source material** to ensure accuracy
2. **Check for completeness** - are there gaps in requirements coverage?
3. **Verify traceability** - can each requirement be traced to source?
4. **Assess feasibility** - are requirements technically achievable?

## Common Requirement Types

### Integration Requirements
- Data synchronization needs
- API connectivity requirements
- Single sign-on and authentication
- Third-party system connections

### User Experience Requirements  
- Interface design preferences
- Workflow and process requirements
- Accessibility needs
- Mobile/device support

### Data Requirements
- Data migration needs
- Data quality and cleansing
- Reporting and analytics
- Data retention and archival

### Security Requirements
- Authentication and authorization
- Data encryption and protection
- Compliance and regulatory needs
- Audit trails and logging

## Quality Checklist

Before finalizing requirement extraction:
- [ ] All requirements have unique identifiers
- [ ] Each requirement has clear acceptance criteria
- [ ] Priorities are assigned based on business value
- [ ] Requirements are traceable to source material
- [ ] Conflicts and dependencies are identified
- [ ] Assumptions requiring validation are flagged
- [ ] Requirements follow SMART criteria
- [ ] Non-functional requirements are quantified
- [ ] Stakeholder ownership is clear

## Output Example

```markdown
## Requirements Summary
**Total Requirements**: 23 (15 Functional, 5 Non-Functional, 3 Business)
**Must Have**: 12 requirements
**Should Have**: 8 requirements  
**Could Have**: 3 requirements

### Top Priority Requirements
1. [REQ-F-001] CRM Integration - Must Have
2. [REQ-B-001] 50% Onboarding Time Reduction - Must Have
3. [REQ-NF-001] 500 Concurrent User Support - Must Have

### Key Constraints
1. [CON-001] SOX Compliance - Fixed
2. [CON-002] $250K Budget Limit - Flexible
3. [CON-003] 6-Month Implementation - Negotiable
```

This tool helps ensure comprehensive, structured requirement capture that forms a solid foundation for solution design and proposal development.