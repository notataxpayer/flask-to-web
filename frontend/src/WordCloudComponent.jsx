import { useEffect, useState, useRef } from 'react';
import WordCloud from 'wordcloud';

const WordCloudComponent = () => {
  const [words, setWords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    fetch('http://localhost:8000/wordcloud')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        return response.json();
      })
      .then(data => {
        setWords(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    if (words.length > 0 && canvasRef.current) {
      // Clear canvas first
      const ctx = canvasRef.current.getContext('2d');
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      
      // Convert data to format needed by wordcloud library
      // Take more words and normalize values for better distribution
      const maxValue = Math.max(...words.map(w => w.value));
      const minValue = Math.min(...words.map(w => w.value));
      
      // Normalize values using log scale for better visualization
      const wordList = words.map(w => {
        // Apply log normalization to reduce gap between high and low frequency
        const normalized = Math.log(w.value + 1) / Math.log(maxValue + 1);
        const scaledValue = minValue + (normalized * (maxValue - minValue));
        return [w.text, scaledValue];
      });
      
      // Dynamic weight factor based on canvas size and max value
      const canvasArea = canvasRef.current.width * canvasRef.current.height;
      const weightFactor = (canvasArea / 50000) * (100 / maxValue);
      
      WordCloud(canvasRef.current, {
        list: wordList,
        gridSize: 8, // Smaller grid for more words
        weightFactor: weightFactor,
        fontFamily: 'Arial, sans-serif',
        color: () => {
          const colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'];
          return colors[Math.floor(Math.random() * colors.length)];
        },
        rotateRatio: 0.3,
        rotationSteps: 2,
        backgroundColor: '#ffffff',
        drawOutOfBound: false,
        shrinkToFit: true,
        minSize: 8, // Smaller minimum size
        maxRotation: Math.PI / 4,
        minRotation: -Math.PI / 4,
      });
    }
  }, [words]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading word cloud...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <p className="text-red-600 font-semibold">Error: {error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex justify-center items-center flex-1 bg-white rounded-lg shadow-md p-2 sm:p-6 overflow-hidden">
        <canvas 
          ref={canvasRef}
          className="max-w-full max-h-full"
          width={window.innerWidth < 640 ? 600 : 800}
          height={window.innerWidth < 640 ? 400 : 500}
        />
      </div>
    </div>
  );
};

export default WordCloudComponent;
