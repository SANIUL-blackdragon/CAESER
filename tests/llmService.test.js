const llmService = require('../api/services/llmService');
const { OpenRouter } = require('langchain/llms/openrouter');

jest.mock('langchain/llms/openrouter');

describe('LLMService', () => {
  beforeEach(() => {
    OpenRouter.mockClear();
    process.env.OPENROUTER_API_KEY = 'test_key';
  });

  it('should process LLM response correctly', async () => {
    const mockResponse = "Demand uplift: 25%\nStrategy: Social media campaign";
    OpenRouter.prototype.call.mockResolvedValue(mockResponse);

    const result = await llmService.getPrediction('Test Product', {});
    expect(result).toEqual({
      uplift: "Demand uplift: 25%",
      strategy: "Strategy: Social media campaign"
    });
  });

  it('should handle circuit breaker failures', async () => {
    OpenRouter.prototype.call.mockRejectedValue(new Error('API failed'));
    
    try {
      await llmService.getPrediction('Test', {});
      await llmService.getPrediction('Test', {});
      await llmService.getPrediction('Test', {});
      fail('Should have thrown');
    } catch (err) {
      expect(err.message).toContain('Service unavailable');
    }
  });
});