import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, Dimensions } from 'react-native';
import Animated, { useSharedValue, useAnimatedStyle, withRepeat, withTiming, withSequence } from 'react-native-reanimated';

const { width } = Dimensions.get('window');

const SystemPulse = () => {
  const scale = useSharedValue(1);
  const opacity = useSharedValue(0.5);

  useEffect(() => {
    scale.value = withRepeat(withTiming(1.5, { duration: 2000 }), -1, true);
    opacity.value = withRepeat(withTiming(0.2, { duration: 2000 }), -1, true);
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  return (
    <View style={styles.pulseContainer}>
      <Animated.View style={[styles.pulseCircle, animatedStyle]} />
      <View style={styles.innerCircle}>
        <Text style={styles.pulseText}>99.8</Text>
      </View>
    </View>
  );
};

const DashboardCard = ({ title, value, subtext, color = '#38bdf8' }) => (
  <View style={styles.card}>
    <Text style={styles.cardLabel}>{title}</Text>
    <Text style={styles.cardValue}>{value}</Text>
    <Text style={[styles.cardSubtext, { color }]}>{subtext}</Text>
  </View>
);

export default function App() {
  const [data, setData] = useState({ balance: 0, depth: "1.4M", fidelity: 99.8 });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const API_BASE = "https://workstation-anwa.onrender.com/api/v1";
        const USER_ID = "demo_user";

        const tokenRes = await fetch(`${API_BASE}/tokens/ledger/${USER_ID}`);
        const tokens = await tokenRes.json();

        const knowledgeRes = await fetch(`${API_BASE}/knowledge/summary`);
        const knowledge = await knowledgeRes.json();

        setData({
          balance: tokens.balance,
          depth: (knowledge.graph_depth / 1000000).toFixed(1) + "M",
          fidelity: 99.8
        });
      } catch (err) {
        console.error("Mobile Sync Failed", err);
      }
    };

    const interval = setInterval(fetchData, 10000);
    fetchData();
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <Text style={styles.title}>JULES AI v128.0</Text>
          <Text style={styles.subtitle}>Sovereign Integrity & Universal Completion</Text>
        </View>

        <SystemPulse />

        <View style={styles.statsGrid}>
          <DashboardCard title="Active Swarms" value="24" subtext="↑ 4 increased" color="#10b981" />
          <DashboardCard title="Signals/hr" value="256K" subtext="Gating: ON" />
          <DashboardCard title="UEG Nodes" value={data.depth} subtext="100% Synced" />
          <DashboardCard title="WST Tokens" value={(data.balance / 1000).toFixed(1) + "K"} subtext="Tier: SOVEREIGN" color="#fbbf24" />
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>v128.0 System Resonance</Text>
          <View style={styles.biomimeticRow}>
            <View style={styles.biomimeticItem}>
               <Text style={styles.biomimeticLabel}>Rectification</Text>
               <Text style={styles.biomimeticValue}>96% Eff.</Text>
            </View>
            <View style={styles.biomimeticItem}>
               <Text style={styles.biomimeticLabel}>Synaptic</Text>
               <Text style={styles.biomimeticValue}>0.38ms</Text>
            </View>
            <View style={styles.biomimeticItem}>
               <Text style={styles.biomimeticLabel}>Molecular</Text>
               <Text style={styles.biomimeticValue}>1.4K ev/s</Text>
            </View>
            <View style={styles.biomimeticItem}>
               <Text style={styles.biomimeticLabel}>Cognitive</Text>
               <Text style={styles.biomimeticValue}>82% Trends</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>QEP Analytics</Text>
          <View style={styles.qepRow}>
            <Text style={styles.qepText}>Morphology Hit: 99.9%</Text>
            <Text style={styles.qepText}>Quiz Accuracy: 98%</Text>
            <Text style={styles.qepText}>Scholar Trust: 0.992 OXY</Text>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Governance & Sovereign Risk</Text>
          <View style={styles.govRow}>
            <View style={styles.govItem}>
              <Text style={styles.govLabel}>ARI</Text>
              <Text style={[styles.govValue, { color: '#10b981' }]}>0.04</Text>
            </View>
            <View style={styles.govItem}>
              <Text style={styles.govLabel}>ATS</Text>
              <Text style={styles.govValue}>v2.0.0</Text>
            </View>
            <View style={styles.govItem}>
              <Text style={styles.govLabel}>Compliance</Text>
              <Text style={styles.govValue}>100%</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Global Impact & Marketplace</Text>
          <View style={styles.impactCard}>
             <Text style={styles.impactText}>Revenue: 52,400 WST</Text>
             <Text style={styles.impactText}>Partnerships: 12 Active</Text>
             <Text style={styles.impactText}>Scholars: 108 Verified</Text>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Pending Approvals</Text>
          <View style={styles.approvalItem}>
            <Text style={styles.approvalTitle}>v128.1-Alpha Evolution</Text>
            <Text style={styles.approvalDesc}>Proposed blueprint for autonomous ecosystem expansion.</Text>
            <View style={styles.buttonRow}>
              <TouchableOpacity style={styles.approveButton}>
                <Text style={styles.buttonText}>APPROVE</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.vetoButton}>
                <Text style={styles.buttonText}>VETO</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </ScrollView>

      <View style={styles.navBar}>
        <TouchableOpacity style={styles.navItem}><Text style={styles.navTextActive}>Dashboard</Text></TouchableOpacity>
        <TouchableOpacity style={styles.navItem}><Text style={styles.navText}>Reactors</Text></TouchableOpacity>
        <TouchableOpacity style={styles.navItem}><Text style={styles.navText}>Knowledge</Text></TouchableOpacity>
        <TouchableOpacity style={styles.navItem}><Text style={styles.navText}>Profile</Text></TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#020617',
  },
  qepRow: {
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.1)',
  },
  qepText: {
    color: '#38bdf8',
    fontSize: 12,
    marginBottom: 4,
  },
  govRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.08)',
  },
  govItem: {
    alignItems: 'center',
  },
  govLabel: {
    color: '#64748b',
    fontSize: 10,
    textTransform: 'uppercase',
  },
  govValue: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  impactCard: {
    backgroundColor: 'rgba(251, 191, 36, 0.05)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(251, 191, 36, 0.2)',
  },
  impactText: {
    color: '#fbbf24',
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  biomimeticRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: 'rgba(56, 189, 248, 0.05)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.1)',
  },
  biomimeticItem: {
    alignItems: 'center',
  },
  biomimeticLabel: {
    color: '#64748b',
    fontSize: 10,
    textTransform: 'uppercase',
    marginBottom: 4,
  },
  biomimeticValue: {
    color: '#38bdf8',
    fontSize: 14,
    fontWeight: 'bold',
  },
  scrollContent: {
    padding: 20,
    paddingTop: 60,
    paddingBottom: 100,
  },
  header: {
    marginBottom: 40,
  },
  title: {
    color: '#38bdf8',
    fontSize: 24,
    fontWeight: '900',
    letterSpacing: 2,
  },
  subtitle: {
    color: '#64748b',
    fontSize: 14,
  },
  pulseContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    height: 200,
    marginBottom: 40,
  },
  pulseCircle: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#38bdf8',
    position: 'absolute',
  },
  innerCircle: {
    width: 80,
    height: 80,
    borderRadius: 40,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.5)',
    backgroundColor: '#020617',
    alignItems: 'center',
    justifyContent: 'center',
  },
  pulseText: {
    color: '#38bdf8',
    fontSize: 20,
    fontWeight: 'bold',
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  card: {
    width: (width - 60) / 2,
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: 'rgba(255, 255, 255, 0.08)',
  },
  cardLabel: {
    color: '#64748b',
    fontSize: 12,
    marginBottom: 4,
  },
  cardValue: {
    color: 'white',
    fontSize: 20,
    fontWeight: 'bold',
  },
  cardSubtext: {
    fontSize: 10,
    marginTop: 4,
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  approvalItem: {
    backgroundColor: 'rgba(255, 255, 255, 0.03)',
    borderRadius: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: 'rgba(56, 189, 248, 0.2)',
  },
  approvalTitle: {
    color: 'white',
    fontWeight: 'bold',
    marginBottom: 4,
  },
  approvalDesc: {
    color: '#64748b',
    fontSize: 12,
    marginBottom: 16,
  },
  buttonRow: {
    flexDirection: 'row',
    gap: 10,
  },
  approveButton: {
    flex: 2,
    backgroundColor: '#38bdf8',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  vetoButton: {
    flex: 1,
    backgroundColor: 'rgba(255, 255, 255, 0.05)',
    padding: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: 'bold',
  },
  navBar: {
    position: 'absolute',
    bottom: 0,
    width: '100%',
    height: 80,
    backgroundColor: 'rgba(2, 6, 23, 0.95)',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    borderTopWidth: 1,
    borderTopColor: 'rgba(255, 255, 255, 0.08)',
  },
  navText: {
    color: '#64748b',
    fontSize: 12,
  },
  navTextActive: {
    color: '#38bdf8',
    fontSize: 12,
    fontWeight: 'bold',
  }
});
