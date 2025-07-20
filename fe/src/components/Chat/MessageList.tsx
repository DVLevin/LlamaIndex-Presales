import { useEffect, useRef } from 'react';
import type { Message as MessageType } from '../../types';
import Message from './Message';

interface MessageListProps {
  messages: MessageType[];
  isStreaming?: boolean;
}

export default function MessageList({ messages, isStreaming = false }: MessageListProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        <div className="text-center">
          <p className="text-lg font-medium">Start a conversation</p>
          <p className="text-sm">Send a message to begin working with the AI agents</p>
        </div>
      </div>
    );
  }

  return (
    <div 
      ref={scrollRef}
      className="flex-1 overflow-y-auto p-4 space-y-4"
    >
      {messages.map((message) => (
        <Message key={message.id} message={message} />
      ))}
      
      {isStreaming && (
        <div className="flex items-center gap-2 p-4 text-gray-500">
          <div className="flex space-x-1">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
          </div>
          <span className="text-sm">Agent is working...</span>
        </div>
      )}
    </div>
  );
}