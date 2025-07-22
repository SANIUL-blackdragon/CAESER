import axios from 'axios';
import { config } from 'dotenv';
import { CircuitBreaker } from '../utils/circuitBreaker';
import retry from 'async-retry';

config();

class QlooService {
  /**
   * Fetches cultural insights for a given location and category.
   * @param {string} location - The location for insights (e.g., "New York, NY").
   * @param {string} category - The category for insights (e.g., "music").
   * @returns {Promise<{ success: boolean, data: any, message: string }>} Response object.
   * @throws {Error} If inputs are invalid or API key is missing.
   */
  static async getCulturalInsights(location, category) {
    const sanitize = (str) => str.trim().replace(/[^\w\s,.-]/gi, '');

    // Consolidated validation
    if (!process.env.QLOO_API_KEY) throw new Error('QLOO_API_KEY not configured');
    if (!location || typeof location !== 'string' || location.trim().length === 0) {
      throw new Error('Invalid location');
    }
    if (!category || typeof category !== 'string' || category.trim().length === 0) {
      throw new Error('Invalid category');
    }

    location = sanitize(location);
    category = sanitize(category);

    const logger = console; // Replace with proper logger in production
    logger.info(`[Qloo API Request] Location: ${location}, Category: ${category}, Timestamp: ${new Date().toISOString()}`);

    const circuitBreaker = new CircuitBreaker({ failureThreshold: 3, successThreshold: 2, timeout: 15000 });

    return circuitBreaker.callService(async () => {
      return retry(
        async () => {
          try {
            const response = await axios.get('https://hackathon.api.qloo.com/v2/insights', {
              headers: { 'X-API-KEY': process.env.QLOO_API_KEY, 'Content-Type': 'application/json' },
              params: { 'filter.type': 'urn:entity:product', 'signal.location.query': location, 'filter.tags': category },
              timeout: 5000,
            });

            if (!response.data || typeof response.data !== 'object' || !response.data.success) {
              throw new Error('API returned invalid or unsuccessful response');
            }

            return { success: true, data: response.data, message: 'Success' };
          } catch (error) {
            logger.error(`Qloo API Error: ${error.message}`);
            if (error.response && [429, 503].includes(error.response.status)) {
              throw error; // Retryable
            }
            return { success: false, data: null, message: error.message };
          }
        },
        {
          retries: 3,
          factor: 2,
          minTimeout: 1000,
          maxTimeout: 5000,
          onRetry: (err) => logger.info(`Retrying Qloo API call: ${err.message}`),
        }
      );
    }).catch(() => ({
      success: false,
      data: null,
      message: 'Service unavailable due to circuit breaker',
    }));
  }
}

export default QlooService;