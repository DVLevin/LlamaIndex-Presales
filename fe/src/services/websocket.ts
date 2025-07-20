import type { WebSocketEvent } from '../types';

export type WebSocketConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error';

export interface WebSocketService {
  connect: (conversationId: string) => void;
  disconnect: () => void;
  sendMessage: (message: string) => void;
  getConnectionStatus: () => WebSocketConnectionStatus;
  onMessage: (callback: (event: WebSocketEvent) => void) => void;
  onStatusChange: (callback: (status: WebSocketConnectionStatus) => void) => void;
}

class WebSocketServiceImpl implements WebSocketService {
  private ws: WebSocket | null = null;
  private connectionStatus: WebSocketConnectionStatus = 'disconnected';
  private messageCallbacks: ((event: WebSocketEvent) => void)[] = [];
  private statusCallbacks: ((status: WebSocketConnectionStatus) => void)[] = [];
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  private conversationId: string | null = null;

  connect(conversationId: string): void {
    this.conversationId = conversationId;
    this.setConnectionStatus('connecting');
    
    const wsUrl = `ws://localhost:8000/ws/${conversationId}`;
    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      this.setConnectionStatus('connected');
      this.reconnectAttempts = 0;
      console.log('WebSocket connected');
    };

    this.ws.onmessage = (event) => {
      try {
        const data: WebSocketEvent = JSON.parse(event.data);
        this.messageCallbacks.forEach(callback => callback(data));
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    this.ws.onclose = (event) => {
      this.setConnectionStatus('disconnected');
      console.log('WebSocket disconnected:', event.code, event.reason);
      
      if (!event.wasClean && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.scheduleReconnect();
      }
    };

    this.ws.onerror = (error) => {
      this.setConnectionStatus('error');
      console.error('WebSocket error:', error);
    };
  }

  disconnect(): void {
    if (this.ws) {
      this.ws.close(1000, 'Client disconnect');
      this.ws = null;
    }
    this.setConnectionStatus('disconnected');
    this.conversationId = null;
  }

  sendMessage(message: string): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      const payload = {
        type: 'user_message',
        data: { content: message },
        conversationId: this.conversationId,
        timestamp: new Date(),
      };
      this.ws.send(JSON.stringify(payload));
    } else {
      console.warn('Cannot send message: WebSocket not connected');
    }
  }

  getConnectionStatus(): WebSocketConnectionStatus {
    return this.connectionStatus;
  }

  onMessage(callback: (event: WebSocketEvent) => void): void {
    this.messageCallbacks.push(callback);
  }

  onStatusChange(callback: (status: WebSocketConnectionStatus) => void): void {
    this.statusCallbacks.push(callback);
  }

  private setConnectionStatus(status: WebSocketConnectionStatus): void {
    this.connectionStatus = status;
    this.statusCallbacks.forEach(callback => callback(status));
  }

  private scheduleReconnect(): void {
    this.reconnectAttempts++;
    const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
    
    console.log(`Attempting to reconnect in ${delay}ms (attempt ${this.reconnectAttempts})`);
    
    setTimeout(() => {
      if (this.conversationId) {
        this.connect(this.conversationId);
      }
    }, delay);
  }
}

export const websocketService = new WebSocketServiceImpl();