export interface Message {
  id: string;
  content: string;
  type: 'user' | 'agent' | 'system';
  agentName?: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface Agent {
  id: string;
  name: string;
  description: string;
  status: AgentStatus;
  currentTask?: string;
}

export type AgentStatus = 'idle' | 'thinking' | 'working' | 'waiting' | 'completed' | 'error';

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  agents: Agent[];
  status: 'active' | 'paused' | 'completed';
  createdAt: Date;
  updatedAt: Date;
}

export interface WebSocketEvent {
  type: 'message' | 'agent_status' | 'tool_call' | 'error' | 'handoff';
  data: any;
  conversationId: string;
  timestamp: Date;
}

export interface ToolCall {
  id: string;
  name: string;
  parameters: Record<string, any>;
  status: 'pending' | 'running' | 'completed' | 'error';
  result?: any;
  agentId: string;
}

export interface AgentHandoff {
  fromAgent: string;
  toAgent: string;
  reason: string;
  context: Record<string, any>;
}