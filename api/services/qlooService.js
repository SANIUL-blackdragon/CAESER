const mockCulturalInsights = {
  'sneakers': {
    'NYC': {
      affinity_score: 85,
      trending_brands: ['Nike', 'Adidas', 'New Balance'],
      popular_styles: ['Retro', 'Limited Edition', 'Collaborations']
    }
  }
};

class QlooService {
  static async getCulturalInsights(location, category) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const data = mockCulturalInsights[category]?.[location] || null;
        resolve({
          success: data !== null,
          data,
          message: data ? 'Success' : 'No data available'
        });
      }, 500); // Simulate network delay
    });
  }
}

module.exports = QlooService;