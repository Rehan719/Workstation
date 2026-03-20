import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, Dimensions, Platform } from 'react-native';
import { LayoutDashboard, Terminal, Globe, Fingerprint, Settings, Shield, Activity, GraduationCap, Code, Building2, BookOpen, Zap, Cpu, Users } from 'lucide-react-native';
import { useStore } from './src/store/mobileStore';

const { width } = Dimensions.get('window');

const DashboardScreen = () => {
  const { systemVitals, currentRealm, user } = useStore();

  const stats = [
    { label: 'Resonance', value: `${(systemVitals.swarmHealth * 100).toFixed(1)}%`, icon: Zap, color: '#64ffda' },
    { label: 'CPU Load', value: `${systemVitals.cpu.toFixed(1)}%`, icon: Cpu, color: '#38bdf8' },
    { label: 'Agents', value: systemVitals.activeAgents.toString(), icon: Users, color: '#ff5252' },
    { label: 'Status', value: 'Sovereign', icon: Shield, color: '#64ffda' },
  ];

  const realms = [
    { id: 'LEARNER', name: 'Learner', icon: GraduationCap, color: '#ffd740' },
    { id: 'DEVELOPER', name: 'Forge', icon: Code, color: '#64ffda' },
    { id: 'ENTERPRISE', name: 'Market', icon: Building2, color: '#ff5252' },
    { id: 'SCHOLAR', name: 'Scholar', icon: BookOpen, color: '#38bdf8' },
  ];

  return (
    <ScrollView contentContainerStyle={styles.scrollContent}>
      <View style={styles.header}>
        <Text style={styles.title}>WORKSTATION <Text style={{color: '#64ffda'}}>v3.0</Text></Text>
        <Text style={styles.subtitle}>GENESIS EPOCH • SOVEREIGN INTERFACE</Text>
      </View>

      <View style={styles.welcomeSection}>
        <Text style={styles.welcomeText}>Welcome, <Text style={{color: 'white'}}>{user?.displayName || 'Guardian'}</Text></Text>
        <View style={styles.badgeRow}>
           <View style={styles.statusBadge}><View style={styles.pulseDot}/><Text style={styles.badgeText}>Live Resonance</Text></View>
        </View>
      </View>

      <View style={styles.statsGrid}>
        {stats.map((stat, i) => (
          <View key={i} style={[styles.glassCard, { width: (width - 60) / 2, marginBottom: 12 }]}>
             <View style={[styles.statIcon, { backgroundColor: `${stat.color}15`, borderColor: `${stat.color}30` }]}>
               <stat.icon size={20} color={stat.color} />
             </View>
             <Text style={styles.statValue}>{stat.value}</Text>
             <Text style={styles.statLabel}>{stat.label}</Text>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Audience Realms</Text>
        <View style={styles.realmGrid}>
           {realms.map((realm) => (
             <TouchableOpacity
               key={realm.id}
               style={[styles.realmCard, currentRealm === realm.id && { borderColor: realm.color, backgroundColor: `${realm.color}10` }]}
             >
                <realm.icon size={24} color={currentRealm === realm.id ? realm.color : '#64748b'} />
                <Text style={[styles.realmLabel, currentRealm === realm.id && { color: 'white' }]}>{realm.name}</Text>
             </TouchableOpacity>
           ))}
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Command Center</Text>
        <View style={styles.glassCard}>
           <Text style={styles.placeholderText}>Multi-modal HUD channels active on sidebar (Desktop) / bottom sheet (Mobile)</Text>
           <TouchableOpacity style={styles.actionBtn}>
              <Text style={styles.actionBtnText}>Open HUD</Text>
           </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={{ flex: 1 }}>
        {activeTab === 'dashboard' && <DashboardScreen />}
        {activeTab === 'forge' && <View style={styles.centered}><Text style={styles.title}>FORGE</Text></View>}
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
    <Icon size={22} color={active ? '#64ffda' : '#64748b'} />
    <Text style={[styles.navText, active && { color: '#64ffda' }]}>{label}</Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#020617' },
  scrollContent: { padding: 20, paddingTop: 30, paddingBottom: 120 },
  header: { marginBottom: 32 },
  title: { color: 'white', fontSize: 28, fontWeight: '900', letterSpacing: 2, textAlign: 'center' },
  subtitle: { color: '#64748b', fontSize: 9, fontWeight: '800', textAlign: 'center', marginTop: 6, letterSpacing: 1 },
  welcomeSection: { marginBottom: 32 },
  welcomeText: { color: '#64748b', fontSize: 18, fontWeight: '800' },
  badgeRow: { flexDirection: 'row', marginTop: 12 },
  statusBadge: { backgroundColor: '#0f172a', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 20, flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: '#1e293b' },
  pulseDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: '#10b981', marginRight: 8 },
  badgeText: { color: '#64748b', fontSize: 9, fontWeight: '900', textTransform: 'uppercase', letterSpacing: 1 },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  glassCard: { backgroundColor: '#0f172a80', padding: 16, borderRadius: 24, borderWidth: 1, borderColor: 'rgba(255,255,255,0.05)' },
  statIcon: { width: 40, height: 40, borderRadius: 12, borderWidth: 1, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  statValue: { color: 'white', fontSize: 20, fontWeight: '900' },
  statLabel: { color: '#64748b', fontSize: 9, fontWeight: '800', textTransform: 'uppercase', marginTop: 2 },
  section: { marginTop: 32 },
  sectionTitle: { color: 'white', fontSize: 18, fontWeight: '900', marginBottom: 16 },
  realmGrid: { flexDirection: 'row', justifyContent: 'space-between' },
  realmCard: { width: (width - 76) / 4, height: 80, backgroundColor: '#0f172a', borderRadius: 20, borderWidth: 1, borderColor: 'rgba(255,255,255,0.05)', alignItems: 'center', justifyContent: 'center' },
  realmLabel: { color: '#64748b', fontSize: 8, fontWeight: '800', marginTop: 8, textTransform: 'uppercase' },
  placeholderText: { color: '#64748b', fontSize: 12, fontWeight: '700', lineHeight: 18, marginBottom: 16 },
  actionBtn: { backgroundColor: '#1e293b', paddingVertical: 12, borderRadius: 12, alignItems: 'center' },
  actionBtnText: { color: 'white', fontSize: 10, fontWeight: '900', textTransform: 'uppercase', letterSpacing: 1 },
  navBar: { position: 'absolute', bottom: 0, width: '100%', height: 90, backgroundColor: '#020617', flexDirection: 'row', borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)', paddingBottom: 25, paddingHorizontal: 10 },
  navItem: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  navText: { color: '#64748b', fontSize: 8, marginTop: 4, fontWeight: '800', textTransform: 'uppercase' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' }
});
