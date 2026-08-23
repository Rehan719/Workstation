import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { Wallet, TrendingUp, ShieldCheck, Activity } from 'lucide-react-native';

const CapitalDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({
    balance: 1250000.00,
    totalDeposited: 1000000.00,
    profit: 250000.00,
    riskScore: 0.22,
    homeostasis: 'STABLE'
  });

  useEffect(() => {
    // Simulate API fetch
    const timer = setTimeout(() => setLoading(false), 1500);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#00ffcc" />
        <Text style={styles.loadingText}>Syncing with UEG...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      {/* Balance Card */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <Wallet color="#00ffcc" size={20} />
          <Text style={styles.cardTitle}>AUM BALANCE</Text>
        </View>
        <Text style={styles.balanceText}>${data.balance.toLocaleString()}</Text>
        <View style={styles.row}>
          <Text style={styles.label}>PROFIT</Text>
          <Text style={styles.profitText}>+${data.profit.toLocaleString()}</Text>
        </View>
      </View>

      {/* Metrics Row */}
      <View style={styles.metricsRow}>
        <View style={[styles.miniCard, { flex: 1 }]}>
          <ShieldCheck color="#00ffcc" size={16} />
          <Text style={styles.miniLabel}>RISK SCORE</Text>
          <Text style={styles.miniValue}>{(data.riskScore * 100).toFixed(1)}%</Text>
        </View>
        <View style={[styles.miniCard, { flex: 1, marginLeft: 10 }]}>
          <Activity color="#00ffcc" size={16} />
          <Text style={styles.miniLabel}>STATUS</Text>
          <Text style={styles.miniValue}>{data.homeostasis}</Text>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>SOVEREIGN ACTIONS</Text>
        <TouchableOpacity style={styles.actionButton}>
          <Text style={styles.actionButtonText}>DEPOSIT CAPITAL</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.actionButton, styles.withdrawButton]}>
          <Text style={styles.actionButtonText}>WITHDRAW PROFIT</Text>
        </TouchableOpacity>
      </View>

      {/* Twin Forecast Preview */}
      <View style={styles.card}>
        <View style={styles.cardHeader}>
          <TrendingUp color="#00ffcc" size={20} />
          <Text style={styles.cardTitle}>TWIN SIMULATION (7D)</Text>
        </View>
        <View style={styles.chartPlaceholder}>
          <Text style={styles.placeholderText}>HD FORECAST: +2.4% EXPECTED GROWTH</Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 15,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#050505',
  },
  loadingText: {
    color: '#00ffcc',
    marginTop: 10,
    fontSize: 16,
    fontFamily: 'monospace',
  },
  card: {
    backgroundColor: '#0f0f0f',
    borderRadius: 12,
    padding: 20,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: '#1a1a1a',
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  cardTitle: {
    color: '#888',
    fontSize: 12,
    fontWeight: 'bold',
    marginLeft: 10,
    letterSpacing: 1,
  },
  balanceText: {
    color: '#fff',
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  label: {
    color: '#666',
    fontSize: 12,
    fontWeight: 'bold',
  },
  profitText: {
    color: '#00ffcc',
    fontSize: 16,
    fontWeight: 'bold',
  },
  metricsRow: {
    flexDirection: 'row',
    marginBottom: 15,
  },
  miniCard: {
    backgroundColor: '#0f0f0f',
    borderRadius: 12,
    padding: 15,
    borderWidth: 1,
    borderColor: '#1a1a1a',
  },
  miniLabel: {
    color: '#666',
    fontSize: 10,
    fontWeight: 'bold',
    marginTop: 5,
  },
  miniValue: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 2,
  },
  section: {
    marginBottom: 20,
  },
  sectionTitle: {
    color: '#444',
    fontSize: 12,
    fontWeight: 'bold',
    marginBottom: 10,
    letterSpacing: 1,
  },
  actionButton: {
    backgroundColor: '#00ffcc',
    borderRadius: 8,
    padding: 15,
    alignItems: 'center',
    marginBottom: 10,
  },
  withdrawButton: {
    backgroundColor: 'transparent',
    borderWidth: 1,
    borderColor: '#00ffcc',
  },
  actionButtonText: {
    color: '#050505',
    fontSize: 14,
    fontWeight: 'bold',
    letterSpacing: 1,
  },
  chartPlaceholder: {
    height: 100,
    justifyContent: 'center',
    alignItems: 'center',
    borderStyle: 'dashed',
    borderWidth: 1,
    borderColor: '#333',
    borderRadius: 8,
  },
  placeholderText: {
    color: '#444',
    fontSize: 12,
    fontWeight: 'bold',
  }
});

export default CapitalDashboard;
