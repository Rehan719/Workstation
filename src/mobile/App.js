import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Alert, SafeAreaView, Animated, Dimensions } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Brain, Book, Shield, Zap, User, Activity, Layout, Search, Settings, ChevronRight } from 'lucide-react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Notifications from 'expo-notifications';

const { width } = Dimensions.get('window');

// Notifications configuration
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

export default function App() {
  const [activeTab, setActiveTab] = useState('Dashboard');
  const [fadeAnim] = useState(new Animated.Value(0));
  const [profile, setProfile] = useState({ name: 'Jules User', tier: 'Pro' });

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start();

    registerForPushNotificationsAsync();
    loadProfile();
  }, [activeTab]);

  const registerForPushNotificationsAsync = async () => {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
  };

  const loadProfile = async () => {
    try {
      const savedProfile = await AsyncStorage.getItem('@user_profile');
      if (savedProfile) {
        setProfile(json.parse(savedProfile));
      } else {
        await AsyncStorage.setItem('@user_profile', JSON.stringify(profile));
      }
    } catch (e) {
      console.error('Failed to load profile', e);
    }
  };

  const renderDashboard = () => (
    <Animated.View style={{ opacity: fadeAnim, flex: 1 }}>
      <ScrollView showsVerticalScrollIndicator={false} style={styles.content}>
        <View style={styles.hero}>
          <Text style={styles.heroSubtitle}>SYSTEM APOTHEOSIS</Text>
          <Text style={styles.heroTitle}>Synergy Active</Text>
          <View style={styles.statusBadge}>
            <View style={styles.statusDot} />
            <Text style={styles.statusText}>HOMEOSTATIC | ALIGNMENT: 1.0</Text>
          </View>
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

        <Text style={styles.sectionTitle}>Engine Orchestration</Text>
        <View style={styles.engineCard}>
          <View style={styles.engineHeader}>
            <Zap color="#0070f3" size={24} />
            <Text style={styles.engineTitle}>Quadruple-Pillar</Text>
          </View>
          <View style={styles.engineRow}>
            <View style={styles.engineIndicator}><Text style={styles.engineLabel}>ESE</Text></View>
            <View style={styles.engineIndicator}><Text style={styles.engineLabel}>ARO</Text></View>
            <View style={styles.engineIndicator}><Text style={styles.engineLabel}>BTO</Text></View>
            <View style={styles.engineIndicator}><Text style={styles.engineLabel}>DRAD</Text></View>
          </View>
          <Text style={styles.engineDesc}>Zero-placeholder autonomous synthesis active.</Text>
        </View>

        <Text style={styles.sectionTitle}>Recent Activity</Text>
        <View style={styles.activityItem}>
          <Activity color="#10b981" size={16} />
          <Text style={styles.activityText}>Quranic Studies Reactor synced with AlQuran Cloud API</Text>
        </View>
        <View style={styles.activityItem}>
          <Shield color="#0070f3" size={16} />
          <Text style={styles.activityText}>Biomimetic Fidelity Audit: 99.8% Compliance</Text>
        </View>
      </ScrollView>
    </Animated.View>
  );

  const renderReactors = () => (
    <Animated.View style={{ opacity: fadeAnim, flex: 1, paddingHorizontal: 20 }}>
      <Text style={styles.pageTitle}>Reactor Constellations</Text>
      <ScrollView showsVerticalScrollIndicator={false}>
        {['Scientific Research', 'Religious Scholarship', 'Legal Mastery', 'Career Development', 'Education'].map((domain) => (
          <TouchableOpacity key={domain} style={styles.reactorItem} onPress={() => Alert.alert(domain, `10 specialized sub-reactors active in the ${domain} constellation.`)}>
            <View style={styles.reactorIcon}>
              {domain === 'Religious Scholarship' ? <Book color="#10b981" size={24} /> : <Brain color="#0070f3" size={24} />}
            </View>
            <View style={{ flex: 1, marginLeft: 15 }}>
              <Text style={styles.reactorTitle}>{domain}</Text>
              <Text style={styles.reactorCount}>10 Sub-reactors</Text>
            </View>
            <ChevronRight color="#333" size={20} />
          </TouchableOpacity>
        ))}
      </ScrollView>
    </Animated.View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" />

      <View style={styles.header}>
        <View style={styles.logoRow}>
          <Text style={styles.logo}>JULES AI</Text>
          <Text style={styles.version}>v∞.0</Text>
        </View>
        <TouchableOpacity style={styles.profileBtn}>
          <User color="#fff" size={20} />
        </TouchableOpacity>
      </View>

      <View style={{ flex: 1 }}>
        {activeTab === 'Dashboard' ? renderDashboard() : renderReactors()}
      </View>

      <View style={styles.tabBar}>
        <TouchableOpacity style={styles.tabItem} onPress={() => setActiveTab('Dashboard')}>
          <Layout color={activeTab === 'Dashboard' ? '#0070f3' : '#666'} size={24} />
          <Text style={[styles.tabLabel, { color: activeTab === 'Dashboard' ? '#0070f3' : '#666' }]}>App</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.tabItem} onPress={() => setActiveTab('Reactors')}>
          <Search color={activeTab === 'Reactors' ? '#0070f3' : '#666'} size={24} />
          <Text style={[styles.tabLabel, { color: activeTab === 'Reactors' ? '#0070f3' : '#666' }]}>Reactors</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.tabItem} onPress={() => Alert.alert('Settings', 'v120.0 Command Center Settings')}>
          <Settings color="#666" size={24} />
          <Text style={styles.tabLabel}>Settings</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#050505',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#111',
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  logo: {
    color: '#fff',
    fontSize: 22,
    fontWeight: '900',
    letterSpacing: -1,
  },
  version: {
    color: '#0070f3',
    fontSize: 12,
    fontWeight: '700',
    marginLeft: 5,
  },
  profileBtn: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#111',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#222',
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  hero: {
    marginTop: 20,
    marginBottom: 25,
  },
  heroSubtitle: {
    color: '#0070f3',
    fontSize: 12,
    fontWeight: '800',
    letterSpacing: 2,
    marginBottom: 5,
  },
  heroTitle: {
    color: '#fff',
    fontSize: 36,
    fontWeight: '900',
    letterSpacing: -1,
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(16, 185, 129, 0.1)',
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 20,
    alignSelf: 'flex-start',
    marginTop: 10,
  },
  statusDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#10b981',
    marginRight: 6,
  },
  statusText: {
    color: '#10b981',
    fontSize: 10,
    fontWeight: '700',
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 15,
    marginBottom: 25,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#0a0a0a',
    padding: 20,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#151515',
  },
  statLabel: {
    color: '#555',
    fontSize: 10,
    fontWeight: '800',
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  statValue: {
    color: '#fff',
    fontSize: 26,
    fontWeight: '900',
  },
  sectionTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '800',
    marginBottom: 15,
  },
  engineCard: {
    backgroundColor: '#0a0a0a',
    padding: 20,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: '#151515',
    marginBottom: 25,
  },
  engineHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  engineTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
    marginLeft: 10,
  },
  engineRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  engineIndicator: {
    width: (width - 100) / 4,
    height: 35,
    backgroundColor: '#111',
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#222',
  },
  engineLabel: {
    color: '#0070f3',
    fontSize: 10,
    fontWeight: '900',
  },
  engineDesc: {
    color: '#555',
    fontSize: 12,
    fontStyle: 'italic',
  },
  activityItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#0a0a0a',
    padding: 15,
    borderRadius: 15,
    marginBottom: 10,
  },
  activityText: {
    color: '#888',
    fontSize: 12,
    marginLeft: 10,
    flex: 1,
  },
  pageTitle: {
    color: '#fff',
    fontSize: 28,
    fontWeight: '900',
    marginTop: 20,
    marginBottom: 20,
  },
  reactorItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#0a0a0a',
    padding: 18,
    borderRadius: 20,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#151515',
  },
  reactorIcon: {
    width: 50,
    height: 50,
    borderRadius: 15,
    backgroundColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#111',
  },
  reactorTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
  },
  reactorCount: {
    color: '#555',
    fontSize: 12,
    marginTop: 2,
  },
  tabBar: {
    flexDirection: 'row',
    height: 80,
    backgroundColor: '#050505',
    borderTopWidth: 1,
    borderTopColor: '#111',
    paddingBottom: 20,
  },
  tabItem: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  tabLabel: {
    fontSize: 10,
    fontWeight: '700',
    marginTop: 4,
  },
});
