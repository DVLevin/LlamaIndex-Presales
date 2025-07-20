import type { Message as MessageType } from '../../types';
import { User, Bot, AlertCircle } from 'lucide-react';
import clsx from 'clsx';

interface MessageProps {
  message: MessageType;
}

export default function Message({ message }: MessageProps) {
  const isUser = message.type === 'user';
  const isSystem = message.type === 'system';
  
  const getIcon = () => {
    if (isUser) return <User className="w-4 h-4" />;
    if (isSystem) return <AlertCircle className="w-4 h-4" />;
    return <Bot className="w-4 h-4" />;
  };

  const getMessageLabel = () => {
    if (isUser) return 'You';
    if (isSystem) return 'System';
    return message.agentName || 'Agent';
  };

  return (
    <div className={clsx(
      'flex gap-3 p-4 rounded-lg',
      {
        'bg-blue-50 border border-blue-200': isUser,
        'bg-gray-50 border border-gray-200': !isUser && !isSystem,
        'bg-yellow-50 border border-yellow-200': isSystem,
      }
    )}>
      <div className={clsx(
        'flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center',
        {
          'bg-blue-500 text-white': isUser,
          'bg-gray-500 text-white': !isUser && !isSystem,
          'bg-yellow-500 text-white': isSystem,
        }
      )}>
        {getIcon()}
      </div>
      
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1">
          <span className="font-medium text-sm text-gray-900">
            {getMessageLabel()}
          </span>
          <span className="text-xs text-gray-500">
            {message.timestamp.toLocaleTimeString()}
          </span>
        </div>
        
        <div className="text-gray-800 whitespace-pre-wrap break-words">
          {message.content}
        </div>
        
        {message.metadata && Object.keys(message.metadata).length > 0 && (
          <details className="mt-2">
            <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-700">
              Metadata
            </summary>
            <pre className="mt-1 text-xs text-gray-600 bg-gray-100 p-2 rounded overflow-auto">
              {JSON.stringify(message.metadata, null, 2)}
            </pre>
          </details>
        )}
      </div>
    </div>
  );
}