# Database (DB) - Task Brief

## Overview
The database layer provides persistent storage and state management for the multi-agent presales system, ensuring data consistency, conversation history, and analytics capabilities.

## Core Responsibilities

### 1. Agent State Management
- **Conversation state**: Maintain context across agent handoffs
- **Workflow progress**: Track agent execution status and results
- **State persistence**: Survive system restarts and failures
- **State recovery**: Resume interrupted agent workflows

### 2. Data Models

#### Conversation Management
```sql
-- Core conversation tracking
conversations (
    id UUID PRIMARY KEY,
    prospect_name VARCHAR,
    company_name VARCHAR,
    status ENUM('active', 'qualified', 'proposal', 'closed'),
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    metadata JSONB
)

-- Message history
messages (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    agent_name VARCHAR,
    message_type ENUM('user', 'agent', 'tool_call', 'tool_result'),
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMP
)
```

#### Agent Workflow Tracking
```sql
-- Agent execution logs
agent_executions (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    agent_name VARCHAR,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    status ENUM('running', 'completed', 'failed', 'handoff'),
    input_data JSONB,
    output_data JSONB,
    error_details TEXT
)

-- Tool usage tracking
tool_calls (
    id UUID PRIMARY KEY,
    agent_execution_id UUID REFERENCES agent_executions(id),
    tool_name VARCHAR,
    parameters JSONB,
    result JSONB,
    execution_time_ms INTEGER,
    status ENUM('success', 'error'),
    created_at TIMESTAMP
)
```

### 3. Prospect and Company Data
```sql
-- Prospect information
prospects (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR,
    phone VARCHAR,
    title VARCHAR,
    company_id UUID REFERENCES companies(id),
    qualification_score INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)

-- Company information
companies (
    id UUID PRIMARY KEY,
    name VARCHAR NOT NULL,
    industry VARCHAR,
    size_category VARCHAR,
    website VARCHAR,
    research_data JSONB,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
```

### 4. Analytics and Reporting
```sql
-- Performance metrics
agent_metrics (
    id UUID PRIMARY KEY,
    agent_name VARCHAR,
    date DATE,
    total_executions INTEGER,
    successful_executions INTEGER,
    average_execution_time_ms INTEGER,
    total_tool_calls INTEGER,
    success_rate DECIMAL(5,2)
)

-- Business outcomes
conversation_outcomes (
    id UUID PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    outcome ENUM('qualified', 'not_qualified', 'proposal_sent', 'deal_closed'),
    value_estimate DECIMAL(10,2),
    outcome_date TIMESTAMP,
    notes TEXT
)
```

## Technical Implementation

### Database Technology Options
1. **PostgreSQL** (Recommended)
   - Excellent JSONB support for flexible agent state
   - Strong consistency guarantees
   - Rich indexing capabilities
   - Time-series data support

2. **Alternative: MongoDB**
   - Native JSON document storage
   - Flexible schema evolution
   - Good for rapid prototyping

### Key Features

#### State Serialization
```python
# Agent state management
class ConversationState:
    def save_state(self, conversation_id: UUID, state: dict):
        # Serialize and store agent state
        pass
    
    def load_state(self, conversation_id: UUID) -> dict:
        # Deserialize and return agent state
        pass
    
    def update_state(self, conversation_id: UUID, updates: dict):
        # Merge updates with existing state
        pass
```

#### Migration Strategy
- Version-controlled database migrations
- Backward compatibility for state schemas
- Data migration scripts for schema changes

#### Indexing Strategy
```sql
-- Performance indexes
CREATE INDEX idx_conversations_status ON conversations(status, updated_at);
CREATE INDEX idx_messages_conversation_time ON messages(conversation_id, created_at);
CREATE INDEX idx_agent_executions_status ON agent_executions(status, start_time);
CREATE INDEX idx_prospects_qualification ON prospects(qualification_score, created_at);

-- JSONB indexes for metadata searches
CREATE INDEX idx_conversations_metadata ON conversations USING GIN(metadata);
CREATE INDEX idx_agent_execution_output ON agent_executions USING GIN(output_data);
```

## Data Access Patterns

### 1. Real-time Queries
- Current conversation state
- Active agent executions
- Live streaming data

### 2. Historical Analysis
- Agent performance over time
- Conversation success patterns
- Tool usage analytics

### 3. Reporting Queries
- Qualification success rates
- Time-to-proposal metrics
- Agent efficiency comparisons

## Success Criteria
1. **Performance**: Sub-50ms query response times for state operations
2. **Scalability**: Handle 10,000+ concurrent conversations
3. **Reliability**: 99.99% uptime with automatic failover
4. **Data Integrity**: Zero data loss with ACID compliance

## Integration Points
- Backend API for state management
- AI agents for context retrieval
- Frontend for historical data display
- Analytics systems for reporting

## Security and Compliance
- Data encryption at rest and in transit
- PII protection and anonymization
- Audit trails for compliance
- Backup and disaster recovery

## Monitoring and Maintenance
- Database performance monitoring
- Query optimization and analysis
- Automated backup verification
- Storage capacity planning

## Next Steps
1. Design detailed database schema
2. Set up PostgreSQL with appropriate extensions
3. Implement data access layer (ORM/SQL)
4. Create migration system
5. Add monitoring and alerting
6. Implement backup and recovery procedures
7. Performance testing and optimization