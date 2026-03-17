import { useState, useEffect } from 'react';
import axios from 'axios';

interface UserPreferences {
  theme: string;
  smart_sidebar_enabled: boolean;
  priority_modules: string[];
}

interface PersonalizationData {
  recommended_modules: string[];
  reasoning: string;
}

export const usePersonalization = (userId: string = 'guardian') => {
  const [preferences, setPreferences] = useState<UserPreferences | null>(null);
  const [data, setData] = useState<PersonalizationData | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchPersonalization = async () => {
    try {
      const [prefsRes, dataRes] = await Promise.all([
        axios.get(`/api/v260/user/preferences?user_id=${userId}`),
        axios.get(`/api/v260/user/recommendations?user_id=${userId}`)
      ]);
      setPreferences(prefsRes.data);
      setData(dataRes.data);
    } catch (error) {
      console.error('Failed to fetch personalization data', error);
      // Fallback data for v146.0 POC
      setData({
        recommended_modules: ['dashboard', 'ceo', 'bto'],
        reasoning: 'Initializing intelligent symbiosis protocol.'
      });
    } finally {
      setLoading(false);
    }
  };

  const logActivity = async (action: string, module: string) => {
    try {
      await axios.post('/api/v260/user/activity', {
        action,
        target_module: module,
        user_id: userId
      });
    } catch (error) {
      console.warn('Failed to log activity', error);
    }
  };

  useEffect(() => {
    fetchPersonalization();
  }, [userId]);

  return { preferences, data, loading, logActivity, refresh: fetchPersonalization };
};
