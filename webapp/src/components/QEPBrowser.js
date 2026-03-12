import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Search, Play, Pause, Bookmark, BookOpen } from 'lucide-react';

const QEPBrowser = () => {
  const [surahs, setSurahs] = useState([]);
  const [selectedSurah, setSelectedSurah] = useState(1);
  const [ayahs, setAyahs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [playing, setPlaying] = useState(null);

  useEffect(() => {
    fetchSurahs();
  }, []);

  useEffect(() => {
    if (selectedSurah) fetchAyahs(selectedSurah);
  }, [selectedSurah]);

  const fetchSurahs = async () => {
    try {
      const res = await axios.get('https://api.alquran.cloud/v1/surah');
      setSurahs(res.data.data);
    } catch (err) { console.error(err); }
  };

  const fetchAyahs = async (id) => {
    setLoading(true);
    try {
      const res = await axios.get(`https://api.alquran.cloud/v1/surah/${id}/editions/quran-uthmani,en.sahih`);
      setAyahs(res.data.data[0].ayahs.map((a, i) => ({
        ...a,
        translation: res.data.data[1].ayahs[i].text
      })));
    } catch (err) { console.error(err); }
    setLoading(false);
  };

  const toggleAudio = (surahNum, ayahNum) => {
    const url = `https://everyayah.com/data/Alafasy_128kbps/${surahNum.toString().padStart(3, '0')}${ayahNum.toString().padStart(3, '0')}.mp3`;
    if (playing && playing.url === url) {
      playing.audio.pause();
      setPlaying(null);
    } else {
      if (playing) playing.audio.pause();
      const audio = new Audio(url);
      audio.play();
      setPlaying({ url, audio });
      audio.onended = () => setPlaying(null);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
      <div className="p-6 border-bottom border-gray-50 flex justify-between items-center bg-indigo-900 text-white">
        <h2 className="text-xl font-bold flex items-center"><BookOpen className="mr-2" /> Quranic Education Platform</h2>
        <select
          onChange={(e) => setSelectedSurah(e.target.value)}
          className="bg-indigo-800 text-white border-none rounded px-2 py-1 text-sm focus:ring-0"
        >
          {surahs.map(s => (
            <option key={s.number} value={s.number}>{s.number}. {s.englishName}</option>
          ))}
        </select>
      </div>

      <div className="h-[600px] overflow-y-auto p-6 space-y-8">
        {loading ? (
          <div className="flex justify-center py-20"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gold-500"></div></div>
        ) : (
          ayahs.map(ayah => (
            <div key={ayah.number} className="pb-8 border-b border-gray-50 last:border-0 group">
              <div className="flex justify-between items-start mb-4">
                <span className="text-xs font-bold text-gold-600 bg-gold-50 px-2 py-1 rounded">
                  {selectedSurah}:{ayah.numberInSurah}
                </span>
                <div className="flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button onClick={() => toggleAudio(selectedSurah, ayah.numberInSurah)} className="text-gray-400 hover:text-indigo-600">
                    {playing && playing.url.includes(`${selectedSurah.toString().padStart(3, '0')}${ayah.numberInSurah.toString().padStart(3, '0')}`) ? <Pause size={18} /> : <Play size={18} />}
                  </button>
                  <button className="text-gray-400 hover:text-gold-600"><Bookmark size={18} /></button>
                </div>
              </div>
              <p className="quran-text text-3xl leading-relaxed mb-4 text-right text-indigo-950">{ayah.text}</p>
              <p className="text-gray-600 leading-relaxed text-sm italic">{ayah.translation}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default QEPBrowser;
