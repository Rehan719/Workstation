import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { Play, Pause, BookOpen } from 'lucide-react-native';
import { Audio } from 'expo-av';
import axios from 'axios';

const QEPScreen = () => {
  const [ayahs, setAyahs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sound, setSound] = useState();

  useEffect(() => {
    fetchAyahs();
    return sound ? () => { sound.unloadAsync(); } : undefined;
  }, [sound]);

  const fetchAyahs = async () => {
    try {
      const res = await axios.get('https://api.alquran.cloud/v1/surah/1/editions/quran-uthmani,en.sahih');
      setAyahs(res.data.data[0].ayahs.map((a, i) => ({
        ...a,
        translation: res.data.data[1].ayahs[i].text
      })));
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  const playSound = async (surah, ayah) => {
    const url = `https://everyayah.com/data/Alafasy_128kbps/${surah.toString().padStart(3, '0')}${ayah.toString().padStart(3, '0')}.mp3`;
    const { sound } = await Audio.Sound.createAsync({ uri: url });
    setSound(sound);
    await sound.playAsync();
  };

  if (loading) return <View style={styles.centered}><ActivityIndicator size="large" color="#C9A86B" /></View>;

  return (
    <View style={styles.container}>
      <FlatList
        data={ayahs}
        keyExtractor={item => item.number.toString()}
        renderItem={({ item }) => (
          <View style={styles.ayahCard}>
            <View style={styles.header}>
              <Text style={styles.ayahNum}>1:{item.numberInSurah}</Text>
              <TouchableOpacity onPress={() => playSound(1, item.numberInSurah)}>
                <Play size={20} color="#1E2A47" />
              </TouchableOpacity>
            </View>
            <Text style={styles.quranText}>{item.text}</Text>
            <Text style={styles.translation}>{item.translation}</Text>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F8F9FA' },
  centered: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  ayahCard: { padding: 20, borderBottomWidth: 1, borderBottomColor: '#EEE', backgroundColor: '#FFF' },
  header: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 10 },
  ayahNum: { color: '#C9A86B', fontWeight: 'bold' },
  quranText: { fontSize: 24, textAlign: 'right', color: '#1E2A47', marginBottom: 10, fontFamily: 'serif' },
  translation: { fontSize: 14, color: '#666', fontStyle: 'italic' }
});

export default QEPScreen;
