# BERTopic MLflow Dashboard

Dashboard visualisasi untuk analisis topik BERTopic menggunakan MLflow tracking server. Aplikasi ini menampilkan word cloud dan analisis sentimen dari hasil eksperimen BERTopic.

## 📋 Fitur

- **Word Cloud Visualization**: Visualisasi kata-kata penting dari dokumen representatif setiap topik
- **Sentiment Analysis**: Analisis sentimen per topik menggunakan lexicon Indonesia + TextBlob
- **Responsive Design**: Mobile-first design dengan TailwindCSS
- **MLflow Integration**: Otomatis mengambil data dari MLflow tracking server

## 🏗️ Struktur Proyek

```
flaskapi/
├── flaskapi.py              # Flask REST API
├── sentiment_analyzer.py    # Custom sentiment analyzer
├── requirements.txt         # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main dashboard component
│   │   ├── WordCloudComponent.jsx  # Word cloud visualization
│   │   └── SentimentView.jsx      # Sentiment analysis view
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- MLflow tracking server (sudah running di http://virtualtech.icu:5000)

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan Flask API:
```bash
python flaskapi.py
```

API akan berjalan di `http://localhost:8000`

### Frontend Setup

1. Masuk ke folder frontend:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Jalankan development server:
```bash
npm run dev
```

Frontend akan berjalan di `http://localhost:5174`

## 📡 API Endpoints

### GET /topic-info
Mengambil semua informasi topik dari MLflow

**Response:**
```json
[
  {
    "Topic": 0,
    "Count": 1797,
    "Name": "0_pemerintah_dan_co_https co",
    "Representation": "['pemerintah', 'dan', 'co', ...]",
    "Representative_Docs": "['doc1', 'doc2', ...]"
  }
]
```

### GET /wordcloud
Menghasilkan data word cloud dari Representative_Docs

**Response:**
```json
[
  {
    "text": "pemerintah",
    "value": 32
  },
  {
    "text": "pertanian",
    "value": 17
  }
]
```

**Features:**
- Ekstraksi kata dari Representative_Docs
- Filtering URL, mention, hashtag, emoji
- Stopwords removal (100+ kata Indonesia)
- Hanya kata meaningful (min 3 huruf, alphabetic only)
- Top 200 kata berdasarkan frekuensi

### GET /sentiment
Analisis sentimen per topik

**Response:**
```json
{
  "total_topics": 15,
  "topics": [
    {
      "topic": 0,
      "topic_name": "0_pemerintah_dan_co_https co",
      "count": 1797,
      "sentiment": "neutral",
      "sentiment_score": 0.123,
      "sentiment_distribution": {
        "positive": 10,
        "negative": 5,
        "neutral": 3
      },
      "sample_docs": ["doc1", "doc2", "doc3"]
    }
  ]
}
```

## 🎨 Frontend Components

### App.jsx
- Main dashboard dengan tab navigation
- Switching antara Word Cloud dan Sentiment Analysis
- Responsive layout dengan centered container (max-w-6xl)

### WordCloudComponent.jsx
- Canvas-based word cloud menggunakan `wordcloud` library
- Log normalization untuk distribusi kata yang lebih baik
- Dynamic sizing (600x400 mobile, 800x500 desktop)
- 8 warna berbeda untuk variasi visual

### SentimentView.jsx
- Grid layout untuk topic cards
- Sentiment badges (positive/negative/neutral)
- Statistics cards (total topics, avg sentiment, dll)
- Sample documents per topic

## 🛠️ Teknologi

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **MLflow**: Experiment tracking & artifact storage
- **Pandas**: Data manipulation
- **TextBlob**: Sentiment analysis (English)
- **boto3**: AWS S3 client untuk MLflow artifacts

### Frontend
- **React 19.2.0**: UI framework
- **Vite 7.2.4**: Build tool
- **TailwindCSS 3.4.0**: Styling
- **wordcloud**: Word cloud visualization

## 📊 MLflow Configuration

- **Tracking URI**: http://virtualtech.icu:5000
- **Experiment**: bertopic-pemerintah
- **Artifact Storage**: S3 (via tracking server proxy)
- **Artifact Path**: `topic_info_{run_id}.csv`

## 🔧 Konfigurasi

### Sentiment Analyzer

`sentiment_analyzer.py` menggunakan kombinasi:
- **Indonesian lexicon**: Kata positif/negatif dalam Bahasa Indonesia
- **TextBlob**: Fallback untuk teks English

Threshold:
- Positive: score > 0.05
- Negative: score < -0.05
- Neutral: -0.05 ≤ score ≤ 0.05

### Word Cloud Filtering

Stopwords mencakup:
- Kata sambung (yang, dan, atau, dll)
- Preposisi (di, ke, dari, dll)
- Pronoun (ini, itu, saya, dll)
- Auxiliary verbs (adalah, akan, bisa, dll)
- Social media slang (wkwk, haha, anjir, dll)
- Common English words (the, and, for, dll)

## 📝 Development Notes

### Issue Solved

1. **MLflow Artifact Download**: Menggunakan `/get-artifact` endpoint untuk proxy S3 download
2. **React 19 Compatibility**: Switching dari `react-wordcloud` ke vanilla `wordcloud`
3. **TailwindCSS PostCSS**: Downgrade ke v3.4.0 dengan object-style config
4. **Word Distribution**: Log normalization untuk visualisasi yang lebih baik
5. **Stopword Filtering**: 100+ Indonesian stopwords untuk hasil yang lebih meaningful

## 🚦 Running the Application

1. Start Flask API (Terminal 1):
```bash
python flaskapi.py
```

2. Start Frontend (Terminal 2):
```bash
cd frontend
npm run dev
```

3. Buka browser: `http://localhost:5174`

## 📄 License

MIT License
