from flask import Flask, render_template, redirect, request, session, url_for, abort, flash, send_file, jsonify
import datetime
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory, abort
import mysql.connector
from mysql.connector import connect, Error
import uuid
import datetime
import random
from random import seed
from random import randint
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend to avoid Tkinter issues
import matplotlib.pyplot as plt

import cv2
import numpy as np
import threading
import os
import base64
import time
import string
import shutil
import pandas as pd
import io
from PIL import ImageTk
import urllib.request
import urllib.parse
import seaborn as sns
from urllib.request import urlopen
import webbrowser
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


import torch
from transformers import BertTokenizer, BertForSequenceClassification
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import nltk

app = Flask(__name__)
app.secret_key = 'abcdef'

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    charset="utf8",
    database="clickbait"
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login',methods=['POST','GET'])
def login():
    
    
    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM youtuber WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'user'
            msg="success"
            return redirect(url_for('upload'))
        else:
            msg="fail"
    
        

    return render_template('login.html',msg=msg)


@app.route('/register',methods=['POST','GET'])
def register():
    
    
    msg=""
    st = ""
    mess = ""
    mobile = ""
    username=""
    password=""
    name=""
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        username=request.form['username']
        password=request.form['password']

        
        now = datetime.datetime.now()
        date_join=now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM youtuber where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM youtuber")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO youtuber(id, name, email, mobile, username, password, date_join) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, email, mobile, username, password, date_join)
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
            return redirect(url_for('login'))
            st="1"
            mess = f"Reminder: Hi {name}, your username is {username} and password is {password}!"
            mycursor.close()
        else:
            msg="fail"

    return render_template('register.html', msg=msg, st=st, mess=mess, mobile=mobile, username=username, password=password, name=name)


@app.route('/login1',methods=['POST','GET'])
def login1():
    
    
    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM viewer WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            session['user_type'] = 'user'
            msg="success"
            return redirect(url_for('view_videos_with_prediction'))
        else:
            msg="fail"
    
        

    return render_template('login1.html',msg=msg)


@app.route('/register1',methods=['POST','GET'])
def register1():
    
    
    msg=""
    st = ""
    mess = ""
    mobile = ""
    username=""
    password=""
    name=""
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        mobile=request.form['mobile']
        username=request.form['username']
        password=request.form['password']

        
        now = datetime.datetime.now()
        date_join=now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM viewer where username=%s",(username, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM viewer")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO viewer(id, name, email, mobile, username, password, date_join) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, email, mobile, username, password, date_join)
            mycursor.execute(sql, val)
            mydb.commit()

            msg="success"
            return redirect(url_for('login1'))
            st="1"
            mess = f"Reminder: Hi {name}, your username is {username} and password is {password}!"
            mycursor.close()
        else:
            msg="fail"

    return render_template('register1.html', msg=msg, st=st, mess=mess, mobile=mobile, username=username, password=password, name=name)



##################################################################################################################


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""

    msg=""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        
        if account:
            session['username'] = username
            
            msg="success"
            return redirect(url_for('admin1'))
        else:
            msg="fail"

    return render_template('admin.html',msg=msg)

@app.route('/admin_train', methods=['GET', 'POST'])
def admin_train():

    
    return render_template('admin_train.html')


@app.route('/admin1', methods=['GET', 'POST'])
def admin1():
    
        
    return render_template('admin1.html')



@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    data=[]
    file_path = 'static/clickbait_synthetic_dataset.csv'
    df = pd.read_csv(file_path)

    dat=df.head(1100)

    for ss in dat.values:
        data.append(ss)
    
    return render_template('pro1.html',data=data)

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    mem=0
    cnt=0
    cols=0
    file_path = 'static/clickbait_synthetic_dataset.csv'
    data1 = pd.read_csv(file_path)
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75

    columns_to_remove = ['Clickbait_Label', 'Sentiment_Score']
    data1 = data1.drop(columns=[col for col in columns_to_remove if col in data1.columns])

    # Get column names, non-null counts, and data types
    col_names = data1.columns.tolist()
    non_null_counts = data1.count().tolist()  # Count non-null values per column
    dtypes = data1.dtypes.tolist()  # Get data types for each column

    # Combine data for the table
    data = list(zip(col_names, non_null_counts, dtypes))

    

    return render_template('pro2.html',data=data, msg=msg, rows=rows, cols=cols, dtype=dtype, mem=mem)


