import { useState } from 'react'
import WordCloudComponent from './WordCloudComponent'
import SentimentView from './SentimentView'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('wordcloud')

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 pb-6">
      {/* Header */}
      <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 sm:py-6">
          <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
            BERTopic Analysis
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-gray-600">
            Analisis Topik & Sentiment - Pemerintah
          </p>
        </div>
      </header>

      {/* Tab Navigation */}
      <div className="max-w-6xl mx-auto px-4 mt-4 sm:mt-6">
        <div className="flex gap-2 bg-white rounded-lg shadow-md p-1">
          <button
            onClick={() => setActiveTab('wordcloud')}
            className={`flex-1 py-2.5 sm:py-3 px-3 sm:px-4 rounded-md font-medium transition-all text-sm sm:text-base ${
              activeTab === 'wordcloud'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span className="text-lg sm:text-xl mr-1 sm:mr-2">☁️</span>
            <span className="hidden sm:inline">Word Cloud</span>
            <span className="sm:hidden">Cloud</span>
          </button>
          <button
            onClick={() => setActiveTab('sentiment')}
            className={`flex-1 py-2.5 sm:py-3 px-3 sm:px-4 rounded-md font-medium transition-all text-sm sm:text-base ${
              activeTab === 'sentiment'
                ? 'bg-blue-600 text-white shadow-md'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <span className="text-lg sm:text-xl mr-1 sm:mr-2">📊</span>
            <span className="hidden sm:inline">Sentiment Analysis</span>
            <span className="sm:hidden">Sentiment</span>
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="max-w-6xl mx-auto px-4 py-4 sm:py-6">
        <div className="bg-gray-50 rounded-lg shadow-lg p-3 sm:p-6 min-h-[400px] sm:min-h-[600px]">
          {activeTab === 'wordcloud' ? (
            <WordCloudComponent />
          ) : (
            <SentimentView />
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-4 sm:mt-8">
        <div className="max-w-6xl mx-auto px-4">
          <p className="text-center text-xs sm:text-sm text-gray-600">
            Powered by MLflow & BERTopic
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
