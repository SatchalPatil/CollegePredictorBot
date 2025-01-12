# College Predictor Bot

A machine learning-powered bot that predicts and ranks the top 10 colleges based on user-provided scores for Maharashtra CET or JEE (Joint Entrance Examination). This project utilizes past three years of college cutoff data for predictions.

## Features

- Predicts top 10 colleges based on CET percentile or JEE rank.
- Offers results in a sorted format based on proximity to user score.
- Fully integrated with Telegram to act as a chatbot for users.

---

## Datasets

### 1. CET Dataset (`CET_cutoff.csv`)
- **Attributes**:
  - `college_name`: Name of the college.
  - `percentile`: Past three years' cutoff percentiles.

### 2. JEE Dataset (`JEE_cutoff.csv`)
- **Attributes**:
  - `college_name`: Name of the college.
  - `rank`: Past three years' cutoff ranks.

---

## Installation and Requirements

## Prerequisites
Ensure Python 3.7+ is installed along with the following libraries:

pip install pandas scikit-learn python-telegram-bot

---

## Setting Up Telegram Bot
- Create a bot using BotFather on Telegram.
- Obtain the bot token and update the BOT_TOKEN in bot.py

## Running the Bot
Start the bot using:

bash
Copy code
python bot.py
Open Telegram and send /start to the bot.

Enter your CET percentile or JEE rank to get predictions.

## Workflow
# Model Training
- Algorithm: Random Forest Classifier.
- Features:
  For CET: Percentile-based predictions.
  For JEE: Rank-based predictions.
- Training: Data split into 80% training and 20% testing.
- 
# Prediction
- User score is passed to the trained model.
- Top 10 colleges are retrieved based on proximity to the user's score.
- 
# Telegram Bot
- User interacts with the bot by providing their scores.
- Bot responds with the top 10 colleges for the given CET or JEE exam.

## Sample Commands for Telegram Bot
- /start: Initiate the bot.
- Provide CET percentile (e.g., 95.6).
- Provide JEE rank (e.g., 1500).

  ![Screenshot 2024-11-27 000236](https://github.com/user-attachments/assets/b434624b-9214-4fd7-b57c-6f81b8d02d42)

  ![Screenshot 2024-11-27 000133](https://github.com/user-attachments/assets/27c7843e-6a0c-4cee-99d0-46131cee455d)


