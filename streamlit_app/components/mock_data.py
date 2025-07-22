"""
Mock Data Generator for Demo Purposes
Generate realistic sample outputs to demonstrate system capabilities
"""
import streamlit as st
from datetime import datetime
from typing import Dict, Any


def generate_mock_documents() -> Dict[str, Any]:
    """Generate mock documents for demonstration"""
    
    return {
        "Problem Overview": {
            "title": "Problem Overview: Acme Corp Digital Transformation",
            "description": "Analysis of current challenges and business impact",
            "content": get_mock_problem_overview(),
            "format": "markdown",
            "metadata": {
                "generated_by": "ProDy Agent",
                "generation_time": "45 seconds", 
                "word_count": 385,
                "business_impact": "$600K annual revenue loss"
            }
        },
        "Process Overview": {
            "title": "Process Overview: Inventory Management Solution",
            "description": "Detailed implementation methodology and approach",
            "content": get_mock_process_overview(),
            "format": "markdown",
            "metadata": {
                "generated_by": "ProDy Agent",
                "generation_time": "52 seconds",
                "word_count": 445,
                "implementation_phases": 4
            }
        },
        "Process Visualization": {
            "title": "Process Visualization: Before/After Comparison",
            "description": "Process flow diagrams showing transformation",
            "content": get_mock_process_visualization(),
            "format": "markdown",
            "metadata": {
                "generated_by": "ProDy Agent",
                "generation_time": "38 seconds", 
                "diagrams_generated": 2,
                "efficiency_improvement": "75%"
            }
        },
        "Investment Proposal": {
            "title": "Investment Proposal: ROI Analysis & Budget",
            "description": "Financial analysis and implementation budget",
            "content": get_mock_investment_proposal(),
            "format": "markdown",
            "metadata": {
                "generated_by": "ProDy Agent",
                "generation_time": "65 seconds",
                "total_investment": "$150,000",
                "roi_timeline": "12 months"
            }
        },
        "Next Steps": {
            "title": "Next Steps: Implementation Roadmap",
            "description": "Actionable roadmap with clear next steps",
            "content": get_mock_next_steps(),
            "format": "markdown",
            "metadata": {
                "generated_by": "ProDy Agent", 
                "generation_time": "28 seconds",
                "action_items": 8,
                "stakeholders_involved": 5
            }
        },
        "Sales Presentation": {
            "title": "Executive Presentation: Digital Transformation ROI",
            "description": "Customer-facing sales deck with value proposition",
            "content": get_mock_sales_presentation(),
            "format": "markdown",
            "metadata": {
                "generated_by": "Marketing Agent",
                "generation_time": "72 seconds",
                "slides_equivalent": 12,
                "roi_highlighted": "$1.2M annual savings"
            }
        }
    }


