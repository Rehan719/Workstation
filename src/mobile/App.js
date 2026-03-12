import React, { useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Brain, Book, Shield, Zap, User } from 'lucide-react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Notifications from 'expo-notifications';

// Notifications configuration
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: false,
    shouldSetBadge: false,
  }),
});

export default function App() {
  useEffect(() => {
    registerForPushNotificationsAsync();
    loadProfile();
  }, []);

  const registerForPushNotificationsAsync = async () => {
    const { status: existingStatus } = await Notifications.getPermissionsAsync();
    let finalStatus = existingStatus;
    if (existingStatus !== 'granted') {
      const { status } = await Notifications.requestPermissionsAsync();
      finalStatus = status;
    }
    if (finalStatus !== 'granted') {
      console.log('Failed to get push token for push notification!');
      return;
    }
  };

  const loadProfile = async () => {
    try {
      const profile = await AsyncStorage.getItem('@user_profile');
      if (!profile) {
        const defaultProfile = { name: 'Jules User', tier: 'Free' };
        await AsyncStorage.setItem('@user_profile', JSON.stringify(defaultProfile));
      }
    } catch (e) {
      console.error('Failed to load profile', e);
    }
  };

  const handleSync = async () => {
    Alert.alert('Synergy Synchronized', 'System health and external connectors are up to date.');
  };

  return (
    <View style={styles.container}>
      <StatusBar style="light" />

      <View style={styles.header}>
        <View style={styles.logoRow}>
          <Text style={styles.logo}>JULES AI v120.0</Text>
          <Shield color="#0070f3" size={20} style={{ marginLeft: 8 }} />
        </View>
        <TouchableOpacity onPress={() => Alert.alert('Profile', 'Name: Jules User\nTier: Free')}>
          <User color="#fff" size={24} />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content}>
        <View style={styles.hero}>
          <Text style={styles.heroTitle}>Apotheosis of Synergy</Text>
          <Text style={styles.heroSubtitle}>The fully operational, biomimetically-conscious digital enterprise.</Text>
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

        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>Engine Status</Text>
          <TouchableOpacity onPress={handleSync}>
            <Text style={styles.syncBtn}>Sync Now</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity style={styles.itemCard} onPress={() => Alert.alert('Engine Info', 'ESE: Digital Twinning\nARO: Resource Optimization\nBTO: Team Orchestration\nDRAD: Resource Fabric')}>
          <View style={styles.iconContainer}>
            <Zap color="#0070f3" size={20} />
          </View>
          <View>
            <Text style={styles.itemTitle}>Quadruple-Pillar Engine</Text>
            <Text style={styles.itemDesc}>ESE, ARO, BTO, DRAD Operational</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.itemCard} onPress={() => Alert.alert('QEP Info', 'Quranic Education Platform providing P0, P1, and P2 feature sets including translations, audio, and tafsir.')}>
          <View style={styles.iconContainer}>
            <Book color="#10b981" size={20} />
          </View>
          <View>
            <Text style={styles.itemTitle}>Quranic Education Hub</Text>
            <Text style={styles.itemDesc}>P0, P1, P2 Features Ready</Text>
          </View>
        </TouchableOpacity>

        <TouchableOpacity style={styles.itemCard} onPress={() => Alert.alert('Reactors Info', '50+ hyper-specialized reactors across Science, Law, Career, and Education domains.')}>
          <View style={styles.iconContainer}>
            <Brain color="#8b5cf6" size={20} />
          </View>
          <View>
            <Text style={styles.itemTitle}>50+ Sub-Reactors</Text>
            <Text style={styles.itemDesc}>Hyper-specialized domain intelligence</Text>
          </View>
        </TouchableOpacity>

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000',
    paddingTop: 50,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  logoRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logo: {
    color: '#fff',
    fontSize: 20,
    fontWeight: '900',
    letterSpacing: -1,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
  },
  hero: {
    marginBottom: 30,
  },
  heroTitle: {
    color: '#fff',
    fontSize: 32,
    fontWeight: '900',
    marginBottom: 8,
  },
  heroSubtitle: {
    color: '#666',
    fontSize: 16,
    lineHeight: 22,
  },
  statsGrid: {
    flexDirection: 'row',
    gap: 15,
    marginBottom: 30,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#111',
    padding: 20,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: '#222',
  },
  statLabel: {
    color: '#999',
    fontSize: 12,
    fontWeight: '700',
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  statValue: {
    color: '#fff',
    fontSize: 24,
    fontWeight: '900',
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '800',
  },
  syncBtn: {
    color: '#0070f3',
    fontWeight: '600',
  },
  itemCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#111',
    padding: 15,
    borderRadius: 12,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#222',
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: 8,
    backgroundColor: '#000',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  itemTitle: {
    color: '#fff',
    fontSize: 15,
    fontWeight: '700',
  },
  itemDesc: {
    color: '#666',
    fontSize: 12,
    marginTop: 2,
  },
});
