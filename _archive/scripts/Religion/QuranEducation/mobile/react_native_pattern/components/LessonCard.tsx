import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const LessonCard = ({ title, level, status }) => {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      <Text style={styles.info}>Level {level} • {status}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#1E293B',
    padding: 20,
    borderRadius: 12,
    marginBottom: 15,
  },
  title: {
    color: '#FFFFFF',
    fontWeight: 'bold',
  },
  info: {
    color: '#94A3B8',
    fontSize: 10,
    marginTop: 5,
  }
});

export default LessonCard;
