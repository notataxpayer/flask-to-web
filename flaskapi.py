from flask import Flask, jsonify
from flask_cors import CORS
import mlflow
import pandas as pd
import requests
from io import StringIO
import ast
import re
from sentiment_analyzer import SentimentAnalyzer

app = Flask(__name__)
CORS(app)
mlflow.set_tracking_uri("http://virtualtech.icu:5000")

EXPERIMENT_NAME = "bertopic-pemerintah"
sentiment_analyzer = SentimentAnalyzer()

def get_latest_run_id():
    exp = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
    runs = mlflow.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=["start_time DESC"]
    )
    return runs.iloc[0].run_id


@app.route("/topic-info", methods=["GET"])
def topic_info():
    latest_run_id = get_latest_run_id()

    # Use MLflow's get-artifact API endpoint to download through the tracking server
    tracking_uri = mlflow.get_tracking_uri()
    artifact_path = f"topic_info_{latest_run_id}.csv"
    
    # MLflow API endpoint for downloading artifacts
    url = f"{tracking_uri}/get-artifact"
    params = {
        "run_uuid": latest_run_id,
        "path": artifact_path
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": f"Failed to download artifact: {response.text}"}), response.status_code
    
    # Read CSV from response content
    df = pd.read_csv(StringIO(response.text))
    return jsonify(df.to_dict(orient="records"))


@app.route("/wordcloud", methods=["GET"])
def wordcloud():
    latest_run_id = get_latest_run_id()

    # Use MLflow's get-artifact API endpoint to download through the tracking server
    tracking_uri = mlflow.get_tracking_uri()
    artifact_path = f"topic_info_{latest_run_id}.csv"
    
    # MLflow API endpoint for downloading artifacts
    url = f"{tracking_uri}/get-artifact"
    params = {
        "run_uuid": latest_run_id,
        "path": artifact_path
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": f"Failed to download artifact: {response.text}"}), response.status_code
    
    # Read CSV from response content
    df = pd.read_csv(StringIO(response.text))
    
    # Comprehensive stopwords - kata sambung, partikel, pronoun, auxiliary verbs
    stopwords = {
        # URL/web related
        'https', 'co', 'http', 'www', 'rt', 'url', 'link', 'https co',
        # Conjunctions & particles
        'yang', 'dan', 'atau', 'tapi', 'tetapi', 'namun', 'sedangkan', 
        'bahwa', 'jika', 'kalau', 'bila', 'apabila', 'maka', 'lalu',
        'kemudian', 'serta', 'agar', 'supaya', 'biar', 'karena', 'sebab',
        'oleh', 'dengan', 'tanpa', 'untuk', 'bagi', 'kepada', 'terhadap',
        # Prepositions
        'di', 'ke', 'dari', 'pada', 'dalam', 'atas', 'bawah', 'antara',
        # Pronouns
        'ini', 'itu', 'ia', 'dia', 'mereka', 'kita', 'kami', 'anda',
        'saya', 'aku', 'kamu', 'kalian', 'beliau', 'nya', 'ku', 'mu',
        # Articles & determiners
        'sang', 'si', 'para', 'kaum', 'suatu', 'sebuah', 'seorang',
        # Modals & auxiliaries
        'adalah', 'ialah', 'yaitu', 'yakni', 'akan', 'telah', 'sudah',
        'sedang', 'masih', 'pernah', 'belum', 'bisa', 'dapat', 'harus',
        'boleh', 'mau', 'ingin', 'hendak',
        # Quantifiers
        'ada', 'tidak', 'tak', 'bukan', 'semua', 'seluruh', 'setiap',
        'tiap', 'banyak', 'sedikit', 'beberapa', 'lain', 'lainnya',
        # Common informal words
        'yg', 'dgn', 'dg', 'tdk', 'tp', 'jg', 'juga', 'ya', 'yah',
        'gak', 'ga', 'kak', 'aja', 'udah', 'sih', 'kok', 'deh', 'dong',
        'lho', 'nih', 'weh', 'wes', 'was', 'lagi', 'pula', 'kayak',
        'gitu', 'gini', 'gimana', 'gmn', 'kenapa', 'knp', 'emang', 'memang',
        # Question words
        'apa', 'siapa', 'kapan', 'dimana', 'mengapa', 'bagaimana', 'berapa',
        # Particles
        'an', 'kan', 'pun', 'lah', 'kah', 'tah', 'per', 'se',
        # Common verbs to exclude (too generic)
        'jadi', 'buat', 'bikin', 'kasih', 'beri', 'ambil',
        # Time/frequency
        'kini', 'sekarang', 'nanti', 'besok', 'kemarin', 'dulu', 'lalu',
        'selalu', 'sering', 'kadang', 'jarang',
        # Intensifiers
        'sangat', 'sekali', 'amat', 'terlalu', 'lebih', 'paling', 'agak',
        'cukup', 'kurang', 'hampir', 'nyaris',
        # Social media slang
        'wkwk', 'wkwkwk', 'haha', 'hehe', 'anjir', 'anjay', 'wow', 'cie',
        'asu', 'bangsat', 'brengsek',
        # English common words
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
        'his', 'how', 'man', 'new', 'now', 'old', 'see', 'way', 'who',
        'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use',
        # Additional common words
        'klo', 'kalo', 'kl', 'sm', 'sama', 'jg', 'terus', 'trus', 'tu',
        'nah', 'noh', 'nih', 'dah', 'deh', 'banget', 'bgt', 'bener',
        'kok', 'dong', 'sih', 'org', 'orang', 'ogut', 'gua', 'gue',
        'tau', 'tahu', 'mah', 'tuh', 'sich', 'kali', 'kek', 'macem',
        'macam', 'begitu', 'begini'
    }
    
    # Process data for word cloud dari Representative_Docs
    word_freq = {}
    for _, row in df.iterrows():
        # Skip outlier topic (-1)
        if row['Topic'] == -1:
            continue
        
        # Parse Representative_Docs
        try:
            docs_str = row['Representative_Docs'].strip()
            docs = ast.literal_eval(docs_str)
        except:
            continue
        
        # Extract words dari semua dokumen
        for doc in docs:
            # Bersihkan dari URL, mention, hashtag
            import re
            # Remove URLs
            doc = re.sub(r'http\S+|www\S+|https\S+', '', doc, flags=re.MULTILINE)
            # Remove mentions
            doc = re.sub(r'@\w+', '', doc)
            # Remove hashtags symbols
            doc = re.sub(r'#\w+', '', doc)
            # Remove unicode emoji and symbols
            doc = re.sub(r'[\U00010000-\U0010ffff]', '', doc, flags=re.UNICODE)
            doc = re.sub(r'[\u2600-\u26FF\u2700-\u27BF]', '', doc)
            # Remove punctuations
            doc = re.sub(r'[^\w\s]', ' ', doc)
            
            # Split jadi kata-kata
            words = doc.lower().split()
            
            for word in words:
                word = word.strip()
                # Skip stopwords, kata pendek, dan non-alphabetic
                if (word in stopwords or 
                    len(word) < 3 or 
                    word.isdigit() or
                    not word.isalpha() or
                    word.startswith('http')):
                    continue
                
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
    
    # Convert to format for wordcloud: [{ text, value }]
    wordcloud_data = [{"text": word, "value": freq} for word, freq in word_freq.items()]
    
    # Sort by value dan ambil top words
    wordcloud_data.sort(key=lambda x: x['value'], reverse=True)
    wordcloud_data = wordcloud_data[:200]  # Top 200 kata
    
    return jsonify(wordcloud_data)


@app.route("/sentiment", methods=["GET"])
def sentiment():
    latest_run_id = get_latest_run_id()

    # Use MLflow's get-artifact API endpoint to download through the tracking server
    tracking_uri = mlflow.get_tracking_uri()
    artifact_path = f"topic_info_{latest_run_id}.csv"
    
    # MLflow API endpoint for downloading artifacts
    url = f"{tracking_uri}/get-artifact"
    params = {
        "run_uuid": latest_run_id,
        "path": artifact_path
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": f"Failed to download artifact: {response.text}"}), response.status_code
    
    # Read CSV from response content
    df = pd.read_csv(StringIO(response.text))
    
    # Analyze sentiment for each topic
    results = []
    for _, row in df.iterrows():
        # Skip outlier topic
        if row['Topic'] == -1:
            continue
        
        # Parse Representative_Docs (it's a string representation of a list)
        try:
            docs_str = row['Representative_Docs'].strip()
            # Convert string to list
            docs = ast.literal_eval(docs_str)
        except:
            docs = []
        
        if docs:
            sentiment, avg_score, sentiment_counts = sentiment_analyzer.analyze_docs(docs)
        else:
            sentiment = 'neutral'
            avg_score = 0.0
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        results.append({
            'topic': int(row['Topic']),
            'topic_name': row['Name'],
            'count': int(row['Count']),
            'sentiment': sentiment,
            'sentiment_score': round(avg_score, 3),
            'sentiment_distribution': sentiment_counts,
            'sample_docs': docs[:3] if len(docs) > 3 else docs  # First 3 docs as sample
        })
    
    # Sort by count (most discussed topics first)
    results.sort(key=lambda x: x['count'], reverse=True)
    
    return jsonify({
        'total_topics': len(results),
        'topics': results
    })


if __name__ == "__main__":
    app.run(port=8000)
