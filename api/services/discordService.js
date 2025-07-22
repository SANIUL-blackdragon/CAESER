const axios = require('axios');
require('dotenv').config();

class DiscordService {
  constructor() {
    this.webhookUrl = process.env.DISCORD_WEBHOOK_URL;
  }

  async sendAlert(prediction, insights) {
    if (!this.webhookUrl) {
      console.warn('No Discord webhook configured');
      return;
    }

    const embed = {
      title: 'New Prediction Alert',
      fields: [
        { name: 'Product', value: prediction.product || 'Unknown' },
        { name: 'Demand Uplift', value: prediction.uplift || 'Unknown' },
        { name: 'Recommended Strategy', value: prediction.strategy || 'Unknown' },
        { name: 'Average Hype Score', value: insights?.averageScore?.toFixed(2) || 'Unknown' }
      ],
      timestamp: new Date().toISOString()
    };

    try {
      await axios.post(this.webhookUrl, {
        embeds: [embed]
      });
    } catch (error) {
      console.error('Failed to send Discord alert:', error.message);
    }
  }
}

module.exports = new DiscordService();