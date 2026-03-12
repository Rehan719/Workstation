const express = require('express');
const quranService = require('../services/quranService');

const router = express.Router();

router.get('/surahs', async (req, res) => {
    try {
        const surahs = await quranService.getSurahs();
        res.json(surahs);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch surahs' });
    }
});

router.get('/ayah/:surah/:ayah', async (req, res) => {
    try {
        const { surah, ayah } = req.params;
        const data = await quranService.getAyah(surah, ayah);
        const audioUrl = quranService.getAudioUrl(surah, ayah);
        res.json({ ...data, audioUrl });
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch ayah' });
    }
});

router.get('/surah/:id', async (req, res) => {
    try {
        const { id } = req.params;
        const data = await quranService.getSurah(id);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch surah' });
    }
});

module.exports = router;