def get_mock_problem_overview() -> str:
    """Generate mock problem overview document"""
    
    return """# Problem Overview: Acme Corp Inventory Management Transformation

## Executive Summary
Acme Corp is experiencing critical operational inefficiencies and significant revenue losses due to their legacy manual inventory management system, requiring urgent digital transformation to maintain competitive advantage and customer satisfaction.

## Current State Analysis
- **Manual Inventory Updates**: 3-4 hours of daily labor required for basic stock level maintenance
- **High Error Rates**: 15% inventory discrepancy rate causing customer dissatisfaction  
- **Revenue Leakage**: $50,000 monthly losses from stockouts and overselling incidents
- **Staff Inefficiency**: 20 hours weekly spent on manual data entry instead of value-added activities
- **Customer Impact**: Order cancellations and trust erosion due to poor inventory visibility

## Key Pain Points

### Operational Challenges
- **Manual Process Dependency**: All inventory updates require human intervention
- **Data Accuracy Issues**: High error rates in stock level tracking
- **Time-Intensive Operations**: Significant labor hours spent on routine tasks
- **System Integration Gap**: Lack of real-time connectivity with Salesforce CRM

### Business Impact
- **Financial**: $600,000 annual revenue loss potential from operational inefficiencies
- **Customer Satisfaction**: Declining trust due to unreliable product availability promises
- **Competitive Position**: Falling behind market leaders in responsiveness and accuracy
- **Operational Efficiency**: Suboptimal resource allocation and productivity

## Stakeholder Impact
- **Sales Team**: Cannot make accurate availability commitments to customers
- **Warehouse Staff**: Overloaded with manual administrative tasks
- **Management**: Limited visibility into inventory performance and trends
- **Customers**: Experience delays and cancellations affecting satisfaction

## Cost of Inaction
- **Continued Revenue Loss**: $600,000+ annually from stockouts and overselling
- **Competitive Disadvantage**: Falling further behind digitally-native competitors  
- **Operational Inefficiency**: Ongoing waste of human resources on manual processes
- **Customer Churn Risk**: Deteriorating service levels threatening customer retention

## Success Criteria
- **Inventory Accuracy**: Reduce discrepancies from 15% to under 2%
- **Operational Efficiency**: Achieve 70%+ reduction in manual work hours
- **Real-time Visibility**: Implement instant inventory availability across all channels
- **System Integration**: Seamless connectivity with existing Salesforce CRM
- **Implementation Timeline**: Complete transformation by September 2024
- **ROI Achievement**: Break-even within 12 months of implementation

## Investment Parameters
- **Budget Allocation**: $150,000 for initial implementation phase
- **Timeline Constraint**: Must be operational before Q4 holiday season
- **Integration Requirement**: Must work seamlessly with existing Salesforce instance
- **ROI Expectation**: Positive return on investment within first year"""


def get_mock_process_overview() -> str:
    """Generate mock process overview document"""
    
    return """# Process Overview: Acme Corp Inventory Management Solution

## Solution Approach
Implement a comprehensive automated inventory management system that integrates with existing Salesforce CRM to provide real-time visibility, eliminate manual processes, and ensure accurate stock levels across all sales channels.

## Implementation Methodology

### Phase 1: Discovery & Design (4 weeks)
- **Current State Assessment**: Map existing processes and system touchpoints
- **Integration Analysis**: Evaluate Salesforce configuration and API capabilities
- **Solution Architecture**: Design optimal system configuration and data flows
- **Stakeholder Alignment**: Confirm requirements and success criteria with key users

### Phase 2: System Development (8 weeks)
- **Core Platform Setup**: Configure inventory management platform
- **Salesforce Integration**: Build real-time API connections and data synchronization
- **Workflow Automation**: Implement automated stock updates and alerts
- **User Interface Design**: Create intuitive dashboards for different user roles

### Phase 3: Testing & Training (4 weeks)
- **System Testing**: Comprehensive testing of all integrations and workflows
- **User Training**: Hands-on training for warehouse and sales teams
- **Parallel Operation**: Run new system alongside existing processes for validation
- **Performance Optimization**: Fine-tune system performance and response times

### Phase 4: Go-Live & Optimization (2 weeks)
- **Production Deployment**: Full cutover to new automated system
- **Monitoring & Support**: 24/7 monitoring during initial launch period
- **Process Refinement**: Optimize workflows based on real usage patterns
- **Success Measurement**: Track KPIs and validate achievement of success criteria

## Technology Stack

### Core Components
- **Inventory Management Platform**: Cloud-based solution with real-time processing
- **Salesforce Connector**: Native API integration for seamless data flow
- **Mobile Applications**: iOS/Android apps for warehouse floor operations
- **Analytics Dashboard**: Executive reporting and performance monitoring

### Integration Points
- **Salesforce CRM**: Bi-directional data sync for opportunities and inventory
- **Warehouse Management**: Physical inventory tracking and automated updates
- **E-commerce Platform**: Real-time availability for online ordering
- **Financial Systems**: Cost tracking and inventory valuation integration

## Success Metrics
- **Inventory Accuracy**: Target <2% discrepancy rate (current 15%)
- **Processing Efficiency**: 70%+ reduction in manual work hours
- **Customer Satisfaction**: Eliminate stockout-related order cancellations
- **Revenue Protection**: Stop $50K monthly losses from overselling
- **Response Time**: Real-time inventory queries (<2 second response)
- **ROI Achievement**: Break-even within 12 months of go-live

## Risk Mitigation
- **Data Migration**: Phased approach with validation at each step
- **User Adoption**: Comprehensive training and change management program
- **Integration Complexity**: Dedicated integration testing and fallback procedures
- **Timeline Risk**: Agile methodology with regular milestone checkpoints
- **Budget Control**: Fixed-price implementation with clear scope boundaries"""


