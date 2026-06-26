import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import LessonCard from './components/LessonCard';
import ProgressRing from './components/ProgressRing';

const App = () => {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.greeting}>As-Salamu Alaykum!</Text>
        <Text style={styles.subGreeting}>Continue your Quranic journey.</Text>
      </View>

      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.progressContainer}>
          <ProgressRing label="Hifz" value={1} total={30} color="#FBBF24" />
          <ProgressRing label="Tajweed" value={85} total={100} color="#10B981" />
        </View>

        <Text style={styles.sectionTitle}>CURRENT LESSONS</Text>
        <LessonCard
          title="Al-Fatihah"
          level={1}
          status="Completed"
        />
        <LessonCard
          title="Intro to Tajweed"
          level={1}
          status="In Progress"
        />
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0F172A',
    paddingTop: 60,
  },
  header: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  greeting: {
    color: '#FFFFFF',
    fontSize: 28,
    fontWeight: '900',
  },
  subGreeting: {
    color: '#64748B',
    fontSize: 12,
    fontWeight: '700',
    marginTop: 5,
  },
  scrollContent: {
    paddingHorizontal: 20,
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 40,
  },
  sectionTitle: {
    color: '#64748B',
    fontSize: 10,
    fontWeight: '900',
    letterSpacing: 2,
    marginBottom: 20,
  }
});

export default App;
