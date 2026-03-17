import React from 'react';
import { Bot, User } from 'lucide-react-native';

export const MessageItem = ({ message }: { message: any }) => {
  const isBot = message.role === 'assistant';

  return (
    <div style={{
      flexDirection: isBot ? 'row' : 'row-reverse',
      marginBottom: 20,
      gap: 12,
      alignItems: 'flex-start'
    }}>
      <div style={{
        width: 36,
        height: 36,
        borderRadius: 12,
        backgroundColor: isBot ? '#38bdf820' : '#fbbf2420',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        {isBot ? <Bot size={20} color="#38bdf8" /> : <User size={20} color="#fbbf24" />}
      </div>
      <div style={{
        padding: 16,
        borderRadius: 20,
        backgroundColor: isBot ? '#1e293b' : '#0f172a',
        borderWidth: 1,
        borderColor: isBot ? '#38bdf820' : '#fbbf2420',
        maxWidth: '80%'
      }}>
        <p style={{ color: 'white', fontSize: 14, lineHeight: 20 }}>{message.content}</p>
      </div>
    </div>
  );
};
