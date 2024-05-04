import logging
import pandas as pd
from flask import Flask, request
import requests
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load your datasets containing college_name and percentile/rank for CET and JEE
data_cet = pd.read_csv("c:/Users/Satchal Patil/Downloads/better college cutoff.csv")
data_jee = pd.read_csv("c:/Users/Satchal Patil/OneDrive/Desktop/JEE cutoff.csv")

# Encoding college names to numerical labels for CET dataset
label_encoder_cet = LabelEncoder()
data_cet['college_label'] = label_encoder_cet.fit_transform(data_cet['college_name'])

# Encoding college names to numerical labels for JEE dataset
label_encoder_jee = LabelEncoder()
data_jee['college_label'] = label_encoder_jee.fit_transform(data_jee['college_name'])

# Handle missing values in the JEE dataset
imputer = SimpleImputer(strategy='mean')
data_jee_imputed = imputer.fit_transform(data_jee[['rank']])

# Train RandomForest models for CET and JEE datasets
model_cet = RandomForestClassifier()
model_cet.fit(data_cet[['percentile']], data_cet['college_label'])

model_jee = RandomForestClassifier()
model_jee.fit(data_jee_imputed, data_jee['college_label'])

# Function to get top 10 colleges based on percentile/rank and dataset
def get_top_colleges(data, label_encoder, user_score, model):
    # Predicting the college labels for the user score
    predicted_college_labels = model.predict([[user_score]])

    # Decoding the predicted college labels to college names
    predicted_colleges = label_encoder.inverse_transform(predicted_college_labels)

    # Calculate the distance of each college from the user score
    if 'percentile' in data.columns:
        data['distance'] = abs(data['percentile'] - user_score)
    elif 'rank' in data.columns:
        data['distance'] = abs(data['rank'] - user_score)

    # Sort the colleges based on their distance from the user score
    sorted_colleges = data.sort_values(by='distance').head(10)

    # Return the top 10 closest colleges to the user score
    return sorted_colleges['college_name']

# Set up Flask
app = Flask(__name__)

# Function to handle incoming Telegram updates (webhook)
@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.json
    process_update(update)
    return '', 200

# Function to process Telegram update
def process_update(update):
    # Extract relevant information from the update
    message = update.get('message')
    if message is None:
        return

    text = message.get('text')
    chat_id = message.get('chat').get('id')

    # Process the text message
    if text:
        exam_type = text.strip().upper()
        if exam_type in ['CET', 'JEE']:
            # Respond with a message to enter score or rank
            send_message(chat_id, f'Great! You selected {exam_type}. Now, please enter your {exam_type} score or rank.')
        else:
            # Invalid exam type
            send_message(chat_id, 'Invalid exam type. Please enter either "CET" or "JEE".')

# Function to send message to Telegram
def send_message(chat_id, text):
    bot_token = "7158075563:AAEUV12F7LcvUlu2MO_iiYG798UNJJfTWoU"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=data)
    if not response.ok:
        logger.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

if __name__ == '__main__':
    # Set up webhook
    bot_token = "7158075563:AAEUV12F7LcvUlu2MO_iiYG798UNJJfTWoU"
    webhook_url = "https://api.telegram.org/bot7158075563:AAEUV12F7LcvUlu2MO_iiYG798UNJJfTWoU/getUpdates"
    response = requests.get(f"https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}")
    if response.ok:
        logger.info("Webhook set up successfully")
    else:
        logger.error("Failed to set up webhook")

    # Run Flask app with Gunicorn
    app.run(host='0.0.0.0', port=5001)
