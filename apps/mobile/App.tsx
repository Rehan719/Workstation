import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, Dimensions, TextInput, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { LayoutDashboard, Zap, Brain, Globe, Sparkles, Send, Bot, User, MessageSquare, Settings, Shield, ShoppingBag, Cpu, Book, FlaskConical, Scale, Briefcase, GraduationCap, Star, Award, Plus, Wifi, Landmark, TrendingUp, Target, Activity, Radio, GitBranch, Fingerprint, Terminal, Layers } from 'lucide-react-native';
import { useStore } from './src/store/mobileStore';
import { useBiometrics } from './src/hooks/useBiometrics';
import { MessageItem } from './src/components/MessageItem';

const { width } = Dimensions.get('window');

const DashboardScreen = () => {
  const { systemVitals, currentRealm, user } = useStore();

  const stats = [
    { label: 'Resonance', value: `${(systemVitals.swarmHealth * 100).toFixed(1)}%`, icon: Zap, color: '#64ffda' },
    { label: 'CPU Load', value: `${systemVitals.cpu.toFixed(1)}%`, icon: Cpu, color: '#38bdf8' },
    { label: 'Agents', value: systemVitals.activeAgents.toString(), icon: Users, color: '#ff5252' },
    { label: 'Status', value: 'Sovereign', icon: Shield, color: '#64ffda' },
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
        <Text style={styles.sectionTitle}>System Vitals</Text>
        <View style={styles.glassCard}>
           <ResonanceItem label="PQC Strength" value="1024-bit" color="#ffd740" />
           <ResonanceItem label="UEG Sync" value="Verified" color="#64ffda" />
        </View>
      </View>
    </ScrollView>
  );
};

const CEOChatScreen = () => {
  const [msg, setMsg] = useState('');
  const [messages, setMessages] = useState([
    { id: '1', role: 'assistant', content: 'I am the VSB AI CEO. How can I assist with your sovereign operation?' }
  ]);

  const send = () => {
    if (!msg.trim()) return;
    setMessages([...messages, { id: Date.now().toString(), role: 'user', content: msg }]);
    setMsg('');
    setTimeout(() => {
       setMessages(prev => [...prev, { id: 'bot-'+Date.now(), role: 'assistant', content: 'Directive received. Analysis in progress...' }]);
    }, 1000);
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={{ flex: 1 }}>
       <View style={{ flex: 1, padding: 20, paddingTop: 40 }}>
          <Text style={styles.sectionTitle}>VSB AI CEO Consultation</Text>
          <FlatList
            data={messages}
            keyExtractor={m => m.id}
            renderItem={({item}) => <MessageItem message={item} />}
            contentContainerStyle={{ paddingBottom: 20 }}
          />
          <View style={{ flexDirection: 'row', gap: 10, alignItems: 'center', marginBottom: 20 }}>
             <TextInput
               value={msg}
               onChangeText={setMsg}
               placeholder="Enter directive..."
               placeholderTextColor="#475569"
               style={{ flex: 1, backgroundColor: '#0f172a', borderWidth: 1, borderColor: '#1e293b', borderRadius: 15, padding: 15, color: 'white', fontWeight: 'bold' }}
             />
             <TouchableOpacity onPress={send} style={{ backgroundColor: '#64ffda', width: 50, height: 50, borderRadius: 25, items: 'center', justifyContent: 'center', alignItems: 'center' }}>
                <Send size={20} color="#020617" />
             </TouchableOpacity>
          </View>
       </View>
    </KeyboardAvoidingView>
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
  const { authenticate } = useBiometrics();

  useEffect(() => {
    authenticate();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={{ flex: 1 }}>
        {activeTab === 'dashboard' && <DashboardScreen />}
        {activeTab === 'ceo' && <CEOChatScreen />}
        {activeTab === 'forge' && <View style={styles.centered}><Text style={styles.title}>FORGE</Text></View>}
      </View>

      <View style={styles.navBar}>
        <NavBtn icon={LayoutDashboard} label="Pulse" active={activeTab === 'dashboard'} onPress={() => setActiveTab('dashboard')} />
        <NavBtn icon={MessageSquare} label="CEO" active={activeTab === 'ceo'} onPress={() => setActiveTab('ceo')} />
        <NavBtn icon={Terminal} label="Forge" active={activeTab === 'forge'} onPress={() => setActiveTab('forge')} />
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
  resRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 16 },
  resLabel: { color: '#64748b', fontSize: 9, fontWeight: '800', width: 100 },
  resBarBg: { flex: 1, height: 4, backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: 2 },
  resBarFill: { height: '100%', borderRadius: 2 },
  resValue: { color: 'white', fontSize: 10, fontWeight: '900', width: 60, textAlign: 'right' },
  navBar: { position: 'absolute', bottom: 0, width: '100%', height: 90, backgroundColor: '#020617', flexDirection: 'row', borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)', paddingBottom: 25, paddingHorizontal: 10 },
  navItem: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  navText: { color: '#64748b', fontSize: 8, marginTop: 4, fontWeight: '800', textTransform: 'uppercase' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' }
});