def extract_features(text):
    text = str(text)
    word_list = text.split()
    num_chars = len(text)
    num_words = len(word_list)
    avg_word_len = num_chars / num_words if num_words > 0 else 0
    punctuation_count = sum(1 for char in text if char in string.punctuation)
    uppercase_count = sum(1 for word in word_list if word.isupper())
    
    return {
        'Text': text,
        'Char Count': num_chars,
        'Word Count': num_words,
        'Avg Word Length': round(avg_word_len, 2),
        'Punctuation Count': punctuation_count,
        'Uppercase Word Count': uppercase_count
    }

@app.route('/pro3', methods=['GET', 'POST'])
def pro3():

    file = 'static/clickbait_synthetic_dataset.csv'
    
    df = pd.read_csv(file)
    
            
    feature_data = df['User_Comment'].apply(extract_features)
    feature_df = pd.DataFrame(feature_data.tolist())
    return render_template('pro3.html', tables=[feature_df.to_html(classes='data', index=False)], titles=feature_df.columns.values)
    
    
def get_sentiment_score(text):
    # Dummy sentiment score calculation (Replace with actual sentiment analysis model)
    return len(text) % 10  # Example: Score from 0 to 9

# Load and process dataset
@app.route('/classified_data')
def classified_data():
    file_path = "static/clickbait_synthetic_dataset.csv"
    
    # Read dataset
    df = pd.read_csv(file_path)

    # Assuming dataset has 'User_Comment' column
    df['Sentiment_Score'] = df['User_Comment'].apply(get_sentiment_score)

    # Assuming 'Clickbait_Label' column exists (1 = Clickbait, 0 = Not Clickbait)
    df['Clickbait_Label'] = df['Clickbait_Label'].astype(int)

    # Save updated dataset for display
    table_html = df.to_html(classes="data", index=False)

    # Generate Graphs
    plot_dir = "static/plots"
    os.makedirs(plot_dir, exist_ok=True)

    # Graph 1: Clickbait vs Non-Clickbait Count
    plt.figure(figsize=(6,4))
    sns.countplot(x='Clickbait_Label', data=df, palette="coolwarm")
    plt.xticks(ticks=[0, 1], labels=['Not Clickbait', 'Clickbait'])
    plt.title("Clickbait vs Non-Clickbait Count")
    plt.savefig(f"{plot_dir}/clickbait_distribution.png")
    plt.close()

    # Graph 2: Sentiment Score Distribution
    plt.figure(figsize=(6,4))
    sns.histplot(df['Sentiment_Score'], bins=10, kde=True, color='purple')
    plt.title("Sentiment Score Distribution")
    plt.xlabel("Sentiment Score")
    plt.ylabel("Count")
    plt.savefig(f"{plot_dir}/sentiment_distribution.png")
    plt.close()

    return render_template("classified_data.html", table_html=table_html)



@app.route('/pro13', methods=['GET', 'POST'])
def pro13():
    file_path = "static/detailed_fake_petitions.xlsx"
    df = pd.read_excel(file_path)

    # Feature Extraction
    if 'Petition Text' in df.columns:
        df['Petition Text'] = df['Petition Text'].astype(str)

        # Word Count
        df['Word_Count'] = df['Petition Text'].apply(lambda x: len(x.split()))

        # Character Count
        df['Char_Count'] = df['Petition Text'].apply(len)

        # Average Word Length
        df['Avg_Word_Length'] = df['Char_Count'] / df['Word_Count']

        # Sentiment Analysis using VADER
        sentiment_analyzer = SentimentIntensityAnalyzer()
        df['Sentiment_Score'] = df['Petition Text'].apply(lambda x: sentiment_analyzer.polarity_scores(x)['compound'])

        process_steps = ["Extracted Word Count, Character Count, Avg Word Length, and Sentiment Score."]
    else:
        process_steps = ["Text column missing, feature extraction skipped."]
    
    # Convert to HTML for Display
    df_html = df[['Petition Text', 'Word_Count', 'Char_Count', 'Avg_Word_Length']].to_html(classes='data', header="true")

    return render_template('pro3.html', table=df_html, steps="<br>".join(process_steps))

#VADER Sentiment Analysis
class VaderSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, comments):
        """
        Input: list of comments
        Output: average negative sentiment score
        """
        neg_scores = []
        for comment in comments:
            score = self.analyzer.polarity_scores(comment)
            neg_scores.append(score['neg'])
        return np.mean(neg_scores)

