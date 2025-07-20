import { useState } from 'react';
import ChatInterface from './components/Chat/ChatInterface';
import AgentDashboard from './components/Dashboard/AgentDashboard';
import type { Agent } from './types';
import { MessageSquare, Users } from 'lucide-react';
import clsx from 'clsx';

function App() {
  const [activeTab, setActiveTab] = useState<'chat' | 'agents'>('chat');
  const conversationId = 'demo-conversation'; // In a real app, this would be dynamic

  // Mock agents data - in real app this would come from WebSocket
  const mockAgents: Agent[] = [
    {
      id: 'research-agent',
      name: 'Research Agent',
      description: 'Conducts prospect research and market intelligence',
      status: 'idle',
    },
    {
      id: 'qualification-agent', 
      name: 'Qualification Agent',
      description: 'Evaluates lead quality and scoring',
      status: 'idle',
    },
    {
      id: 'proposal-agent',
      name: 'Proposal Agent', 
      description: 'Generates customized proposals and presentations',
      status: 'idle',
    },
    {
      id: 'review-agent',
      name: 'Review Agent',
      description: 'Quality assurance and compliance checking',
      status: 'idle',
    },
  ];

  return (
    <div className="h-screen bg-gray-50 flex flex-col">
      {/* Tab Navigation */}
      <div className="bg-white border-b border-gray-200">
        <nav className="flex space-x-8 px-6 py-3">
          <button
            onClick={() => setActiveTab('chat')}
            className={clsx(
              'flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md',
              activeTab === 'chat'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            )}
          >
            <MessageSquare className="w-4 h-4" />
            Chat
          </button>
          <button
            onClick={() => setActiveTab('agents')}
            className={clsx(
              'flex items-center gap-2 px-3 py-2 text-sm font-medium rounded-md',
              activeTab === 'agents'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-500 hover:text-gray-700'
            )}
          >
            <Users className="w-4 h-4" />
            Agents
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === 'chat' ? (
          <ChatInterface conversationId={conversationId} />
        ) : (
          <div className="h-full p-6 overflow-y-auto">
            <AgentDashboard agents={mockAgents} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
