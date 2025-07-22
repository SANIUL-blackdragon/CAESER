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
    // Input validation
    if (!process.env.QLOO_API_KEY) {
      throw new Error('QLOO_API_KEY environment variable not configured');
    }
    if (typeof location !== 'string' || location.length === 0) {
      throw new Error('Invalid location parameter: must be a non-empty string');
    }
    if (typeof category !== 'string' || category.length === 0) {
      throw new Error('Invalid category parameter: must be a non-empty string');
    }

    const circuitBreaker = new CircuitBreaker({
      failureThreshold: 3,
      successThreshold: 2,
      timeout: 15000,
    });

    // Request logging
    console.log(`[Qloo API Request] Location: ${location}, Category: ${category}, Timestamp: ${new Date().toISOString()}`);

    return circuitBreaker.callService(async () => {
      return retry(
        // Retry callback function
        async (bail) => {
          try {
            const response = await axios.get('https://qloo-api.com/v1/cultural_insights', {
              headers: {
                'X-API-KEY': process.env.QLOO_API_KEY,
                'Content-Type': 'application/json',
              },
              params: {
                location,
                category,
                granularity: 'city',
              },
              timeout: 5000,
            });

            return {
              success: true,
              data: response.data,
              message: 'Success',
            };
          } catch (error) {
            console.error('Qloo API Error:', error.response ? error.response.data : error.message);
            const isRetryable = error.response && error.response.status >= 500;
            if (!isRetryable) {
              bail(error);
            }
            throw error;
          }
        },
        {
          retries: 3,
          factor: 2,
          minTimeout: 1000,
          maxTimeout: 5000,
          // @param {Error} err - The error that triggered the retry.
          onRetry: (err) => {
            console.log(`Retrying Qloo API call after error: ${err.message}`);
          },
        }
      );
    });
  }
}

export default QlooService;