def get_mock_process_visualization() -> str:
    """Generate mock process visualization document"""
    
    return """# Process Visualization: Acme Corp Transformation

## Current State: Manual Inventory Process

```mermaid
graph TD
    A[Customer Order] --> B[Sales Rep Check]
    B --> C[Call Warehouse]
    C --> D[Manual Count]
    D --> E[Phone/Email Update]
    E --> F[Excel Spreadsheet]
    F --> G[Sales Rep Response]
    G --> H[Customer Wait]
    
    I[Daily Update Process]
    I --> J[Print Reports]
    J --> K[Walk Warehouse]
    K --> L[Manual Count]
    L --> M[Data Entry]
    M --> N[Excel Update]
    N --> O[Error Checking]
    
    style A fill:#ffcdd2
    style H fill:#ffcdd2
    style I fill:#ffcdd2
    style O fill:#ffcdd2
```

**Current Process Issues:**
- 3-4 hours daily manual effort
- Multiple hand-offs create error opportunities
- No real-time visibility
- Customer delays and dissatisfaction

## Future State: Automated Inventory System

```mermaid
graph TD
    A[Customer Order] --> B[Real-time API Query]
    B --> C[Instant Availability Check]
    C --> D[Auto-Reserve Inventory]
    D --> E[CRM Update]
    E --> F[Customer Confirmation]
    
    G[Warehouse Receiving] --> H[Barcode Scan]
    H --> I[Auto System Update]
    I --> J[Real-time Sync]
    J --> K[All Channels Updated]
    
    L[Automated Reorder] --> M[Stock Level Monitor]
    M --> N[Trigger Reorder Point]
    N --> O[Vendor Notification]
    O --> P[Purchase Order Auto-Gen]
    
    style A fill:#c8e6c9
    style F fill:#c8e6c9
    style G fill:#c8e6c9
    style K fill:#c8e6c9
    style L fill:#c8e6c9
    style P fill:#c8e6c9
```

**Future Process Benefits:**
- Real-time inventory visibility
- Automated updates and alerts
- Zero manual data entry
- Instant customer responses

## Process Improvement Analysis

### Efficiency Gains
| Process Step | Current Time | Future Time | Improvement |
|--------------|--------------|-------------|-------------|
| Order Availability Check | 15-30 minutes | 2-3 seconds | 99% reduction |
| Daily Inventory Update | 3-4 hours | Automated | 100% elimination |
| Stock Level Reconciliation | 2 hours weekly | Real-time | 100% elimination |
| Reorder Processing | 1 hour manual | Automated | 100% elimination |
| **Total Weekly Savings** | **25+ hours** | **<1 hour** | **96% reduction** |

### Quality Improvements
- **Accuracy**: 15% error rate → <2% error rate
- **Timeliness**: Hours → seconds for availability confirmation
- **Consistency**: Manual variations → standardized automated processes
- **Visibility**: Spreadsheet-based → real-time dashboard monitoring

### Customer Experience Enhancement
- **Instant Availability**: Real-time inventory checks during sales calls
- **Reliable Promises**: Accurate delivery commitments with auto-reservation
- **Proactive Communication**: Automated notifications of delays or changes
- **Self-Service Options**: Customer portal for order and inventory status

## Implementation Impact Timeline

```mermaid
gantt
    title Implementation Timeline & Benefits
    dateFormat  YYYY-MM-DD
    section Phase 1
    Discovery & Design    :2024-03-01, 4w
    section Phase 2  
    Development          :2024-04-01, 8w
    section Phase 3
    Testing & Training   :2024-06-01, 4w
    section Phase 4
    Go-Live & Optimization :2024-07-01, 2w
    
    section Benefits Realization
    Initial Savings      :2024-07-15, 12w
    Full ROI Achievement :2024-10-15, 52w
```

**Expected Results:**
- **Week 1**: Eliminate daily manual updates (20 hours/week saved)
- **Month 1**: Achieve <5% inventory discrepancy rate
- **Month 3**: Reach full 70% manual work reduction
- **Month 6**: Achieve <2% inventory accuracy target
- **Month 12**: Full ROI realization with $1.2M annual savings"""


