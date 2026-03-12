const axios = require('axios');

const ALQURAN_BASE_URL = 'https://api.alquran.cloud/v1';
const EVERYAYAH_BASE_URL = 'https://everyayah.com/data/Alafasy_128kbps';

const quranService = {
    getSurahs: async () => {
        const response = await axios.get(`${ALQURAN_BASE_URL}/surah`);
        return response.data.data;
    },

    getAyah: async (surahNumber, ayahNumber, edition = 'en.sahih') => {
        const response = await axios.get(`${ALQURAN_BASE_URL}/ayah/${surahNumber}:${ayahNumber}/editions/quran-uthmani,${edition}`);
        return response.data.data;
    },

    getSurah: async (surahNumber, edition = 'en.sahih') => {
        const response = await axios.get(`${ALQURAN_BASE_URL}/surah/${surahNumber}/editions/quran-uthmani,${edition}`);
        return response.data.data;
    },

    getAudioUrl: (surahNumber, ayahNumber) => {
        // Pads numbers to 3 digits (e.g., 1 -> 001)
        const s = surahNumber.toString().padStart(3, '0');
        const a = ayahNumber.toString().padStart(3, '0');
        return `${EVERYAYAH_BASE_URL}/${s}${a}.mp3`;
    }
};

module.exports = quranService;
