const axios = require('axios');
require('dotenv').config();

class LLMService {
  static async getPrediction(insightData) {
    if (!insightData || typeof insightData !== 'object') {
      throw new Error('Invalid input format');
    }
    
    try {
      const start = Date.now();
      // Validate and sanitize input
      const sanitizedData = {
        location: insightData.location?.slice(0, 100),
        category: insightData.category?.slice(0, 50),
        data: insightData.data ? JSON.stringify(insightData.data).slice(0, 1000) : null
      };
      const response = await axios.post(
        'https://openrouter.ai/api/v1/chat/completions',
        {
          model: "deepseek-ai/deepseek-r1",
          messages: [{
            role: "user",
            content: `Analyze cultural insights: ${JSON.stringify(insightData)}. Predict demand uplift and marketing strategies.`
          }],
          temperature: 0.7,
          max_tokens: 500
        },
        {
          headers: {
            'Authorization': `Bearer ${process.env.OPENROUTER_API_KEY}`,
            'HTTP-Referer': 'https://github.com/your-repo',
            'X-Title': 'CÆSER Retail Analytics'
          },
          timeout: 10000
        }
      );
      
      return {
        success: true,
        data: this._parseResponse(response.data),
        latency: Date.now() - start
      };
    } catch (error) {
      console.error('OpenRouter API Error:', error.response?.data || error.message);
      return {
        success: false,
        data: null,
        message: error.response?.data?.error?.message || 'AI prediction failed'
      };
    }
  }

  static _parseResponse(response) {
    try {
      const content = response.choices[0].message.content;
      return {
        prediction: content.match(/Prediction:\s*(.+)/)?.[1] || 'No prediction',
        strategy: content.match(/Strategy:\s*(.+)/)?.[1] || 'No strategy',
        confidence: parseFloat(content.match(/Confidence:\s*([0-9.]+)/)?.[1]) || 0
      };
    } catch (e) {
      throw new Error('Failed to parse LLM response');
    }
  }
}

module.exports = LLMService;