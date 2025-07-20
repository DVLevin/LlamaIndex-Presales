import type { Agent, AgentStatus as AgentStatusType } from '../../types';
import { Bot, CheckCircle, Clock, AlertCircle, Loader2, Pause } from 'lucide-react';
import clsx from 'clsx';

interface AgentStatusProps {
  agent: Agent;
}

export default function AgentStatus({ agent }: AgentStatusProps) {
  const getStatusDisplay = (status: AgentStatusType) => {
    switch (status) {
      case 'idle':
        return {
          icon: <Bot className="w-4 h-4" />,
          text: 'Idle',
          color: 'text-gray-600',
          bgColor: 'bg-gray-100',
        };
      case 'thinking':
        return {
          icon: <Clock className="w-4 h-4" />,
          text: 'Thinking',
          color: 'text-blue-600',
          bgColor: 'bg-blue-100',
        };
      case 'working':
        return {
          icon: <Loader2 className="w-4 h-4 animate-spin" />,
          text: 'Working',
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
        };
      case 'waiting':
        return {
          icon: <Pause className="w-4 h-4" />,
          text: 'Waiting',
          color: 'text-purple-600',
          bgColor: 'bg-purple-100',
        };
      case 'completed':
        return {
          icon: <CheckCircle className="w-4 h-4" />,
          text: 'Completed',
          color: 'text-green-600',
          bgColor: 'bg-green-100',
        };
      case 'error':
        return {
          icon: <AlertCircle className="w-4 h-4" />,
          text: 'Error',
          color: 'text-red-600',
          bgColor: 'bg-red-100',
        };
    }
  };

  const statusDisplay = getStatusDisplay(agent.status);

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="font-medium text-gray-900 mb-1">{agent.name}</h3>
          <p className="text-sm text-gray-600 mb-3">{agent.description}</p>
          
          {agent.currentTask && (
            <div className="mb-3">
              <p className="text-xs font-medium text-gray-500 mb-1">Current Task:</p>
              <p className="text-sm text-gray-700">{agent.currentTask}</p>
            </div>
          )}
        </div>
        
        <div className={clsx(
          'flex items-center gap-2 px-2 py-1 rounded-full text-xs font-medium',
          statusDisplay.color,
          statusDisplay.bgColor
        )}>
          {statusDisplay.icon}
          <span>{statusDisplay.text}</span>
        </div>
      </div>
    </div>
  );
}