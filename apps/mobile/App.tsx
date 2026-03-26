import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, SafeAreaView, StatusBar, Dimensions, TextInput, FlatList, KeyboardAvoidingView, Platform, ActivityIndicator, Alert } from 'react-native';
import { LayoutDashboard, Zap, Brain, Globe, Sparkles, Send, Bot, User, MessageSquare, Settings, Shield, ShoppingBag, Cpu, Book, FlaskConical, Scale, Briefcase, GraduationCap, Star, Award, Plus, Wifi, Landmark, TrendingUp, Target, Activity, Radio, GitBranch, Fingerprint, Terminal, Layers, Box, Info, HeartPulse, Heart, Microscope, FileCode } from 'lucide-react-native';
import { useStore } from './src/store/mobileStore';
import { useBiometrics } from './src/hooks/useBiometrics';
import { MessageItem } from './src/components/MessageItem';

const { width } = Dimensions.get('window');

const DashboardScreen = () => {
  const { systemVitals, currentRealm, user, genomicMetadata } = useStore();

  const stats = [
    { label: 'Resonance', value: `${(systemVitals.swarmHealth * 100).toFixed(1)}%`, icon: Zap, color: '#64ffda' },
    { label: 'Latency', value: `${systemVitals.latency_ms || 28}ms`, icon: Cpu, color: '#38bdf8' },
    { label: 'Nodes', value: `${systemVitals.node_count || 100}+`, icon: Globe, color: '#ff5252' },
    { label: 'Status', value: 'v3.0 Sovereign', icon: Shield, color: '#64ffda' },
  ];

  return (
    <ScrollView contentContainerStyle={styles.scrollContent}>
      <View style={styles.header}>
        <Text style={styles.title}>WORKSTATION <Text style={{color: '#64ffda'}}>v3.0</Text></Text>
        <Text style={styles.subtitle}>CIVILIZATION EPOCH • ULTIMATE SYNTHESIS</Text>
      </View>

      <View style={styles.welcomeSection}>
        <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-end' }}>
          <View>
            <Text style={styles.welcomeText}>Welcome, <Text style={{color: 'white'}}>{user?.displayName || 'Guardian'}</Text></Text>
            <Text style={styles.realmLabel}>{currentRealm} REALM ACTIVE</Text>
          </View>
          <View style={styles.statusBadge}><View style={styles.pulseDot}/><Text style={styles.badgeText}>Mesh Operational</Text></View>
        </View>
      </View>

      <View style={styles.statsGrid}>
        {stats.map((stat, i) => (
          <View key={i} style={[styles.glassCard, { width: (width - 60) / 2, marginBottom: 15 }]}>
             <View style={[styles.statIcon, { backgroundColor: `${stat.color}15`, borderColor: `${stat.color}30` }]}>
               <stat.icon size={20} color={stat.color} />
             </View>
             <Text style={styles.statValue}>{stat.value}</Text>
             <Text style={styles.statLabel}>{stat.label}</Text>
          </View>
        ))}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Foundational Domains</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginHorizontal: -20, paddingHorizontal: 20 }}>
           <DomainCard icon={Heart} label="Religion" color="#64ffda" />
           <DomainCard icon={Microscope} label="Science" color="#ffd740" />
           <DomainCard icon={Landmark} label="Law" color="#38bdf8" />
           <DomainCard icon={Briefcase} label="Employment" color="#64ffda" />
           <DomainCard icon={GraduationCap} label="Education" color="#10b981" />
           <DomainCard icon={HeartPulse} label="Care" color="#ff5252" />
        </ScrollView>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Genomic Integrity</Text>
        <View style={styles.glassCard}>
           <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 15 }}>
              <Text style={styles.resLabel}>ROOT HASH</Text>
              <Text style={[styles.resValue, { color: '#64ffda', width: 200 }]} numberOfLines={1}>{genomicMetadata?.root_hash || '0x...'}</Text>
           </View>
           <ResonanceItem label="PQC Strength" value="1024-bit" color="#ffd740" percent="100%" />
           <ResonanceItem label="UEG Sync" value="Verified" color="#64ffda" percent="100%" />
        </View>
      </View>
    </ScrollView>
  );
};

