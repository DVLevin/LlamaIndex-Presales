import type { Agent } from '../../types';
import AgentStatus from './AgentStatus';

interface AgentDashboardProps {
  agents: Agent[];
}

export default function AgentDashboard({ agents }: AgentDashboardProps) {
  if (agents.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-8">
        <div className="text-center text-gray-500">
          <p className="font-medium">No agents active</p>
          <p className="text-sm">Start a conversation to see agent activity</p>
        </div>
      </div>
    );
  }

  const activeAgents = agents.filter(agent => agent.status !== 'idle');
  const idleAgents = agents.filter(agent => agent.status === 'idle');

  return (
    <div className="space-y-6">
      {activeAgents.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Active Agents</h2>
          <div className="space-y-3">
            {activeAgents.map((agent) => (
              <AgentStatus key={agent.id} agent={agent} />
            ))}
          </div>
        </div>
      )}
      
      {idleAgents.length > 0 && (
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Available Agents</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            {idleAgents.map((agent) => (
              <AgentStatus key={agent.id} agent={agent} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}