def get_mock_investment_proposal() -> str:
    """Generate mock investment proposal document"""
    
    return """# Investment Proposal: Acme Corp Digital Transformation

## Executive Summary
This proposal outlines a $150,000 investment in automated inventory management that will deliver $1.2M in annual savings, eliminate $600K in current revenue losses, and provide complete ROI within 12 months.

## Investment Breakdown

### Software & Platform Costs
| Component | Cost | Description |
|-----------|------|-------------|
| **Inventory Management Platform** | $45,000 | Cloud-based core system with real-time processing |
| **Salesforce Integration** | $25,000 | Native API connectors and custom workflows |
| **Mobile Applications** | $20,000 | iOS/Android apps for warehouse operations |
| **Analytics Dashboard** | $15,000 | Executive reporting and KPI monitoring |
| **Security & Compliance** | $10,000 | Data encryption and audit trail capabilities |

### Implementation Services
| Service | Cost | Timeline |
|---------|------|----------|
| **System Configuration** | $15,000 | 4 weeks |
| **Data Migration** | $8,000 | 2 weeks |
| **Integration Development** | $7,000 | 3 weeks |
| **Testing & QA** | $3,000 | 1 week |
| **Training & Documentation** | $2,000 | 1 week |

**Total Investment: $150,000**

## ROI Analysis

### Current Annual Costs (Problems)
- **Revenue Loss from Stockouts**: $300,000
- **Revenue Loss from Overselling**: $300,000  
- **Manual Labor Costs**: $85,000 (20 hours/week × $80/hour loaded cost)
- **Error Correction Costs**: $45,000
- **Customer Service Overhead**: $25,000
- **Total Annual Cost of Current State**: $755,000

### Future Annual Costs (Solution)
- **Platform Subscription**: $35,000
- **Support & Maintenance**: $15,000
- **Reduced Manual Labor**: $25,000 (96% reduction)
- **Total Annual Operating Cost**: $75,000

### Annual Savings Calculation
- **Gross Annual Savings**: $755,000 - $75,000 = $680,000
- **Net ROI**: $680,000 - $150,000 = $530,000 (Year 1)
- **Ongoing Annual Savings**: $680,000 (Years 2+)

### ROI Timeline
| Period | Investment | Savings | Cumulative ROI |
|--------|------------|---------|----------------|
| **Month 6** | $150,000 | $340,000 | $190,000 |
| **Month 12** | $150,000 | $680,000 | $530,000 |
| **Month 24** | $150,000 | $1,360,000 | $1,210,000 |
| **Month 36** | $150,000 | $2,040,000 | $1,890,000 |

**Break-even Point: 3.3 months**
**12-Month ROI: 353%**
**3-Year Total ROI: 1,260%**

## Risk Assessment & Mitigation

### Implementation Risks
- **Risk**: Integration complexity with Salesforce
  - **Probability**: Medium
  - **Mitigation**: Dedicated integration specialist and testing environment
  
- **Risk**: User adoption challenges  
  - **Probability**: Low
  - **Mitigation**: Comprehensive training program and change management
  
- **Risk**: Data migration issues
  - **Probability**: Low  
  - **Mitigation**: Phased migration with validation checkpoints

### Financial Risks
- **Risk**: Lower than expected savings
  - **Probability**: Low
  - **Mitigation**: Conservative estimates with 20% buffer built into projections
  
- **Risk**: Cost overruns
  - **Probability**: Low
  - **Mitigation**: Fixed-price contract with clear scope definition

## Success Metrics & KPIs
- **Primary**: Inventory accuracy >98% (currently 85%)
- **Efficiency**: Manual work reduction >70% (target: 96%)
- **Financial**: Revenue loss elimination ($600K annually)
- **Customer**: Zero stockout-related cancellations
- **Speed**: <2 second inventory query response time

## Next Steps & Approval Process
1. **Board Approval**: Present investment proposal to executive team
2. **Vendor Selection**: Finalize platform selection and contract terms  
3. **Project Kickoff**: Begin discovery phase within 2 weeks of approval
4. **Implementation Start**: Target go-live by September 1, 2024
5. **Success Review**: 90-day post-implementation ROI validation

**Recommended Decision Timeline**: Approval by March 15, 2024 to meet Q4 deadline"""


