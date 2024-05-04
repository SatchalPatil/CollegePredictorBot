import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load your datasets containing college_name and percentile/rank for CET and JEE
data_cet = pd.read_csv("c:/Users/Satchal Patil/Downloads/better college cutoff.csv")
data_jee = pd.read_csv("c:/Users/Satchal Patil/OneDrive/Desktop/JEE cutoff.csv")

# Encoding college names to numerical labels for CET dataset
label_encoder_cet = LabelEncoder()
data_cet['college_label'] = label_encoder_cet.fit_transform(data_cet['college_name'])

# Encoding college names to numerical labels for JEE dataset
label_encoder_jee = LabelEncoder()
data_jee['college_label'] = label_encoder_jee.fit_transform(data_jee['college_name'])

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

# Function to take user input for percentile or rank
def get_user_input():
    while True:
        exam_type = input("Enter 'CET' for Maharashtra CET or 'JEE' for Joint Entrance Exam (JEE), or 'exit' to quit: ").upper()
        if exam_type == 'EXIT':
            return None, None
        elif exam_type == 'CET':
            user_input = float(input("Enter your CET percentile: "))
            return exam_type, user_input
        elif exam_type == 'JEE':
            user_input = int(input("Enter your JEE rank: "))
            return exam_type, user_input
        else:
            print("Invalid input. Please enter 'CET', 'JEE', or 'exit'.")

# Creating and training the Random Forest model for CET
model_cet = RandomForestClassifier(n_estimators=100, random_state=42)
X_cet = data_cet[['percentile']]
y_cet = data_cet['college_label']
X_train_cet, X_test_cet, y_train_cet, y_test_cet = train_test_split(X_cet, y_cet, test_size=0.2, random_state=42)
model_cet.fit(X_train_cet, y_train_cet)

# Creating and training the Random Forest model for JEE
model_jee = RandomForestClassifier(n_estimators=100, random_state=42)
if 'percentile' in data_jee.columns:
    X_jee = data_jee[['percentile']]
elif 'rank' in data_jee.columns:
    X_jee = data_jee[['rank']]
y_jee = data_jee['college_label']
X_train_jee, X_test_jee, y_train_jee, y_test_jee = train_test_split(X_jee, y_jee, test_size=0.2, random_state=42)
model_jee.fit(X_train_jee, y_train_jee)

# Keep asking user for input until they choose to exit
while True:
    exam_type, user_score = get_user_input()
    if exam_type is None:
        break

    # If user input is valid, display top colleges
    if exam_type == 'CET':
        top_colleges = get_top_colleges(data_cet, label_encoder_cet, user_score, model_cet)
        print("\nTop 10 Colleges for CET:")
        for college in top_colleges:
            print(college)
    elif exam_type == 'JEE':
        top_colleges = get_top_colleges(data_jee, label_encoder_jee, user_score, model_jee)
        print("\nTop 10 Colleges for JEE:")
        for college in top_colleges:
            print(college)