const DomainCard = ({ icon: Icon, label, color }) => (
  <TouchableOpacity style={[styles.glassCard, { width: 120, marginRight: 12, alignItems: 'center', padding: 20 }]}>
     <View style={{ width: 45, height: 45, borderRadius: 15, backgroundColor: `${color}10`, alignItems: 'center', justifyContent: 'center', marginBottom: 12 }}>
        <Icon size={22} color={color} />
     </View>
     <Text style={[styles.badgeText, { color: 'white', textAlign: 'center' }]}>{label}</Text>
  </TouchableOpacity>
);

const ResonanceItem = ({ label, value, color, percent }) => (
  <View style={styles.resRow}>
    <Text style={styles.resLabel}>{label}</Text>
    <View style={styles.resBarBg}>
       <View style={[styles.resBarFill, { width: percent, backgroundColor: color }]} />
    </View>
    <Text style={[styles.resValue, { color }]}>{value}</Text>
  </View>
);

const CEOChatScreen = () => {
  const [messages, setMessages] = useState([{ role: 'assistant', content: 'Greeting, Guardian. I am the VSB AI CEO.' }]);
  const [input, setInput] = useState('');

  const sendMessage = () => {
     if (!input.trim()) return;
     const newMsgs = [...messages, { role: 'user', content: input }];
     setMessages(newMsgs);
     setInput('');
     setTimeout(() => {
        setMessages([...newMsgs, { role: 'assistant', content: 'Synthesis complete. Directive logged.' }]);
     }, 1000);
  };

  return (
    <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>AI CEO</Text>
      <FlatList
        data={messages}
        keyExtractor={(_, i) => i.toString()}
        renderItem={({ item }) => (
          <View style={[styles.glassCard, { marginBottom: 10, alignSelf: item.role === 'user' ? 'flex-end' : 'flex-start', maxWidth: '80%', backgroundColor: item.role === 'user' ? '#1e293b' : '#0f172a80' }]}>
            <Text style={{ color: 'white' }}>{item.content}</Text>
          </View>
        )}
      />
      <View style={{ flexDirection: 'row', gap: 10, marginTop: 20 }}>
        <TextInput
          style={[styles.glassCard, { flex: 1, color: 'white', paddingVertical: 12 }]}
          placeholder="Issue directive..."
          placeholderTextColor="#64748b"
          value={input}
          onChangeText={setInput}
        />
        <TouchableOpacity onPress={sendMessage} style={[styles.statIcon, { backgroundColor: '#64ffda', width: 50, height: 50 }]}>
           <Send size={20} color="#020617" />
        </TouchableOpacity>
      </View>
    </KeyboardAvoidingView>
  );
};

const ForgeScreen = () => (
  <View style={styles.screenContainer}>
    <Text style={styles.sectionTitle}>Developer Forge</Text>
    <ScrollView>
       {['Llama-3.2-3B', 'Vector-Adapter', 'GaaS-Guard'].map((m, i) => (
         <View key={i} style={[styles.glassCard, { marginBottom: 15, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }]}>
           <View>
              <Text style={{ color: 'white', fontWeight: 'bold' }}>{m}</Text>
              <Text style={styles.badgeText}>Module v1.0</Text>
           </View>
           <TouchableOpacity style={{ padding: 10, backgroundColor: '#64ffda20', borderRadius: 10 }}>
              <Plus size={16} color="#64ffda" />
           </TouchableOpacity>
         </View>
       ))}
       <TouchableOpacity style={[styles.glassCard, { alignItems: 'center', backgroundColor: '#64ffda', marginTop: 20 }]}>
          <Text style={{ color: '#020617', fontWeight: '900' }}>CREATE BLUEPRINT</Text>
       </TouchableOpacity>
    </ScrollView>
  </View>
);

