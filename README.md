# 💼 Job Recommendation System

A smart job recommendation system that uses Machine Learning (Weka), Python, and Flask to suggest suitable jobs based on a user's uploaded CV (PDF). The system extracts keywords from the CV and matches them with a job dataset using clustering and similarity analysis.

---
## Live Demo
You can access the deployed app here: [https://ats-l3cf.onrender.com](https://ats-l3cf.onrender.com)

## 🚀 Features

- Upload CV in PDF format
- Extract keywords from CV using NLP
- Recommend jobs based on extracted skills, experience, and location
- Job data clustering using K-Means (Weka)
- Simple and user-friendly web interface

---

## 🛠️ Technologies Used

- Python
- Flask (Backend & Web Interface)
- Weka (Machine Learning - Clustering)
- Pandas & Scikit-learn (Data Processing)
- PyPDF2 / pdfminer.six (PDF Text Extraction)
- HTML & CSS (Frontend)
- CSV Dataset of Jobs

---


---

## 📝 How It Works

1. **Upload your CV** (PDF)
2. **Extract keywords** using NLP (skills, experience, etc.)
3. **Pre-trained Weka model** clusters job data
4. **Compare extracted keywords** with job clusters
5. **Top job matches** are displayed to the user

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/job-recommendation-system.git
cd job-recommendation-system
pip install -r requirements.txt
## For Run
python app.py