def get_mock_next_steps() -> str:
    """Generate mock next steps document"""
    
    return """# Next Steps: Acme Corp Implementation Roadmap

## Immediate Actions (Next 2 Weeks)

### 1. Executive Approval Process
- **Action**: Present investment proposal to board of directors
- **Owner**: Sarah Johnson (VP Operations)
- **Deadline**: March 15, 2024
- **Dependencies**: Finance team ROI validation
- **Success Criteria**: Formal project approval and budget allocation

### 2. Vendor Contract Finalization
- **Action**: Negotiate and execute software licensing agreements
- **Owner**: John Smith (CTO) + Legal team
- **Deadline**: March 22, 2024
- **Dependencies**: Board approval completion
- **Success Criteria**: Signed contracts and SOW in place

### 3. Project Team Assembly
- **Action**: Assign dedicated project team members and stakeholders
- **Owner**: Sarah Johnson (VP Operations)
- **Deadline**: March 18, 2024
- **Dependencies**: Project approval
- **Success Criteria**: Named team with defined roles and responsibilities

## Phase 1: Discovery & Design (Weeks 3-6)

### 4. Current State Documentation
- **Action**: Complete mapping of existing processes and system integrations
- **Owner**: Operations team + IT
- **Timeline**: 2 weeks
- **Deliverables**: Process maps, integration inventory, data flow diagrams

### 5. Salesforce Integration Planning  
- **Action**: Analyze current CRM configuration and plan integration approach
- **Owner**: IT team + Salesforce admin
- **Timeline**: 1 week
- **Deliverables**: Integration architecture, API specifications, data mapping

### 6. Solution Architecture Design
- **Action**: Finalize system configuration and technical architecture
- **Owner**: Implementation partner + CTO
- **Timeline**: 1 week  
- **Deliverables**: Technical architecture document, deployment plan

## Phase 2: Development & Integration (Weeks 7-14)

### 7. Platform Configuration
- **Action**: Set up core inventory management system
- **Owner**: Implementation partner
- **Timeline**: 4 weeks
- **Milestones**: Core system operational, basic workflows configured

### 8. Salesforce Integration Development
- **Action**: Build and test real-time API connections
- **Owner**: Integration team
- **Timeline**: 3 weeks
- **Milestones**: Data sync operational, workflow triggers working

## Decision Points & Approvals

### Critical Decision Point 1: Architecture Review
- **Timeline**: Week 6
- **Decision Makers**: CTO, VP Operations, Implementation Partner
- **Go/No-Go Criteria**: Architecture meets requirements, integration feasible, timeline realistic
- **Approval Required**: Technical architecture sign-off

### Critical Decision Point 2: Integration Testing
- **Timeline**: Week 12
- **Decision Makers**: IT team, Sales team, Operations team
- **Go/No-Go Criteria**: Data accuracy >95%, response time <3 seconds, no critical bugs
- **Approval Required**: User acceptance testing sign-off

### Critical Decision Point 3: Production Readiness
- **Timeline**: Week 17
- **Decision Makers**: Executive team
- **Go/No-Go Criteria**: All testing complete, training done, rollback plan ready
- **Approval Required**: Go-live authorization

## Stakeholder Involvement Matrix

| Stakeholder | Role | Involvement Level | Key Responsibilities |
|-------------|------|------------------|---------------------|
| **Sarah Johnson (VP Ops)** | Executive Sponsor | High | Decision authority, budget oversight |
| **John Smith (CTO)** | Technical Lead | High | Architecture approval, integration oversight |
| **Sales Team Lead** | Business User | Medium | Requirements validation, UAT participation |
| **Warehouse Manager** | End User | High | Process design, training, operational readiness |
| **IT Administrator** | Technical Support | Medium | System administration, ongoing support |

## Success Metrics Tracking

### Weekly Progress Reviews
- **Participants**: Project team + stakeholders
- **Format**: Status dashboard + issues escalation
- **Focus**: Timeline adherence, budget tracking, risk mitigation

### Monthly Executive Updates  
- **Participants**: Executive team + project sponsor
- **Format**: Executive summary + key metrics
- **Focus**: ROI tracking, strategic alignment, decision support

## Risk Monitoring & Escalation

### High Priority Risks to Monitor
1. **Integration Complexity**: Weekly technical reviews with escalation path
2. **User Adoption**: Proactive change management and training programs  
3. **Timeline Adherence**: Daily standups with milestone tracking
4. **Budget Control**: Weekly budget reviews with variance analysis

### Escalation Process
- **Level 1**: Project team resolution (within 24 hours)
- **Level 2**: Department head involvement (within 48 hours)
- **Level 3**: Executive team escalation (within 72 hours)
- **Level 4**: Board notification for critical issues

## Communication Plan
- **Daily**: Project team standups
- **Weekly**: Stakeholder status updates
- **Monthly**: Executive progress reviews  
- **Quarterly**: Board progress reports

**Project Success Definition**: On-time, on-budget delivery with >95% user satisfaction and measurable ROI within 6 months."""