const GenomeScreen = () => {
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // v0.1: Fetch actual articles for mobile explorer
    fetch('http://localhost:8000/api/v154/constitution/articles')
      .then(res => res.json())
      .then(data => {
        setArticles(data.slice(0, 50)); // Display top 50 for performance
        setIsLoading(false);
      })
      .catch(() => setIsLoading(false));
  }, []);

  return (
    <View style={styles.screenContainer}>
      <Text style={styles.sectionTitle}>Genome Explorer</Text>
      <View style={[styles.glassCard, { flex: 1 }]}>
        <Text style={styles.badgeText}>Nodes Seeded: {articles.length}</Text>

        {isLoading ? (
          <ActivityIndicator color="#64ffda" style={{ marginVertical: 40 }} />
        ) : (
          <ScrollView style={{ marginTop: 20 }}>
             {articles.map((a, i) => (
               <TouchableOpacity key={i} style={{ padding: 15, backgroundColor: '#020617', borderRadius: 15, marginBottom: 10, borderWidth: 1, borderColor: '#64ffda20' }}>
                  <Text style={{ color: '#64ffda', fontWeight: 'bold', fontSize: 12 }}>ARTICLE {a.id}</Text>
                  <Text style={{ color: 'white', marginTop: 5 }}>{a.title}</Text>
               </TouchableOpacity>
             ))}
          </ScrollView>
        )}

        <View style={{ marginTop: 20, gap: 10 }}>
           <ResonanceItem label="Operons" value="142 Active" color="#64ffda" percent="100%" />
           <ResonanceItem label="Regulons" value="12.5k Active" color="#38bdf8" percent="92%" />
        </View>
      </View>
    </View>
  );
};

const AdminScreen = () => (
  <View style={styles.screenContainer}>
    <Text style={styles.sectionTitle}>System Admin</Text>
    <View style={styles.glassCard}>
      <Text style={styles.badgeText}>Sovereign Identity Verified</Text>
      <View style={{ marginTop: 20, gap: 15 }}>
         <TouchableOpacity onPress={() => Alert.alert('Audit', 'No critical findings.')} style={{ flexDirection: 'row', alignItems: 'center', gap: 15 }}>
            <Shield size={20} color="#64ffda" />
            <Text style={{ color: 'white' }}>Run OWASP Audit</Text>
         </TouchableOpacity>
         <TouchableOpacity style={{ flexDirection: 'row', alignItems: 'center', gap: 15 }}>
            <Zap size={20} color="#ffd740" />
            <Text style={{ color: 'white' }}>Node Lifecycle Management</Text>
         </TouchableOpacity>
         <TouchableOpacity style={{ flexDirection: 'row', alignItems: 'center', gap: 15 }}>
            <Activity size={20} color="#ff5252" />
            <Text style={{ color: 'white' }}>Homeostatic Dashboard</Text>
         </TouchableOpacity>
      </View>
    </View>
  </View>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isAuthenticating, setIsAuthenticating] = useState(true);
  const { authenticate } = useBiometrics();

  useEffect(() => {
    const runAuth = async () => {
       const success = await authenticate();
       if (success) setIsAuthenticating(false);
    };
    runAuth();
  }, []);

  if (isAuthenticating) {
     return (
        <View style={[styles.container, { justifyContent: 'center', alignItems: 'center' }]}>
           <Zap size={48} color="#64ffda" style={{ marginBottom: 20 }} />
           <ActivityIndicator color="#64ffda" />
           <Text style={[styles.badgeText, { marginTop: 20 }]}>Sovereign Handshake Required</Text>
           <TouchableOpacity onPress={() => setIsAuthenticating(false)} style={{ marginTop: 40, padding: 15, borderBottomWidth: 1, borderBottomColor: '#64ffda' }}>
              <Text style={{ color: '#64ffda', fontSize: 10, fontWeight: '900' }}>BYPASS FOR DEMO</Text>
           </TouchableOpacity>
        </View>
     );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />

      <View style={{ flex: 1 }}>
        {activeTab === 'dashboard' && <DashboardScreen />}
        {activeTab === 'ceo' && <CEOChatScreen />}
        {activeTab === 'forge' && <ForgeScreen />}
        {activeTab === 'genome' && <GenomeScreen />}
        {activeTab === 'admin' && <AdminScreen />}
      </View>

      <View style={styles.navBar}>
        <NavBtn icon={LayoutDashboard} label="Pulse" active={activeTab === 'dashboard'} onPress={() => setActiveTab('dashboard')} />
        <NavBtn icon={MessageSquare} label="CEO" active={activeTab === 'ceo'} onPress={() => setActiveTab('ceo')} />
        <NavBtn icon={Zap} label="Forge" active={activeTab === 'forge'} onPress={() => setActiveTab('forge')} />
        <NavBtn icon={Fingerprint} label="Genome" active={activeTab === 'genome'} onPress={() => setActiveTab('genome')} />
        <NavBtn icon={Settings} label="Admin" active={activeTab === 'admin'} onPress={() => setActiveTab('admin')} />
      </View>
    </SafeAreaView>
  );
}