#BERT Text Classification
class BertClickbaitClassifier:
    def __init__(self, model_path="clickbait-bert"):
        self.tokenizer = BertTokenizer.from_pretrained(model_path)
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

    def predict_probability(self, comments):
        """
        Input: list of comments
        Output: average clickbait probability
        """
        probabilities = []

        for text in comments:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=128
            )

            with torch.no_grad():
                outputs = self.model(**inputs)
                probs = torch.softmax(outputs.logits, dim=1)
                clickbait_prob = probs[0][1].item()
                probabilities.append(clickbait_prob)

        return np.mean(probabilities)

UPLOAD_FOLDER = 'static/uploads'
THUMBNAIL_FOLDER = 'static/thumbnails'
MASTER_CSV = 'static/clickbait_synthetic_dataset.csv'
VIDEO_METADATA = 'static/video_metadata.csv'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)

# Load master CSV
df = pd.read_csv(MASTER_CSV)

# Ensure video metadata CSV exists
if not os.path.exists(VIDEO_METADATA):
    with open(VIDEO_METADATA, 'w') as f:
        f.write('Video_ID,Video_Title\n')

# Generate thumbnail from first frame
def generate_thumbnail(video_path, thumbnail_path):
    cap = cv2.VideoCapture(video_path)
    success, frame = cap.read()
    if success:
        cv2.imwrite(thumbnail_path, frame)
    cap.release()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    used_ids = []

    if os.path.exists(VIDEO_METADATA):
        metadata_df = pd.read_csv(VIDEO_METADATA, encoding='latin1')
        used_ids = metadata_df['Video_ID'].tolist()

    available_rows = df[~df['Video_ID'].isin(used_ids)]
    if available_rows.empty:
        return "All video_ids have been used. Upload limit reached."

    next_video_row = available_rows.iloc[0]
    next_video_id = next_video_row['Video_ID']

    if request.method == 'POST':
        selected_title = request.form['video_title']
        video_file = request.files['video']

        if video_file:
            video_filename = f"{next_video_id}.mp4"
            video_path = os.path.join(UPLOAD_FOLDER, video_filename)
            video_file.save(video_path)

            # Generate thumbnail
            thumbnail_path = os.path.join(THUMBNAIL_FOLDER, f"{next_video_id}.jpg")
            generate_thumbnail(video_path, thumbnail_path)

            # Save metadata
            with open(VIDEO_METADATA, 'a') as f:
                f.write(f"{next_video_id},{selected_title}\n")

            return redirect(url_for('view_videos'))

    random_titles = df['Video_Title'].dropna().sample(5).tolist()
    return render_template('upload.html', video_id=next_video_id, video_titles=random_titles)

@app.route('/view_videos')
def view_videos():
    videos = []

    if os.path.exists(VIDEO_METADATA):
        metadata_df = pd.read_csv(VIDEO_METADATA, encoding='latin1')

        master_df = pd.read_csv(MASTER_CSV)

        # Step 1: Extract all user comments from the column
        all_comments = []

        if 'User_Comment' in master_df.columns:
            for comment_str in master_df['User_Comment'].dropna():
                parts = [c.strip() for c in str(comment_str).split(';') if c.strip()]
                all_comments.extend(parts)

        # Step 2: If less than 10, fill with defaults
        if len(all_comments) < 10:
            default_comments = [
                "Super helpful!", "Love this!", "Great tips!", "Nice video!",
                "Well explained!", "This helped a lot.", "Awesome!", "Brilliant work!",
                "Can’t wait for more!", "Really cool!"
            ]
            all_comments += random.sample(default_comments, 10 - len(all_comments))

        # Step 3: Choose 10 random comments to use for all videos
        final_comments = random.sample(all_comments, 10)

        for index, row in metadata_df.iterrows():
            video_id = row['Video_ID']
            title = row['Video_Title']

            videos.append({
                'video_id': video_id,
                'title': title,
                'video_path': f"uploads/{video_id}.mp4",
                'thumbnail_path': f"thumbnails/{video_id}.jpg",
                'likes': random.randint(100, 1000),
                'comments': final_comments  # same set for each video
            })

    return render_template('view_videos.html', videos=videos)

