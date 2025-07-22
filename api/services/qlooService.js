import axios from 'axios';
import { config } from 'dotenv';
import { CircuitBreaker } from '../utils/circuitBreaker';
import retry from 'async-retry';

config(); // Load environment variables

class QlooService {
  // Fetches cultural insights for a given location and category.
  // @param {String} location - The location for the cultural insights (e.g., "New York").
  // @param {String} category - The category for the cultural insights (e.g., "music").
  // @returns {Object} An object with success (boolean), data (any), and message (string).
  static async getCulturalInsights(location, category) {
    if (!process.env.QLOO_API_KEY) throw new Error('QLOO_API_KEY not configured');
    if (typeof location !== 'string' || location.length === 0) throw new Error('Invalid location');
    if (typeof category !== 'string' || category.length === 0) throw new Error('Invalid category');

    const circuitBreaker = new CircuitBreaker({ failureThreshold: 3, successThreshold: 2, timeout: 15000 });
    console.log(`[Qloo API Request] Location: ${location}, Category: ${category}, Timestamp: ${new Date().toISOString()}`);

    return circuitBreaker.callService(async () => {
      return retry(async () => {
        const response = await axios.get('https://hackathon.api.qloo.com/v2/insights', {
          headers: { 'X-API-KEY': process.env.QLOO_API_KEY, 'Content-Type': 'application/json' },
          params: {
            'filter.type': 'urn:entity:product',
            'signal.location.query': location,
            'filter.tags': category
          },
          timeout: 5000
        });
        return { success: true, data: response.data, message: 'Success' };
      }, {
        retries: 3,
        factor: 2,
        minTimeout: 1000,
        maxTimeout: 5000,
        onRetry: (err) => console.log(`Retrying Qloo API call: ${err.message}`)
      });
    });
  }
}

export default QlooService;