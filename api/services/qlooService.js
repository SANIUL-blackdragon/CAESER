const axios = require('axios');
require('dotenv').config();

class QlooService {
  static async getCulturalInsights(location, category) {
    try {
      const response = await axios.get('https://qloo-api.com/v1/cultural_insights', {
        headers: {
          'X-API-KEY': process.env.QLOO_API_KEY,
          'Content-Type': 'application/json'
        },
        params: {
          location,
          category,
          granularity: 'city'
        },
        timeout: 5000
      });
      
      return {
        success: true,
        data: response.data,
        message: 'Success'
      };
    } catch (error) {
      console.error('Qloo API Error:', error.response?.data || error.message);
      return {
        success: false,
        data: null,
        message: error.response?.data?.error || 'Failed to fetch cultural insights'
      };
    }
  }
}

module.exports = QlooService;