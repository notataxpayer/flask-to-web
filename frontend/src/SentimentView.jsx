import { useEffect, useState } from 'react';

const SentimentView = () => {
  const [sentimentData, setSentimentData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/sentiment')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch sentiment data');
        }
        return response.json();
      })
      .then(data => {
        setSentimentData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'bg-green-100 text-green-800 border-green-300';
      case 'negative':
        return 'bg-red-100 text-red-800 border-red-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return '😊';
      case 'negative':
        return '😞';
      default:
        return '😐';
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading sentiment analysis...</p>
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

  const { total_topics, topics } = sentimentData;

  // Calculate overall sentiment statistics
  const totalPositive = topics.filter(t => t.sentiment === 'positive').length;
  const totalNegative = topics.filter(t => t.sentiment === 'negative').length;
  const totalNeutral = topics.filter(t => t.sentiment === 'neutral').length;

  return (
    <div className="h-full overflow-y-auto">
      {/* Header Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-4 mb-4 sm:mb-6">
        <div className="bg-white rounded-lg shadow-md p-3 sm:p-4 border-l-4 border-blue-500">
          <h3 className="text-gray-600 text-xs sm:text-sm font-medium">Total Topics</h3>
          <p className="text-2xl sm:text-3xl font-bold text-gray-800">{total_topics}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-3 sm:p-4 border-l-4 border-green-500">
          <h3 className="text-gray-600 text-xs sm:text-sm font-medium">Positive</h3>
          <p className="text-2xl sm:text-3xl font-bold text-green-600">{totalPositive}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-3 sm:p-4 border-l-4 border-red-500">
          <h3 className="text-gray-600 text-xs sm:text-sm font-medium">Negative</h3>
          <p className="text-2xl sm:text-3xl font-bold text-red-600">{totalNegative}</p>
        </div>
        <div className="bg-white rounded-lg shadow-md p-3 sm:p-4 border-l-4 border-gray-500">
          <h3 className="text-gray-600 text-xs sm:text-sm font-medium">Neutral</h3>
          <p className="text-2xl sm:text-3xl font-bold text-gray-600">{totalNeutral}</p>
        </div>
      </div>

      {/* Topics List */}
      <div className="space-y-3 sm:space-y-4">
        {topics.map((topic) => (
          <div key={topic.topic} className="bg-white rounded-lg shadow-md p-3 sm:p-5 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-2 sm:mb-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 sm:gap-3 mb-2">
                  <span className="text-xl sm:text-2xl">{getSentimentIcon(topic.sentiment)}</span>
                  <h3 className="text-sm sm:text-lg font-semibold text-gray-800 leading-tight">
                    Topic {topic.topic}: {topic.topic_name.split('_').slice(1, 4).join(' ') || topic.topic_name}
                  </h3>
                </div>
                <div className="flex items-center gap-2 sm:gap-3 flex-wrap">
                  <span className={`px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium border ${getSentimentColor(topic.sentiment)}`}>
                    {topic.sentiment.toUpperCase()}
                  </span>
                  <span className="text-xs sm:text-sm text-gray-600">
                    Score: <span className="font-semibold">{topic.sentiment_score}</span>
                  </span>
                  <span className="text-xs sm:text-sm text-gray-600">
                    Docs: <span className="font-semibold">{topic.count}</span>
                  </span>
                </div>
              </div>
            </div>

            {/* Sentiment Distribution */}
            <div className="mb-2 sm:mb-3">
              <div className="flex gap-2 sm:gap-4 text-xs text-gray-600 flex-wrap">
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 sm:w-3 sm:h-3 bg-green-500 rounded-full"></span>
                  Pos: {topic.sentiment_distribution.positive}
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 sm:w-3 sm:h-3 bg-red-500 rounded-full"></span>
                  Neg: {topic.sentiment_distribution.negative}
                </span>
                <span className="flex items-center gap-1">
                  <span className="w-2 h-2 sm:w-3 sm:h-3 bg-gray-500 rounded-full"></span>
                  Neu: {topic.sentiment_distribution.neutral}
                </span>
              </div>
            </div>

            {/* Sample Documents */}
            <div className="mt-2 sm:mt-3 pt-2 sm:pt-3 border-t border-gray-200">
              <p className="text-xs text-gray-500 font-medium mb-2">Sample:</p>
              <div className="space-y-1.5 sm:space-y-2">
                {topic.sample_docs.slice(0, 2).map((doc, idx) => (
                  <p key={idx} className="text-xs sm:text-sm text-gray-700 italic bg-gray-50 p-2 rounded leading-relaxed">
                    "{doc.length > 150 ? doc.substring(0, 150) + '...' : doc}"
                  </p>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SentimentView;
