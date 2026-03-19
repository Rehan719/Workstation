import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, Dimensions, TextInput, FlatList, KeyboardAvoidingView, Platform } from 'react-native';
import { LayoutDashboard, Zap, Brain, Globe, Sparkles, Send, Bot, User, MessageSquare, Settings, Shield, ShoppingBag, Cpu, Book, FlaskConical, Scale, Briefcase, GraduationCap, Star, Award, Plus, Wifi, Landmark, TrendingUp, Target, Activity } from 'lucide-react-native';

const { width, height } = Dimensions.get('window');

const DashboardScreen = ({ wallet, insights }) => (
  <ScrollView contentContainerStyle={styles.scrollContent}>
    <View style={styles.header}>
      <Text style={styles.title}>WORKSTATION</Text>
      <Text style={styles.subtitle}>COLLECTIVE INTELLIGENCE ACTIVE • v152.0</Text>
    </View>

    <View style={styles.statsGrid}>
      <View style={[styles.glassCard, { width: (width - 64) / 2 }]}>
         <View style={[styles.statIcon, { backgroundColor: '#64ffda15', borderColor: '#64ffda30' }]}>
           <Brain size={22} color="#64ffda" />
         </View>
         <Text style={styles.statValue}>Brain</Text>
         <Text style={styles.statLabel}>Planetary Intel</Text>
      </View>
      <View style={[styles.glassCard, { width: (width - 64) / 2 }]}>
         <View style={[styles.statIcon, { backgroundColor: '#ff525215', borderColor: '#ff525230' }]}>
           <Cpu size={22} color="#ff5252" />
         </View>
         <Text style={styles.statValue}>1,420</Text>
         <Text style={styles.statLabel}>Autonomous Decisions</Text>
      </View>
    </View>

    <View style={styles.section}>
      <Text style={styles.sectionTitle}>Latest Insight</Text>
      <View style={[styles.glassCard, { borderLeftWidth: 4, borderLeftColor: '#64ffda' }]}>
         <Text style={{ color: 'white', fontWeight: '900', fontSize: 16 }}>{insights[0]?.title || 'Analyzing Ecosystem...'}</Text>
         <Text style={{ color: '#64748b', fontWeight: '700', fontSize: 12, marginTop: 8 }}>{insights[0]?.observation}</Text>
      </View>
    </View>

    <View style={styles.section}>
      <Text style={styles.sectionTitle}>Civilization Hubs</Text>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap', gap: 12 }}>
         <DomainBtn icon={Globe} label="Brain" color="#64ffda" />
         <DomainBtn icon={Target} label="Wisdom" color="#ffd740" />
         <DomainBtn icon={Shield} label="Gov" color="#64ffda" />
         <DomainBtn icon={Briefcase} label="Start" color="#ffd740" />
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

const CEOScreen = () => {
  const [messages, setMessages] = useState([{ role: 'assistant', content: 'Greeting, Citizen. v152.0 Collective Intelligence is online. How shall we coordinate our collective resonance today?' }]);
  const [input, setInput] = useState('');

  const send = () => {
    if (!input.trim()) return;
    setMessages([...messages, { role: 'user', content: input }, { role: 'assistant', content: 'Synthesis in progress. Collective intelligence updated.' }]);
    setInput('');
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={{ flex: 1 }}>
      <View style={[styles.header, { paddingHorizontal: 24, paddingTop: 60, marginBottom: 20 }]}>
        <Text style={styles.title}>AI CEO</Text>
        <Text style={styles.subtitle}>CIVILIZATION MODE ACTIVE</Text>
      </View>
      <FlatList
        data={messages}
        keyExtractor={(_, i) => i.toString()}
        contentContainerStyle={{ padding: 24 }}
        renderItem={({ item }) => (
          <View style={[styles.msgContainer, item.role === 'user' ? styles.userMsg : styles.botMsg]}>
            <Text style={styles.msgText}>{item.content}</Text>
          </View>
        )}
      />
      <View style={styles.inputArea}>
        <TextInput
          value={input}
          onChangeText={setInput}
          placeholder="Issue directive..."
          placeholderTextColor="#64748b"
          style={styles.input}
        />
        <TouchableOpacity onPress={send} style={styles.sendBtn}>
          <Send size={20} color="#020617" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [insights, setInsights] = useState([{ title: 'Viral Trend Detected', observation: '14% increase in Bio-Reactor creations.' }]);

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={{ flex: 1 }}>
        {activeTab === 'dashboard' && <DashboardScreen insights={insights} />}
        {activeTab === 'ceo' && <CEOScreen />}
        {activeTab === 'intel' && (
          <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', padding: 40 }}>
            <Activity size={64} color="#64ffda" />
            <Text style={{ color: 'white', fontWeight: '900', fontSize: 24, marginTop: 20, textAlign: 'center' }}>Civilization Brain</Text>
            <Text style={{ color: '#64748b', fontWeight: '800', fontSize: 10, marginTop: 8, textTransform: 'uppercase', textAlign: 'center' }}>Real-time Intelligence Active</Text>
          </View>
        )}
      </View>

      <View style={styles.navBar}>
        <NavBtn icon={LayoutDashboard} label="Pulse" active={activeTab === 'dashboard'} onPress={() => setActiveTab('dashboard')} />
        <NavBtn icon={MessageSquare} label="CEO" active={activeTab === 'ceo'} onPress={() => setActiveTab('ceo')} />
        <NavBtn icon={Globe} label="Intel" active={activeTab === 'intel'} onPress={() => setActiveTab('intel')} />
        <NavBtn icon={Target} label="Wisdom" active={activeTab === 'other'} onPress={() => {}} />
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
  resValue: { color: 'white', fontSize: 12, fontWeight: '900', width: 40, textAlign: 'right' },
  navBar: { position: 'absolute', bottom: 0, width: '100%', height: 100, backgroundColor: '#020617f0', flexDirection: 'row', borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)', paddingBottom: 30, paddingHorizontal: 12 },
  navItem: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  navText: { color: '#64748b', fontSize: 9, marginTop: 6, fontWeight: '800', textTransform: 'uppercase' },
  msgContainer: { padding: 20, borderRadius: 24, marginBottom: 16, maxWidth: '85%' },
  botMsg: { backgroundColor: '#0f172a', borderBottomLeftRadius: 4, alignSelf: 'flex-start', borderLeftWidth: 2, borderLeftColor: '#64ffda' },
  userMsg: { backgroundColor: '#ffd74020', borderBottomRightRadius: 4, alignSelf: 'flex-end', borderRightWidth: 2, borderRightColor: '#ffd740' },
  msgText: { color: 'white', fontWeight: '700', fontSize: 14, lineHeight: 20 },
  inputArea: { padding: 20, paddingBottom: 110, backgroundColor: '#020617', flexDirection: 'row', gap: 12, alignItems: 'center' },
  input: { flex: 1, height: 56, backgroundColor: '#0f172a', borderRadius: 20, paddingHorizontal: 20, color: 'white', fontWeight: '700' },
  sendBtn: { width: 56, height: 56, backgroundColor: '#64ffda', borderRadius: 20, alignItems: 'center', justifyContent: 'center' }
});
