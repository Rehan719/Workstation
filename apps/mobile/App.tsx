import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, TextInput, Dimensions } from 'react-native';
import { Bot, LayoutDashboard, Package, User, Send, Zap, Cpu, TrendingUp, Brain, Globe, History, Sparkles } from 'lucide-react-native';

const { width } = Dimensions.get('window');

const DashboardScreen = ({ mode }) => (
  <ScrollView contentContainerStyle={styles.scrollContent}>
    <View style={styles.header}>
      <Text style={styles.title}>WORKSTATION</Text>
      <Text style={styles.subtitle}>{mode.toUpperCase()} MISSION ACTIVE</Text>
    </View>

    <View style={styles.statsGrid}>
      <StatCard label="Fidelity" value="99.9%" icon={Zap} color="#38bdf8" />
      <StatCard label="Resonance" value="0.98" icon={Brain} color="#10b981" />
    </View>

    {mode === 'strategic' && (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Ecosystem Vitals</Text>
        <View style={styles.resonanceRow}>
           <ResonanceItem label="WST" value="52.4K" color="#fbbf24" />
           <ResonanceItem label="SWARM" value="42" color="#38bdf8" />
        </View>
      </View>
    )}

    {mode === 'research' && (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Global Signals</Text>
        <View style={styles.signalCard}>
           <Text style={styles.signalText}>arXiv: Multi-Agentic Systems...</Text>
           <Text style={styles.signalSub}>Relevance: 98%</Text>
        </View>
      </View>
    )}
  </ScrollView>
);

const StatCard = ({ label, value, icon: Icon, color }) => (
  <View style={styles.statCard}>
    <View style={[styles.statIcon, { backgroundColor: color + '20' }]}>
      <Icon size={20} color={color} />
    </View>
    <Text style={styles.statValue}>{value}</Text>
    <Text style={styles.statLabel}>{label}</Text>
  </View>
);

const ResonanceItem = ({ label, value, color }) => (
  <View style={styles.resItem}>
    <Text style={styles.resLabel}>{label}</Text>
    <Text style={[styles.resValue, { color }]}>{value}</Text>
  </View>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [mode, setMode] = useState('strategic');

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <DashboardScreen mode={mode} />

      <View style={styles.navBar}>
        <TouchableOpacity onPress={() => setMode(mode === 'strategic' ? 'research' : 'strategic')} style={styles.navItem}>
          <Sparkles size={24} color="#fbbf24" />
          <Text style={styles.navText}>Switch Mode</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('dashboard')} style={styles.navItem}>
          <LayoutDashboard size={24} color={activeTab === 'dashboard' ? '#38bdf8' : '#64748b'} />
          <Text style={styles.navText}>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Globe size={24} color="#64748b" />
          <Text style={styles.navText}>World</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#020617' },
  scrollContent: { padding: 24, paddingTop: 40, paddingBottom: 100 },
  header: { marginBottom: 32 },
  title: { color: '#38bdf8', fontSize: 28, fontWeight: '900', letterSpacing: 2 },
  subtitle: { color: '#64748b', fontSize: 14, fontWeight: '700' },
  statsGrid: { flexDirection: 'row', justifyContent: 'space-between' },
  statCard: { width: (width - 64) / 2, backgroundColor: '#0f172a', padding: 20, borderRadius: 24, borderWidth: 1, borderColor: '#1e293b' },
  statIcon: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  statValue: { color: 'white', fontSize: 20, fontWeight: '800' },
  statLabel: { color: '#64748b', fontSize: 10, fontWeight: '700', textTransform: 'uppercase' },
  section: { marginTop: 32 },
  sectionTitle: { color: 'white', fontSize: 18, fontWeight: '800', marginBottom: 16 },
  resonanceRow: { flexDirection: 'row', justifyContent: 'space-around', backgroundColor: '#0f172a', padding: 24, borderRadius: 24, borderWidth: 1, borderColor: '#1e293b' },
  resItem: { alignItems: 'center' },
  resLabel: { color: '#64748b', fontSize: 10, fontWeight: '700', marginBottom: 4 },
  resValue: { fontSize: 20, fontWeight: '900' },
  signalCard: { backgroundColor: '#1e293b', padding: 20, borderRadius: 20 },
  signalText: { color: 'white', fontWeight: 'bold' },
  signalSub: { color: '#38bdf8', fontSize: 10, marginTop: 4 },
  navBar: { position: 'absolute', bottom: 0, width: '100%', height: 90, backgroundColor: '#020617', flexDirection: 'row', borderTopWidth: 1, borderTopColor: '#1e293b', paddingBottom: 20 },
  navItem: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  navText: { color: '#64748b', fontSize: 10, marginTop: 4, fontWeight: '700' }
});
