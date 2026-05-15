# 🎯 Comment-Driven Clickbait Thumbnail Detection
### Using Sentiment and Transformer-Based Analysis

> **MCA Final Year Project** | SRM Institute of Science and Technology  
> **Author:** Mano K (RA2432242010045)  
> **Guide:** Dr. B. Nagarajan  
> **Specialization:** Generative Artificial Intelligence

---

## 📌 About the Project

A YouTube Simulator Web App that automatically detects misleading (clickbait) thumbnails by analyzing user comments using **VADER Sentiment Analysis** and **BERT Transformer Classification**.

Instead of analyzing images, this system leverages NLP to evaluate authentic user feedback and generate a **Clickbait Score** that flags deceptive thumbnails.

---

## 🔄 How It Works

```
User Comments → Preprocessing → VADER Sentiment Analysis
                                        ↓
                              BERT Classification
                                        ↓
                            Clickbait Score Generated
                                        ↓
                         Flag ❌ / Certify ✅ Video
                                        ↓
                         Recommend Trustworthy Videos
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.7, Flask |
| Frontend | HTML, CSS, Bootstrap |
| Database | MySQL (WampServer) |
| NLP Models | VADER + BERT (HuggingFace) |
| ML Libraries | TensorFlow, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |

---

## 👥 User Roles

- **Admin** – Upload datasets, train and deploy BERT model
- **YouTuber** – Upload videos/thumbnails, receive certification
- **Viewer** – Search videos, get clickbait warnings + recommendations

---

## ⚙️ How to Run Locally

### Prerequisites
- Python 3.7+
- WampServer (MySQL)
- Git

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/your-username/clickbait-detection.git
cd clickbait-detection

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup Database
# Open WampServer → phpMyAdmin
# Create database: clickbait
# Import: db/clickbait.sql

# 4. Run the app
python main.py

# 5. Open browser
# http://localhost:5000
```

---

## 📁 Project Structure

```
clickbait-detection/
├── main.py                          # Flask app - main backend
├── requirements.txt                 # Python dependencies
├── db/
│   └── clickbait.sql               # MySQL database schema
├── static/
│   ├── clickbait_synthetic_dataset.csv
│   ├── plots/                      # Generated graphs
│   ├── images/                     # UI images
│   ├── js/                         # JavaScript files
│   └── plugins/                    # CSS plugins
└── templates/                      # HTML templates (Flask)
```

---

## 🧠 Core Models

### VADER (Sentiment Analysis)
Detects negative emotional cues in comments → signals misleading content

### BERT (Bidirectional Encoder Representations from Transformers)
Fine-tuned classifier that identifies clickbait-specific linguistic patterns

### Clickbait Score Formula
```
Clickbait Score = f(VADER negative polarity + BERT clickbait probability)
Score > threshold → FLAG as Clickbait ❌
Score < threshold → CERTIFY as Genuine ✅
```

---

## 📊 Results

- VADER effectively identified negative sentiment indicating deceptive thumbnails
- BERT accurately classified clickbait vs genuine comments
- System achieved high accuracy and precision in detection
- Recommendation system successfully guided users to trustworthy content

---

## 🔮 Future Enhancements

- Multilingual comment analysis
- Real-time YouTube API integration
- Image-based thumbnail analysis using CNN
- Extension to other platforms (Instagram, Facebook)

---

## 🏫 Institution

**SRM Institute of Science and Technology**  
Faculty of Science and Humanities  
Department of Computer Applications  
Kattankulathur – 603203

---

## 📄 License

This project is for academic purposes only.
