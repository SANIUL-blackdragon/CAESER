const QlooService = require('../api/services/qlooService');
const { CircuitBreaker } = require('../api/utils/circuitBreaker');

jest.mock('axios');

describe('QlooService', () => {
  beforeEach(() => {
    process.env.QLOO_API_KEY = 'test_key';
    jest.clearAllMocks();
  });

  it('should return mock data when API succeeds', async () => {
    const mockData = { affinities: [0.8], trendScore: 0.9, culturalRelevance: 0.7 };
    require('axios').get.mockResolvedValue({ data: mockData });

    const result = await QlooService.getCulturalInsights('NYC', 'sneakers');
    expect(result.data).toEqual(mockData);
  });

  it('should trigger circuit breaker after failures', async () => {
    require('axios').get.mockRejectedValue(new Error('API failed'));
    
    try {
      await QlooService.getCulturalInsights('NYC', 'sneakers');
      await QlooService.getCulturalInsights('NYC', 'sneakers');
      await QlooService.getCulturalInsights('NYC', 'sneakers');
      fail('Should have thrown');
    } catch (err) {
      expect(err.message).toContain('Service unavailable');
    }
  });
});