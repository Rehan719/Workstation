import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, TextInput, ActivityIndicator } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Brain, Book, Shield, Zap, Search, Play } from 'lucide-react-native';

const API_BASE = "http://127.0.0.1:8000/api/v1";

export default function App() {
  const [view, setView] = useState('dashboard');
  const [status, setStatus] = useState(null);
  const [quranData, setQuranData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState('1:1');

  useEffect(() => {
    fetchStatus();
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await fetch(`${API_BASE}/status`);
      const data = await res.json();
      setStatus(data);
    } catch (e) {
      console.log("Backend offline");
    }
  };

  const fetchAyah = async (ref) => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/qep/ayah/${ref}`);
      const data = await res.json();
      setQuranData(data);
    } catch (e) {
      alert("Error fetching Ayah");
    }
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" />

      <View style={styles.header}>
        <Text style={styles.logo}>JULES AI v120.0</Text>
        <Shield color="#0070f3" size={24} />
      </View>

      <View style={styles.tabs}>
        <TouchableOpacity onPress={() => setView('dashboard')} style={[styles.tab, view === 'dashboard' && styles.activeTab]}>
            <Text style={[styles.tabText, view === 'dashboard' && styles.activeTabText]}>System</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setView('qep')} style={[styles.tab, view === 'qep' && styles.activeTab]}>
            <Text style={[styles.tabText, view === 'qep' && styles.activeTabText]}>QEP</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        {view === 'dashboard' ? (
          <>
            <View style={styles.hero}>
              <Text style={styles.heroTitle}>Apotheosis of Synergy</Text>
              <Text style={styles.heroSubtitle}>Digital Twin Ecosystem v120.0</Text>
            </View>

            <View style={styles.statsGrid}>
              <View style={styles.statCard}>
                <Text style={styles.statLabel}>Synergy</Text>
                <Text style={styles.statValue}>99.9%</Text>
              </View>
              <View style={styles.statCard}>
                <Text style={styles.statLabel}>Fidelity</Text>
                <Text style={styles.statValue}>{status?.fidelity * 100 || 99.5}%</Text>
              </View>
            </View>

            <Text style={styles.sectionTitle}>Business Governance</Text>
            {status?.governance?.okr_progress.map((okr, i) => (
                <View key={i} style={styles.okrCard}>
                    <Text style={styles.okrTitle}>{okr.objective}</Text>
                    <View style={styles.progressBar}>
                        <View style={[styles.progressFill, { width: `${okr.completion * 100}%` }]} />
                    </View>
                </View>
            ))}
          </>
        ) : (
          <>
            <Text style={styles.heroTitle}>Quranic Education</Text>
            <View style={styles.searchBar}>
                <TextInput
                    style={styles.input}
                    placeholder="Enter reference (1:1)"
                    placeholderTextColor="#666"
                    value={search}
                    onChangeText={setSearch}
                />
                <TouchableOpacity onPress={() => fetchAyah(search)} style={styles.searchBtn}>
                    <Search color="white" size={20} />
                </TouchableOpacity>
            </View>

            {loading ? <ActivityIndicator size="large" color="#0070f3" /> : (
                quranData && (
                    <View style={styles.ayahCard}>
                        <Text style={styles.arabicText}>{quranData.arabic}</Text>
                        <Text style={styles.translationText}>"{quranData.translation}"</Text>
                        <View style={styles.ayahFooter}>
                            <Text style={styles.refText}>Surah {quranData.surah}, Ayah {quranData.ayah}</Text>
                            <TouchableOpacity style={styles.playBtn}>
                                <Play color="white" size={16} fill="white" />
                            </TouchableOpacity>
                        </View>
                    </View>
                )
            )}
          </>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#000', paddingTop: 50 },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 20, marginBottom: 10 },
  logo: { color: '#fff', fontSize: 18, fontWeight: '900', letterSpacing: -1 },
  tabs: { flexDirection: 'row', paddingHorizontal: 20, marginBottom: 20, gap: 10 },
  tab: { paddingVertical: 8, paddingHorizontal: 16, borderRadius: 20, backgroundColor: '#111' },
  activeTab: { backgroundColor: '#0070f3' },
  tabText: { color: '#666', fontWeight: 'bold' },
  activeTabText: { color: '#fff' },
  content: { flex: 1, paddingHorizontal: 20 },
  hero: { marginBottom: 30 },
  heroTitle: { color: '#fff', fontSize: 32, fontWeight: '900', marginBottom: 4 },
  heroSubtitle: { color: '#666', fontSize: 16 },
  statsGrid: { flexDirection: 'row', gap: 15, marginBottom: 30 },
  statCard: { flex: 1, backgroundColor: '#111', padding: 20, borderRadius: 16, borderWidth: 1, borderColor: '#222' },
  statLabel: { color: '#999', fontSize: 10, fontWeight: '700', textTransform: 'uppercase', marginBottom: 4 },
  statValue: { color: '#fff', fontSize: 24, fontWeight: '900' },
  sectionTitle: { color: '#fff', fontSize: 18, fontWeight: '800', marginBottom: 15 },
  okrCard: { backgroundColor: '#111', padding: 15, borderRadius: 12, marginBottom: 10 },
  okrTitle: { color: '#fff', fontSize: 14, marginBottom: 8 },
  progressBar: { height: 4, backgroundColor: '#222', borderRadius: 2, overflow: 'hidden' },
  progressFill: { height: '100%', backgroundColor: '#0070f3' },
  searchBar: { flexDirection: 'row', gap: 10, marginBottom: 20 },
  input: { flex: 1, backgroundColor: '#111', color: '#fff', padding: 12, borderRadius: 10, borderWidth: 1, borderColor: '#222' },
  searchBtn: { backgroundColor: '#0070f3', width: 50, height: 50, borderRadius: 10, justifyContent: 'center', alignItems: 'center' },
  ayahCard: { backgroundColor: '#111', padding: 20, borderRadius: 20, borderWidth: 1, borderColor: '#222' },
  arabicText: { color: '#fff', fontSize: 24, textAlign: 'right', lineHeight: 40, marginBottom: 20 },
  translationText: { color: '#999', fontSize: 16, fontStyle: 'italic', lineHeight: 24, marginBottom: 20 },
  ayahFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  refText: { color: '#666', fontSize: 12 },
  playBtn: { backgroundColor: '#0070f3', width: 32, height: 32, borderRadius: 16, justifyContent: 'center', alignItems: 'center' }
});
