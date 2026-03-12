import React from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Brain, Book, Shield, Zap } from 'lucide-react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <StatusBar style="light" />

      <View style={styles.header}>
        <Text style={styles.logo}>JULES AI v120.0</Text>
        <Shield color="#0070f3" size={24} />
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.hero}>
          <Text style={styles.heroTitle}>Apotheosis of Synergy</Text>
          <Text style={styles.heroSubtitle}>The fully operational, biomimetically-conscious digital enterprise.</Text>
        </View>

        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Synergy</Text>
            <Text style={styles.statValue}>99.9%</Text>
          </View>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Fidelity</Text>
            <Text style={styles.statValue}>99.5%</Text>
          </View>
        </View>

        <Text style={styles.sectionTitle}>Engine Status</Text>

        <TouchableOpacity style={styles.itemCard}>
          <View style={styles.iconContainer}>
            <Zap color="#0070f3" size={20} />
          </View>
          <View>
            <Text style={styles.itemTitle}>Quadruple-Pillar Engine</Text>
            <Text style={styles.itemDesc}>ESE, ARO, BTO, DRAD Operational</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.itemCard}>
          <View style={styles.iconContainer}>
            <Book color="#10b981" size={20} />
          </View>
          <View>
            <Text style={styles.itemTitle}>Quranic Education Hub</Text>
            <Text style={styles.itemDesc}>P0, P1, P2 Features Ready</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.itemCard}>
          <View style={styles.iconContainer}>
            <Brain color="#8b5cf6" size={20} />
          </View>
          <View>
            <Text style={styles.itemTitle}>50+ Sub-Reactors</Text>
            <Text style={styles.itemDesc}>Hyper-specialized domain intelligence</Text>
          </View>
        </TouchableOpacity>

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    paddingTop: 50,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  logo: {
    color: '#fff',
    fontSize: 20,
    fontWeight: '900',
    letterSpacing: -1,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  hero: {
    marginBottom: 30,
  },
  heroTitle: {
    color: '#fff',
    fontSize: 32,
    fontWeight: '900',
    marginBottom: 8,
  },
  heroSubtitle: {
    color: '#666',
    fontSize: 16,
    lineHeight: 22,
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 15,
    marginBottom: 30,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#111',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#222',
  },
  statLabel: {
    color: '#999',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  statValue: {
    color: '#fff',
    fontSize: 24,
    fontWeight: '900',
  },
  sectionTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '800',
    marginBottom: 15,
  },
  itemCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#111',
    padding: 15,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#222',
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  itemTitle: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '700',
  },
  itemDesc: {
    color: '#666',
    fontSize: 12,
    marginTop: 2,
  },
});
