import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const ProgressRing = ({ label, value, total, color }) => {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>{label}</Text>
      <View style={[styles.ring, { borderColor: color }]}>
        <Text style={styles.value}>{value}/{total}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    flex: 1,
  },
  label: {
    color: '#64748B',
    fontSize: 10,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  ring: {
    width: 100,
    height: 100,
    borderRadius: 50,
    borderWidth: 4,
    alignItems: 'center',
    justifyContent: 'center',
  },
  value: {
    color: '#FFFFFF',
    fontWeight: 'bold',
  }
});

export default ProgressRing;