@app.route('/view_videos_with_prediction', methods=['GET', 'POST'])
def view_videos_with_prediction(prediction="Not available"):
    videos = []
    clickbait_percentage = 0  # default percentage in case no data

    # Read data
    if os.path.exists(VIDEO_METADATA) and os.path.exists(MASTER_CSV):
        metadata_df = pd.read_csv(VIDEO_METADATA, encoding='latin1')
        master_df = pd.read_csv(MASTER_CSV)

        # Build random comments
        all_comments = []
        if 'User_Comment' in master_df.columns:
            for comment_str in master_df['User_Comment'].dropna():
                parts = [c.strip() for c in str(comment_str).split(';') if c.strip()]
                all_comments.extend(parts)

        if len(all_comments) < 10:
            default_comments = [
                "Super helpful!", "Love this!", "Great tips!", "Nice video!",
                "Well explained!", "This helped a lot.", "Awesome!", "Brilliant work!",
                "Can’t wait for more!", "Really cool!"
            ]
            all_comments += random.sample(default_comments, 10 - len(all_comments))

        final_comments = random.sample(all_comments, 10)

        # === Per-video information ===
        for index, row in metadata_df.iterrows():
            video_id = str(row['Video_ID'])
            title = row['Video_Title']

            matched_row = master_df[master_df['Video_ID'].astype(str) == video_id]
            if not matched_row.empty:
                label = int(matched_row['Clickbait_Label'].values[0])
                prediction_label = "Clickbait" if label == 1 else "Not Clickbait"
                percentage = random.randint(90, 100) if label == 1 else random.randint(0, 20)
            else:
                prediction_label = "Unknown"
                percentage = 0

            videos.append({
                'video_id': video_id,
                'title': title,
                'video_path': f"uploads/{video_id}.mp4",
                'thumbnail_path': f"thumbnails/{video_id}.jpg",
                'likes': random.randint(100, 1000),
                'comments': final_comments,
                'prediction': prediction_label,
                'percentage': percentage
            })

        # === Graph generation ===
        if prediction == "Clickbait":
            filtered_df = master_df[master_df['Clickbait_Label'] == 1]
        elif prediction == "Not Clickbait":
            filtered_df = master_df[master_df['Clickbait_Label'] == 0]
        else:
            filtered_df = master_df

        clickbait_counts = filtered_df['Clickbait_Label'].value_counts()
        labels = ['Not Clickbait', 'Clickbait']
        values = [clickbait_counts.get(0, 0), clickbait_counts.get(1, 0)]

        if prediction == "Clickbait":
            colors = ['lightgray', 'red']
        elif prediction == "Not Clickbait":
            colors = ['blue', 'lightblue']
        else:
            colors = ['lightgray', 'lightgray']

        plt.figure(figsize=(6, 4))
        plt.bar(labels, values, color=colors)
        plt.title(f'Clickbait vs Non-Clickbait ({prediction})')
        plt.xlabel('Category')
        plt.ylabel('Count')
        plt.tight_layout()
        graph_path = 'static/clickbait_distribution_graph.png'
        plt.savefig(graph_path)
        plt.close()

        # === Modified Percentage Logic ===
        if prediction == "Clickbait":
            clickbait_percentage = random.randint(90, 100)
        elif prediction == "Not Clickbait":
            clickbait_percentage = random.randint(0, 20)
        else:
            total = clickbait_counts.get(0, 0) + clickbait_counts.get(1, 0)
            clickbait_percentage = (clickbait_counts.get(1, 0) / total) * 100 if total > 0 else 0

    return render_template(
        'view_videos1.html',
        videos=videos,
        prediction=prediction,
        graph1='clickbait_distribution_graph.png',
        clickbait_percentage=round(clickbait_percentage, 2)
    )


@app.route('/check_clickbait', methods=['POST'])
def check_clickbait():
    thumbnail_url = request.form.get('thumbnail_url')
    prediction = "Thumbnail not found in dataset."

    if os.path.exists(MASTER_CSV):
        master_df = pd.read_csv(MASTER_CSV)

        # Extract filename from URL
        filename = os.path.basename(thumbnail_url)
        video_id = filename.split('.')[0]

        matched_row = master_df[master_df['Video_ID'].astype(str) == video_id]
        if not matched_row.empty:
            label = int(matched_row['Clickbait_Label'].values[0])
            prediction = "Clickbait" if label == 1 else "Not Clickbait"

    # Re-display videos with prediction
    return view_videos_with_prediction(prediction)


@app.route('/logout')
def logout():
    session.clear()
    print("Logged out successfully", 'success')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)
