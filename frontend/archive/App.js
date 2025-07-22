import React from 'react';
import { HypeEngine } from '../api/services/hypeEngine';
import './App.css';

function App() {
  const [hypeScore, setHypeScore] = React.useState(null);
  const [perfMetrics, setPerfMetrics] = React.useState({
    loadStart: 0,
    dataFetchTime: 0,
    renderTime: 0
  });

  React.useEffect(() => {
    const startTime = performance.now();
    setPerfMetrics(prev => ({...prev, loadStart: startTime}));

    async function loadData() {
      try {
        const fetchStart = performance.now();
        const response = await HypeEngine.simulateBuyers({
          affinities: [0.85],
          trendScore: 0.9,
          culturalRelevance: 0.8
        }, 100);
        const fetchEnd = performance.now();
        
        setHypeScore(response.metrics.averageScore);
        setPerfMetrics(prev => ({
          ...prev,
          dataFetchTime: fetchEnd - fetchStart,
          renderTime: performance.now() - startTime
        }));

        console.log('Performance Metrics:', {
          dataFetch: `${(fetchEnd - fetchStart).toFixed(2)}ms`,
          totalRender: `${(performance.now() - startTime).toFixed(2)}ms`
        });
      } catch (error) {
        console.error('Error loading hype data:', error);
      }
    }
    loadData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cultural Affinity Dashboard</h1>
        {hypeScore ? (
          <div className="hype-score">
            <h2>Current Hype Score</h2>
            <div className="score-value">{hypeScore.toFixed(2)}</div>
            <div className="score-range">(0-1 scale)</div>
          </div>
        ) : (
          <p>Loading hype data...</p>
        )}
      </header>
    </div>
  );
}

export default App;