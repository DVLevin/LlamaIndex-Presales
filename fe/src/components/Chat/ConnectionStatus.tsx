import type { WebSocketConnectionStatus } from '../../services/websocket';
import { Wifi, WifiOff, AlertCircle, Loader2 } from 'lucide-react';
import clsx from 'clsx';

interface ConnectionStatusProps {
  status: WebSocketConnectionStatus;
}

export default function ConnectionStatus({ status }: ConnectionStatusProps) {
  const getStatusDisplay = () => {
    switch (status) {
      case 'connected':
        return {
          icon: <Wifi className="w-4 h-4" />,
          text: 'Connected',
          color: 'text-green-600',
          bgColor: 'bg-green-100',
        };
      case 'connecting':
        return {
          icon: <Loader2 className="w-4 h-4 animate-spin" />,
          text: 'Connecting...',
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
        };
      case 'disconnected':
        return {
          icon: <WifiOff className="w-4 h-4" />,
          text: 'Disconnected',
          color: 'text-gray-600',
          bgColor: 'bg-gray-100',
        };
      case 'error':
        return {
          icon: <AlertCircle className="w-4 h-4" />,
          text: 'Connection Error',
          color: 'text-red-600',
          bgColor: 'bg-red-100',
        };
      default:
        return {
          icon: <WifiOff className="w-4 h-4" />,
          text: 'Unknown',
          color: 'text-gray-600',
          bgColor: 'bg-gray-100',
        };
    }
  };

  const statusDisplay = getStatusDisplay();

  return (
    <div className={clsx(
      'flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium',
      statusDisplay.color,
      statusDisplay.bgColor
    )}>
      {statusDisplay.icon}
      <span>{statusDisplay.text}</span>
    </div>
  );
}