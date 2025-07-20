import { useState, useEffect, useCallback } from 'react';
import type { Message, WebSocketEvent } from '../../types';
import { websocketService } from '../../services/websocket';
import type { WebSocketConnectionStatus } from '../../services/websocket';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import ConnectionStatus from './ConnectionStatus';

interface ChatInterfaceProps {
  conversationId: string;
}

export default function ChatInterface({ conversationId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [connectionStatus, setConnectionStatus] = useState<WebSocketConnectionStatus>('disconnected');
  const [isStreaming, setIsStreaming] = useState(false);

  const handleWebSocketMessage = useCallback((event: WebSocketEvent) => {
    switch (event.type) {
      case 'message':
        const newMessage: Message = {
          id: crypto.randomUUID(),
          content: event.data.content,
          type: event.data.type || 'agent',
          agentName: event.data.agentName,
          timestamp: new Date(event.timestamp),
          metadata: event.data.metadata,
        };
        setMessages(prev => [...prev, newMessage]);
        break;
        
      case 'agent_status':
        if (event.data.status === 'working' || event.data.status === 'thinking') {
          setIsStreaming(true);
        } else if (event.data.status === 'completed' || event.data.status === 'idle') {
          setIsStreaming(false);
        }
        break;
        
      case 'error':
        const errorMessage: Message = {
          id: crypto.randomUUID(),
          content: `Error: ${event.data.message || 'Unknown error occurred'}`,
          type: 'system',
          timestamp: new Date(event.timestamp),
        };
        setMessages(prev => [...prev, errorMessage]);
        setIsStreaming(false);
        break;
    }
  }, []);

  const handleStatusChange = useCallback((status: WebSocketConnectionStatus) => {
    setConnectionStatus(status);
  }, []);

  const handleSendMessage = useCallback((content: string) => {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content,
      type: 'user',
      timestamp: new Date(),
    };
    
    setMessages(prev => [...prev, userMessage]);
    websocketService.sendMessage(content);
    setIsStreaming(true);
  }, []);

  useEffect(() => {
    websocketService.onMessage(handleWebSocketMessage);
    websocketService.onStatusChange(handleStatusChange);
    websocketService.connect(conversationId);

    return () => {
      websocketService.disconnect();
    };
  }, [conversationId, handleWebSocketMessage, handleStatusChange]);

  return (
    <div className="flex flex-col h-full bg-white">
      <div className="border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold text-gray-900">
            Presales AI Assistant
          </h1>
          <ConnectionStatus status={connectionStatus} />
        </div>
      </div>
      
      <MessageList 
        messages={messages} 
        isStreaming={isStreaming} 
      />
      
      <MessageInput 
        onSendMessage={handleSendMessage}
        disabled={connectionStatus !== 'connected'}
        placeholder={
          connectionStatus !== 'connected' 
            ? 'Connecting...' 
            : 'Ask me about prospects, research, or proposals...'
        }
      />
    </div>
  );
}