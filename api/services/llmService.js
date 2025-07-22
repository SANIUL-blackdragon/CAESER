const { OpenRouter } = require('langchain/llms/openrouter');
const { CircuitBreaker } = require('../utils/circuitBreaker');
const NodeCache = require('node-cache');
require('dotenv').config();

class LLMService {
  constructor() {
    this.llm = new OpenRouter({
      apiKey: process.env.OPENROUTER_API_KEY,
      modelName: "deepseek-r1"
    });
    this.circuitBreaker = new CircuitBreaker({
      failureThreshold: 3,
      successThreshold: 2,
      timeout: 10000
    });
    this.cache = new NodeCache({ stdTTL: 3600 }); // Cache with 1-hour TTL
  }

  async getPrediction(product, insights) {
    const sanitize = (str) => str.trim().replace(/[^'\w\s.,-]/gi, '');
    if (typeof product !== 'string') {
      throw new Error('Product must be a string');
    }
    product = sanitize(product);
    const cacheKey = `${product}:${JSON.stringify(insights)}`;
    const cached = this.cache.get(cacheKey);
    if (cached) return cached;
    const response = await this.circuitBreaker.callService(() =>
      this.llm.call(this._generatePrompt(product, insights)).then(res => this._processResponse(res))
    );
    this.cache.set(cacheKey, response);
    return response;
  }

  _generatePrompt(product, insights) {
    return `
      You are an expert market analyst. Based on the product '${product}' and cultural insights ${JSON.stringify(insights)}, provide:
      1. Demand uplift as a percentage (e.g., "15%").
      2. A concise marketing strategy (e.g., "Target urban youth via social media").
      Example:
      - Product: Sneakers, Insights: { affinity: 0.85 }
      - Response: 20% uplift, "Leverage influencer campaigns on Instagram."
    `;
  }

  _processResponse(response) {
    const upliftMatch = response.match(/(\d+)%?\s*uplift/i);
    const strategyMatch = response.match(/strategy:\s*(.+)$/im);
    return {
      uplift: upliftMatch ? upliftMatch[1] + '%' : 'Unknown',
      strategy: strategyMatch ? strategyMatch[1] : 'Unknown'
    };
  }
}

module.exports = new LLMService();