def get_mock_sales_presentation() -> str:
    """Generate mock sales presentation document"""
    
    return """# Executive Presentation: Acme Corp Digital Transformation ROI

## The Challenge: $600K Annual Revenue Loss

### Your Current Reality
- **15% inventory discrepancy** rate causing customer dissatisfaction
- **$50,000 monthly losses** from stockouts and overselling
- **3-4 hours daily** spent on manual inventory updates
- **20 hours weekly** of valuable staff time wasted on data entry
- **Customer trust erosion** from unreliable availability promises

> *"We're losing customers because we can't tell them what we actually have in stock"* - Your Sales Team

## The Opportunity: Digital Transformation ROI

### What Success Looks Like
- **Real-time inventory visibility** across all sales channels
- **<2% inventory discrepancy** rate (from current 15%)
- **96% reduction in manual work** (from 25+ hours to <1 hour weekly)
- **Instant availability confirmation** (from 15-30 minutes to 2-3 seconds)
- **$680,000 annual savings** starting Year 1

## Our Solution: Proven Automated Inventory Management

### Core Capabilities
🎯 **Real-Time Integration**
- Seamless Salesforce CRM connectivity
- Instant inventory updates across all channels
- Mobile apps for warehouse floor operations

📊 **Intelligent Analytics** 
- Executive dashboards and KPI monitoring
- Automated reorder point management
- Predictive inventory planning

🔒 **Enterprise Security**
- Bank-level data encryption
- Complete audit trails
- Role-based access controls

### Why This Works
- **Proven Technology**: Successfully deployed at 500+ companies
- **Industry Expertise**: 15+ years in inventory management solutions
- **Salesforce Partnership**: Certified integration partner with deep CRM expertise

## ROI Projection: 353% First Year Return

### Investment Overview
- **Total Investment**: $150,000 (one-time)
- **Annual Operating Cost**: $50,000
- **Break-Even Point**: 3.3 months
- **12-Month Net ROI**: $530,000

### 3-Year Financial Impact
| Year | Investment | Savings | Net Benefit |
|------|------------|---------|-------------|
| **Year 1** | $150,000 | $680,000 | **$530,000** |
| **Year 2** | $50,000 | $680,000 | **$630,000** |
| **Year 3** | $50,000 | $680,000 | **$630,000** |
| **Total** | $250,000 | $2,040,000 | **$1,790,000** |

> *Conservative estimates with 20% buffer - actual results typically exceed projections*

## Implementation Plan: Fast Track to Success

### Timeline: 18 Weeks to Full Operation
- **Weeks 1-4**: Discovery & Design
- **Weeks 5-12**: Development & Integration  
- **Weeks 13-16**: Testing & Training
- **Weeks 17-18**: Go-Live & Optimization

### Your Team's Involvement
- **Minimal disruption** to daily operations
- **Comprehensive training** for all users
- **24/7 support** during launch period
- **Guaranteed success** with proven methodology

## Why Choose Us: Your Success is Our Mission

### Proven Track Record
- **500+ successful implementations** in similar companies
- **99.8% customer satisfaction** rating
- **Average ROI achievement**: 340% in first year
- **Industry awards** for innovation and service excellence

### Partnership Approach  
- **Fixed-price guarantee** - no cost overruns
- **Dedicated project team** assigned to your success
- **Executive sponsor** program with direct access to leadership
- **Success guarantee** - we don't succeed unless you do

### Post-Implementation Support
- **24/7 monitoring** and support
- **Quarterly business reviews** to optimize performance
- **Ongoing training** and best practice sharing
- **Technology roadmap** planning for future growth

## Customer Success Story: Similar Company Results

*"We achieved 92% reduction in manual work and eliminated all stockout-related cancellations within 4 months. The ROI exceeded expectations by 45% - this was the best technology investment we've ever made."*

**- VP Operations, Mid-Market Manufacturing Company**

**Their Results:**
- 94% reduction in inventory discrepancies
- $850K annual savings (vs $680K projected)  
- 4.2-month payback period
- Zero stockout incidents post-implementation

## Next Steps: Fast Track Your Success

### Immediate Action Plan
1. **Executive Approval** (this week)
2. **Contract Execution** (next week)
3. **Project Kickoff** (within 2 weeks)
4. **Go-Live Target**: September 1, 2024

### Investment Decision Support
- **Pilot Program Available**: 90-day trial with limited scope
- **ROI Guarantee**: Full refund if projected savings not achieved within 12 months
- **Reference Visits**: Meet with similar customers to validate results
- **Board Presentation**: We'll present to your board if needed

## The Bottom Line: Transform Your Business Now

### The Cost of Delay
- **Every month of delay** = $50K continued losses
- **6-month delay** = $300K in preventable losses  
- **Q4 holiday season risk** without real-time inventory

### The Value of Action
- **$680K annual savings** starting within 6 months
- **Competitive advantage** through superior customer service
- **Operational excellence** with automated, accurate processes
- **Future-ready platform** for continued growth and expansion

---

## Ready to Move Forward?

**Next Meeting**: Technical deep-dive with your IT team
**Timeline**: Project kickoff within 2 weeks of approval
**Contact**: Implementation specialist standing by

*Let's transform your inventory management and capture that $680K in annual savings starting this year.*

---

**Contact Information**
- Project Lead: [Implementation Specialist]
- Email: success@yoursolution.com
- Phone: [Direct line]
- Emergency: 24/7 support hotline"""


def load_mock_documents_to_session():
    """Load mock documents into session state for demonstration"""
    
    st.session_state.generated_documents = generate_mock_documents()
    st.session_state.pipeline_state = "completed"
    st.session_state.processing_progress = 100
    st.session_state.current_agent = "Completed"
    st.session_state.total_processing_time = "6 minutes 23 seconds"