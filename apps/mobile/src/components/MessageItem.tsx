import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Bot, User } from 'lucide-react-native';

export const MessageItem = ({ message }: { message: any }) => {
  const isBot = message.role === 'assistant';

  return (
    <View style={[styles.container, isBot ? styles.botContainer : styles.userContainer]}>
      <View style={[styles.iconBox, isBot ? styles.botIconBox : styles.userIconBox]}>
        {isBot ? <Bot size={20} color="#38bdf8" /> : <User size={20} color="#fbbf24" />}
      </View>
      <View style={[styles.bubble, isBot ? styles.botBubble : styles.userBubble]}>
        <Text style={styles.text}>{message.content}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    marginBottom: 20,
    gap: 12,
    alignItems: 'flex-start'
  },
  botContainer: {
    flexDirection: 'row',
  },
  userContainer: {
    flexDirection: 'row-reverse',
  },
  iconBox: {
    width: 36,
    height: 36,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center'
  },
  botIconBox: {
    backgroundColor: 'rgba(56, 189, 248, 0.12)'
  },
  userIconBox: {
    backgroundColor: 'rgba(251, 191, 36, 0.12)'
  },
  bubble: {
    padding: 16,
    borderRadius: 20,
    borderWidth: 1,
    maxWidth: '80%'
  },
  botBubble: {
    backgroundColor: '#1e293b',
    borderColor: 'rgba(56, 189, 248, 0.12)'
  },
  userBubble: {
    backgroundColor: '#0f172a',
    borderColor: 'rgba(251, 191, 36, 0.12)'
  },
  text: {
    color: 'white',
    fontSize: 14,
    lineHeight: 20
  }
});
