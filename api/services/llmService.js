const { OpenRouter } = require('langchain/llms/openrouter');
const { CircuitBreaker } = require('../utils/circuitBreaker');
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
  }

  async getPrediction(product, insights) {
    const prompt = this._generatePrompt(product, insights);
    return this.circuitBreaker.callService(() =>
      this.llm.call(prompt)
        .then(response => this._processResponse(response))
    );
  }

  _generatePrompt(product, insights) {
    return `Given the product '${product}' and cultural insights ${JSON.stringify(insights)},
    predict demand uplift as a percentage and suggest a marketing strategy.`;
  }

  _processResponse(response) {
    const lines = response.split('\n');
    return {
      uplift: lines.find(l => l.includes('uplift')) || 'Unknown',
      strategy: lines.find(l => l.includes('strategy')) || 'Unknown'
    };
  }
}

module.exports = new LLMService();