import React, { useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, TextInput, Dimensions } from 'react-native';
import { Bot, LayoutDashboard, Package, User, Send, Zap, Cpu, TrendingUp } from 'lucide-react-native';

const { width } = Dimensions.get('window');

const StatCard = ({ label, value, icon: Icon, color }) => (
  <View style={styles.statCard}>
    <div style={styles.statHeader}>
      <div style={[styles.statIcon, { backgroundColor: color + '20' }]}>
        <Icon size={20} color={color} />
      </div>
    </div>
    <Text style={styles.statValue}>{value}</Text>
    <Text style={styles.statLabel}>{label}</Text>
  </View>
);

const DashboardScreen = () => (
  <ScrollView contentContainerStyle={styles.scrollContent}>
    <View style={styles.header}>
      <Text style={styles.title}>WORKSTATION</Text>
      <Text style={styles.subtitle}>Sovereign Gateway</Text>
    </View>

    <View style={styles.statsGrid}>
      <StatCard label="Fidelity" value="99.9%" icon={Zap} color="#38bdf8" />
      <StatCard label="Agents" value="42" icon={Cpu} color="#10b981" />
      <StatCard label="Network" value="1.4M" icon={TrendingUp} color="#fbbf24" />
      <StatCard label="Nodes" value="108" icon={User} color="#64748b" />
    </View>

    <View style={styles.section}>
      <Text style={styles.sectionTitle}>System Resonance</Text>
      <View style={styles.resonanceCard}>
        <View style={styles.pulseInner}>
           <Text style={styles.pulseText}>ACTIVE</Text>
        </View>
      </View>
    </View>
  </ScrollView>
);

const ChatScreen = () => {
  const [msg, setMsg] = useState('');
  return (
    <View style={styles.flex1}>
      <ScrollView contentContainerStyle={styles.chatScroll}>
        <View style={styles.botMsg}>
          <Text style={styles.msgText}>Greetings, Guardian. How shall we direct the evolution today?</Text>
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
          <Text style={[styles.navText, activeTab === 'dashboard' && styles.navTextActive]}>Dashboard</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('chat')} style={styles.navItem}>
          <Bot size={24} color={activeTab === 'chat' ? '#38bdf8' : '#64748b'} />
          <Text style={[styles.navText, activeTab === 'chat' && styles.navTextActive]}>AI CEO</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <Package size={24} color="#64748b" />
          <Text style={styles.navText}>Catalog</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.navItem}>
          <User size={24} color="#64748b" />
          <Text style={styles.navText}>Profile</Text>
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
  statHeader: { marginBottom: 12 },
  statIcon: { width: 40, height: 40, borderRadius: 12, alignItems: 'center', justifyContent: 'center' },
  statValue: { color: 'white', fontSize: 20, fontWeight: '800' },
  statLabel: { color: '#64748b', fontSize: 10, fontWeight: '700', textTransform: 'uppercase', marginTop: 4 },
  section: { marginTop: 20 },
  sectionTitle: { color: 'white', fontSize: 18, fontWeight: '800', marginBottom: 16 },
  resonanceCard: { height: 160, backgroundColor: '#0f172a', borderRadius: 24, alignItems: 'center', justifyContent: 'center', borderStyle: 'dashed', borderWidth: 1, borderColor: '#38bdf850' },
  pulseInner: { width: 80, height: 80, borderRadius: 40, backgroundColor: '#38bdf820', alignItems: 'center', justifyContent: 'center', borderWidth: 1, borderColor: '#38bdf8' },
  pulseText: { color: '#38bdf8', fontSize: 10, fontWeight: '900' },
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
