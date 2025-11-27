from textblob import TextBlob
import re

class SentimentAnalyzer:
    """
    Sentiment analyzer untuk teks bahasa Indonesia/campuran.
    Menggunakan TextBlob dengan beberapa penyesuaian.
    """
    
    # Kata-kata positif bahasa Indonesia
    POSITIVE_WORDS = {
        'bagus', 'baik', 'hebat', 'sukses', 'senang', 'mantap', 'keren',
        'maju', 'berkembang', 'meningkat', 'optimal', 'efektif', 'efisien',
        'terima kasih', 'dukung', 'mendukung', 'setuju', 'suka', 'cinta',
        'luar biasa', 'cemerlang', 'gemilang', 'jaya', 'menang', 'prestasi'
    }
    
    # Kata-kata negatif bahasa Indonesia
    NEGATIVE_WORDS = {
        'buruk', 'jelek', 'gagal', 'sedih', 'kecewa', 'marah', 'benci',
        'mundur', 'menurun', 'rusak', 'korup', 'korupsi', 'salah', 'bodoh',
        'goblok', 'tolol', 'bangsat', 'asu', 'brengsek', 'gagal', 'hancur',
        'miskin', 'susah', 'sulit', 'masalah', 'kritik', 'protes', 'demo'
    }
    
    def clean_text(self, text):
        """Bersihkan teks dari URL, mention, hashtag, dll"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags
        text = re.sub(r'#\w+', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text.lower()
    
    def analyze_indonesian(self, text):
        """Analisis sentiment menggunakan kamus bahasa Indonesia"""
        text_clean = self.clean_text(text)
        words = text_clean.split()
        
        positive_count = sum(1 for word in words if word in self.POSITIVE_WORDS)
        negative_count = sum(1 for word in words if word in self.NEGATIVE_WORDS)
        
        if positive_count > negative_count:
            return 'positive', (positive_count - negative_count) / max(len(words), 1)
        elif negative_count > positive_count:
            return 'negative', -(negative_count - positive_count) / max(len(words), 1)
        else:
            return 'neutral', 0.0
    
    def analyze_textblob(self, text):
        """Analisis sentiment menggunakan TextBlob (untuk teks Inggris)"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'positive', polarity
            elif polarity < -0.1:
                return 'negative', polarity
            else:
                return 'neutral', polarity
        except:
            return 'neutral', 0.0
    
    def analyze(self, text):
        """Analisis sentiment gabungan (Indonesia + TextBlob)"""
        text_clean = self.clean_text(text)
        
        # Analisis dengan kamus Indonesia
        sentiment_id, score_id = self.analyze_indonesian(text)
        
        # Analisis dengan TextBlob
        sentiment_en, score_en = self.analyze_textblob(text_clean)
        
        # Gabungkan hasil (prioritas kamus Indonesia)
        if abs(score_id) > 0.01:  # Ada kata positif/negatif Indonesia
            return sentiment_id, score_id
        else:
            return sentiment_en, score_en
    
    def analyze_docs(self, docs_list):
        """
        Analisis sentiment dari list dokumen.
        Returns: sentiment mayoritas dan skor rata-rata
        """
        if not docs_list:
            return 'neutral', 0.0
        
        sentiments = []
        scores = []
        
        for doc in docs_list:
            sentiment, score = self.analyze(doc)
            sentiments.append(sentiment)
            scores.append(score)
        
        # Hitung mayoritas sentiment
        sentiment_counts = {
            'positive': sentiments.count('positive'),
            'negative': sentiments.count('negative'),
            'neutral': sentiments.count('neutral')
        }
        
        majority_sentiment = max(sentiment_counts, key=sentiment_counts.get)
        avg_score = sum(scores) / len(scores)
        
        return majority_sentiment, avg_score, sentiment_counts
