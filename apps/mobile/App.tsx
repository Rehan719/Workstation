import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, TextInput, Dimensions } from 'react-native';
import { Bot, LayoutDashboard, Package, User, Send, Zap, Cpu, TrendingUp, Brain, Globe, History } from 'lucide-react-native';

const { width } = Dimensions.get('window');

const StatCard = ({ label, value, icon: Icon, color }) => (
  <View style={styles.statCard}>
    <View style={styles.statHeader}>
      <View style={[styles.statIcon, { backgroundColor: color + '20' }]}>
        <Icon size={20} color={color} />
      </View>
    </View>
    <Text style={styles.statValue}>{value}</Text>
    <Text style={styles.statLabel}>{label}</Text>
  </View>
);

const DashboardScreen = () => (
  <ScrollView contentContainerStyle={styles.scrollContent}>
    <View style={styles.header}>
      <Text style={styles.title}>WORKSTATION</Text>
      <Text style={styles.subtitle}>Cognitive Gateway</Text>
    </View>

    <View style={styles.statsGrid}>
      <StatCard label="Fidelity" value="99.9%" icon={Zap} color="#38bdf8" />
      <StatCard label="Health" value="0.999" icon={Brain} color="#10b981" />
      <StatCard label="Signals" value="12 Active" icon={Globe} color="#fbbf24" />
      <StatCard label="Step" value="v139" icon={History} color="#64748b" />
    </View>

    <View style={styles.section}>
      <Text style={styles.sectionTitle}>Biochemical Resonance</Text>
      <View style={styles.resonanceRow}>
        <ResonanceItem label="OXY" value="96%" color="#10b981" />
        <ResonanceItem label="SER" value="92%" color="#fbbf24" />
        <ResonanceItem label="DOP" value="98%" color="#38bdf8" />
      </View>
    </View>
  </ScrollView>
);

const ResonanceItem = ({ label, value, color }) => (
  <View style={styles.resItem}>
    <Text style={styles.resLabel}>{label}</Text>
    <Text style={[styles.resValue, { color }]}>{value}</Text>
  </View>
);

const ChatScreen = () => {
  const [msg, setMsg] = useState('');
  return (
    <View style={styles.flex1}>
      <ScrollView contentContainerStyle={styles.chatScroll}>
        <View style={styles.botMsg}>
          <Text style={styles.msgText}>Cognitive convergence active. How shall we direct the evolution today?</Text>
        </View>
      </ScrollView>
      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Enter command..."
          placeholderTextColor="#64748b"
          value={msg}
          onChangeText={setMsg}
        />
        <TouchableOpacity style={styles.sendBtn}>
          <Send size={20} color="#020617" />
        </TouchableOpacity>
      </View>
    </View>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      {activeTab === 'dashboard' ? <DashboardScreen /> : <ChatScreen />}

      <View style={styles.navBar}>
        <TouchableOpacity onPress={() => setActiveTab('dashboard')} style={styles.navItem}>
          <LayoutDashboard size={24} color={activeTab === 'dashboard' ? '#38bdf8' : '#64748b'} />
          <Text style={[styles.navText, activeTab === 'dashboard' && styles.navTextActive]}>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('chat')} style={styles.navItem}>
          <Bot size={24} color={activeTab === 'chat' ? '#38bdf8' : '#64748b'} />
          <Text style={[styles.navText, activeTab === 'chat' && styles.navTextActive]}>AI CEO</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Globe size={24} color="#64748b" />
          <Text style={styles.navText}>World</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <History size={24} color="#64748b" />
          <Text style={styles.navText}>Evolution</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#020617' },
  flex1: { flex: 1 },
  scrollContent: { padding: 24, paddingTop: 40, paddingBottom: 100 },
  header: { marginBottom: 32 },
  title: { color: '#38bdf8', fontSize: 28, fontWeight: '900', letterSpacing: 2 },
  subtitle: { color: '#64748b', fontSize: 14, fontWeight: '700', textTransform: 'uppercase' },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  statCard: { width: (width - 64) / 2, backgroundColor: '#0f172a', padding: 20, borderRadius: 24, marginBottom: 16, borderWidth: 1, borderColor: '#1e293b' },
  statIcon: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  statValue: { color: 'white', fontSize: 20, fontWeight: '800' },
  statLabel: { color: '#64748b', fontSize: 10, fontWeight: '700', textTransform: 'uppercase', marginTop: 4 },
  section: { marginTop: 20 },
  sectionTitle: { color: 'white', fontSize: 18, fontWeight: '800', marginBottom: 16 },
  resonanceRow: { flexDirection: 'row', justifyContent: 'space-between', backgroundColor: '#0f172a', padding: 24, borderRadius: 24, borderWidth: 1, borderColor: '#1e293b' },
  resItem: { alignItems: 'center' },
  resLabel: { color: '#64748b', fontSize: 10, fontWeight: '700', marginBottom: 4 },
  resValue: { fontSize: 20, fontWeight: '900' },
  navBar: { position: 'absolute', bottom: 0, width: '100%', height: 90, backgroundColor: '#020617', flexDirection: 'row', borderTopWidth: 1, borderTopColor: '#1e293b', paddingBottom: 20 },
  navItem: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  navText: { color: '#64748b', fontSize: 10, marginTop: 4, fontWeight: '700' },
  navTextActive: { color: '#38bdf8' },
  chatScroll: { padding: 20, paddingTop: 60 },
  botMsg: { backgroundColor: '#1e293b', padding: 16, borderRadius: 20, borderTopLeftRadius: 4, maxWidth: '80%' },
  msgText: { color: 'white', fontSize: 14, lineHeight: 20 },
  inputRow: { flexDirection: 'row', padding: 16, paddingBottom: 110, backgroundColor: '#020617', gap: 12 },
  input: { flex: 1, backgroundColor: '#0f172a', borderRadius: 16, paddingHorizontal: 16, color: 'white', borderWidth: 1, borderColor: '#1e293b' },
  sendBtn: { backgroundColor: '#38bdf8', width: 48, height: 48, borderRadius: 16, alignItems: 'center', justifyContent: 'center' }
});