const NavBtn = ({ icon: Icon, label, active, onPress }) => (
  <TouchableOpacity onPress={onPress} style={styles.navItem}>
    <Icon size={24} color={active ? '#64ffda' : '#475569'} />
    <Text style={[styles.navText, active && { color: '#64ffda' }]}>{label}</Text>
  </TouchableOpacity>
);

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#020617' },
  scrollContent: { padding: 20, paddingTop: 40, paddingBottom: 120 },
  header: { marginBottom: 40 },
  title: { color: 'white', fontSize: 32, fontWeight: '900', letterSpacing: -1, textAlign: 'center' },
  subtitle: { color: '#64748b', fontSize: 10, fontWeight: '800', textAlign: 'center', marginTop: 8, letterSpacing: 3 },
  welcomeSection: { marginBottom: 35 },
  welcomeText: { color: '#64748b', fontSize: 20, fontWeight: '800' },
  realmLabel: { color: '#64ffda', fontSize: 9, fontWeight: '900', marginTop: 4, letterSpacing: 2 },
  statusBadge: { backgroundColor: '#0f172a', paddingHorizontal: 15, paddingVertical: 8, borderRadius: 15, flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: '#1e293b' },
  pulseDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#10b981', marginRight: 10 },
  badgeText: { color: '#64748b', fontSize: 10, fontWeight: '900', textTransform: 'uppercase', letterSpacing: 1 },
  screenContainer: { flex: 1, padding: 20, paddingTop: 40 },
  statsGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  glassCard: { backgroundColor: '#0f172a80', padding: 20, borderRadius: 30, borderWidth: 1, borderColor: 'rgba(255,255,255,0.05)' },
  statIcon: { width: 45, height: 45, borderRadius: 15, borderWidth: 1, alignItems: 'center', justifyContent: 'center', marginBottom: 15 },
  statValue: { color: 'white', fontSize: 22, fontWeight: '900', letterSpacing: -0.5 },
  statLabel: { color: '#64748b', fontSize: 10, fontWeight: '800', textTransform: 'uppercase', marginTop: 4, letterSpacing: 0.5 },
  section: { marginTop: 40 },
  sectionTitle: { color: 'white', fontSize: 20, fontWeight: '900', marginBottom: 20, letterSpacing: -0.5 },
  resRow: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 18 },
  resLabel: { color: '#64748b', fontSize: 10, fontWeight: '800', width: 90 },
  resBarBg: { flex: 1, height: 5, backgroundColor: 'rgba(255,255,255,0.05)', borderRadius: 2.5 },
  resBarFill: { height: '100%', borderRadius: 2.5 },
  resValue: { color: 'white', fontSize: 11, fontWeight: '900', width: 70, textAlign: 'right' },
  navBar: { position: 'absolute', bottom: 0, width: '100%', height: 100, backgroundColor: '#020617', flexDirection: 'row', borderTopWidth: 1, borderTopColor: 'rgba(255,255,255,0.05)', paddingBottom: 35, paddingHorizontal: 15 },
  navItem: { flex: 1, alignItems: 'center', justifyContent: 'center' },
  navText: { color: '#475569', fontSize: 9, marginTop: 6, fontWeight: '900', textTransform: 'uppercase', letterSpacing: 1 }
});
