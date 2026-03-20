import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, Dimensions, TextInput, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { LayoutDashboard, Zap, Brain, Globe, Sparkles, Send, Bot, User, MessageSquare, Settings, Shield, ShoppingBag, Cpu, Book, FlaskConical, Scale, Briefcase, GraduationCap, Star, Award, Plus, Wifi, Landmark, TrendingUp, Target, Activity, Radio, GitBranch, Fingerprint, Terminal, Layers } from 'lucide-react-native';

const { width, height } = Dimensions.get('window');

const DashboardScreen = ({ stats }) => (
  <ScrollView contentContainerStyle={styles.scrollContent}>
    <View style={styles.header}>
      <Text style={styles.title}>WORKSTATION</Text>
      <Text style={styles.subtitle}>GENESIS v200.0 • LAYER STATUS: 7/7 ACTIVE</Text>
    </View>

    <View style={styles.statsGrid}>
      <View style={[styles.glassCard, { width: (width - 64) / 2 }]}>
         <View style={[styles.statIcon, { backgroundColor: '#64ffda15', borderColor: '#64ffda30' }]}>
           <Shield size={22} color="#64ffda" />
         </View>
         <Text style={styles.statValue}>Genome</Text>
         <Text style={styles.statLabel}>v200.0 Certified</Text>
      </View>
      <View style={[styles.glassCard, { width: (width - 64) / 2 }]}>
         <View style={[styles.statIcon, { backgroundColor: '#ff525215', borderColor: '#ff525230' }]}>
           <Activity size={22} color="#ff5252" />
         </View>
         <Text style={styles.statValue}>1,420</Text>
         <Text style={styles.statLabel}>Recombinations</Text>
      </View>
    </View>

    <View style={styles.section}>
      <Text style={styles.sectionTitle}>Realms of Light</Text>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 12 }}>
         <DomainBtn icon={Terminal} label="Forge" color="#64ffda" />
         <DomainBtn icon={Book} label="Learner" color="#ffd740" />
         <DomainBtn icon={Briefcase} label="Enterprise" color="#ff5252" />
         <DomainBtn icon={FlaskConical} label="Scholar" color="#64ffda" />
      </View>
    </View>

    <View style={styles.section}>
      <Text style={styles.sectionTitle}>System Vitals</Text>
      <View style={styles.glassCard}>
         <ResonanceItem label="Fidelity" value="99.9%" color="#64ffda" />
         <ResonanceItem label="PQC Strength" value="1024-bit" color="#ffd740" />
      </View>
    </View>
  </ScrollView>
);

const DomainBtn = ({ icon: Icon, label, color }) => (
  <TouchableOpacity style={[styles.glassCard, { width: (width - 76) / 4, alignItems: 'center', padding: 12 }]}>
     <Icon size={18} color={color} />
     <Text style={[styles.statLabel, { fontSize: 8, marginTop: 8 }]}>{label}</Text>
  </TouchableOpacity>
);

const ForgeScreen = () => {
  return (
    <View style={{ flex: 1, padding: 24, paddingTop: 60 }}>
      <Text style={styles.title}>THE FORGE</Text>
      <Text style={styles.subtitle}>DEVELOPER REALM • L7 UNIVERSE</Text>

      <View style={[styles.glassCard, { marginTop: 40, height: 300, justifyContent: 'center', alignItems: 'center' }]}>
         <Terminal size={64} color="#64ffda" />
         <Text style={{ color: 'white', fontWeight: '900', fontSize: 18, marginTop: 20 }}>Visual Agent Composer</Text>
         <Text style={{ color: '#64748b', fontWeight: '800', fontSize: 10, marginTop: 8, textTransform: 'uppercase' }}>Composition Stub for Mobile</Text>
      </View>

      <TouchableOpacity style={{ marginTop: 24, backgroundColor: '#64ffda', padding: 20, borderRadius: 20, alignItems: 'center' }}>
         <Text style={{ color: '#020617', fontWeight: '900', textTransform: 'uppercase' }}>Initiate Recombination</Text>
      </TouchableOpacity>
    </View>
  );
};

const ResonanceItem = ({ label, value, color }) => (
  <View style={styles.resRow}>
    <Text style={styles.resLabel}>{label}</Text>
    <View style={styles.resBarBg}>
       <View style={[styles.resBarFill, { width: '90%', backgroundColor: color }]} />
    </View>
    <Text style={[styles.resValue, { color }]}>{value}</Text>
  </View>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={{ flex: 1 }}>
        {activeTab === 'dashboard' && <DashboardScreen />}
        {activeTab === 'forge' && <ForgeScreen />}
      </View>

      <View style={styles.navBar}>
        <NavBtn icon={LayoutDashboard} label="Pulse" active={activeTab === 'dashboard'} onPress={() => setActiveTab('dashboard')} />
        <NavBtn icon={Terminal} label="Forge" active={activeTab === 'forge'} onPress={() => setActiveTab('forge')} />
        <NavBtn icon={Globe} label="Civil" active={activeTab === 'other'} onPress={() => {}} />
        <NavBtn icon={Fingerprint} label="Soul" active={activeTab === 'other'} onPress={() => {}} />
        <NavBtn icon={Settings} label="Admin" active={activeTab === 'other'} onPress={() => {}} />
      </View>
    </SafeAreaView>
  );
}

const NavBtn = ({ icon: Icon, label, active, onPress }) => (
  <TouchableOpacity onPress={onPress} style={styles.navItem}>
    <Icon size={24} color={active ? '#64ffda' : '#64748b'} />
    <Text style={[styles.navText, active && { color: '#64ffda' }]}>{label}</Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#020617' },
  scrollContent: { padding: 24, paddingTop: 40, paddingBottom: 120 },
  header: { marginBottom: 40 },
  title: { color: '#64ffda', fontSize: 32, fontWeight: '900', letterSpacing: 4, textAlign: 'center' },
  subtitle: { color: '#64748b', fontSize: 10, fontWeight: '800', textAlign: 'center', marginTop: 8, letterSpacing: 1 },
  statsGrid: { flexDirection: 'row', justifyContent: 'space-between' },
  glassCard: { backgroundColor: '#0f172a80', padding: 20, borderRadius: 32, borderWidth: 1, borderColor: 'rgba(255,255,255,0.05)' },
  statIcon: { width: 48, height: 48, borderRadius: 16, borderWidth: 1, alignItems: 'center', justifyContent: 'center', marginBottom: 16 },
  statValue: { color: 'white', fontSize: 24, fontWeight: '900' },
  statLabel: { color: '#64748b', fontSize: 10, fontWeight: '800', textTransform: 'uppercase', marginTop: 4 },
  section: { marginTop: 40 },
  sectionTitle: { color: 'white', fontSize: 20, fontWeight: '900', marginBottom: 20 },
  resRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 16 },
  resLabel: { color: '#64748b', fontSize: 10, fontWeight: '800', width: 80 },
  resBarBg: { flex: 1, height: 4, backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: 2 },
  resBarFill: { height: '100%', borderRadius: 2 },
  resValue: { color: 'white', fontSize: 12, fontWeight: '900', width: 60, textAlign: 'right' },
  navBar: { position: 'absolute', bottom: 0, width: '100%', height: 100, backgroundColor: '#020617f0', flexDirection: 'row', borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)', paddingBottom: 30, paddingHorizontal: 12 },
  navItem: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  navText: { color: '#64748b', fontSize: 9, marginTop: 6, fontWeight: '800', textTransform: 'uppercase' }
});
