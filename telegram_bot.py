import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Load datasets
data_cet = pd.read_csv("CET_cutoff.csv")
data_jee = pd.read_csv("JEE_cutoff.csv")

# Encode college CET
label_encoder_cet = LabelEncoder()
data_cet['college_label'] = label_encoder_cet.fit_transform(data_cet['college_name'])

# Encode college JEE
label_encoder_jee = LabelEncoder()
data_jee['college_label'] = label_encoder_jee.fit_transform(data_jee['college_name'])

# Train Random Forest model for CET
model_cet = RandomForestClassifier(n_estimators=100, random_state=42)
X_cet = data_cet[['percentile']]
y_cet = data_cet['college_label']
X_train_cet, X_test_cet, y_train_cet, y_test_cet = train_test_split(X_cet, y_cet, test_size=0.2, random_state=42)
model_cet.fit(X_train_cet, y_train_cet)

# Train Random Forest model for JEE
model_jee = RandomForestClassifier(n_estimators=100, random_state=42)
X_jee = data_jee[['percentile']] if 'percentile' in data_jee.columns else data_jee[['rank']]
y_jee = data_jee['college_label']
X_train_jee, X_test_jee, y_train_jee, y_test_jee = train_test_split(X_jee, y_jee, test_size=0.2, random_state=42)
model_jee.fit(X_train_jee, y_train_jee)

# Function to get top 10 colleges
def get_top_colleges(data, label_encoder, user_score, model):
    data['distance'] = abs(data['percentile'] - user_score) if 'percentile' in data.columns else abs(data['rank'] - user_score)
    sorted_colleges = data.sort_values(by='distance').head(10)
    return sorted_colleges['college_name'].tolist()

# /start
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome! Enter your exam type and score in the format:\n\n"
        "`CET <percentile>` or `JEE <rank>`\n"
        "Example: `CET 98.5`\n"
        "Type /help for more info.",
        parse_mode="Markdown"
    )

# /help
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Enter your exam type and score in the format:\n\n"
        "`CET <percentile>` or `JEE <rank>`\n"
        "This bot predicts the top 10 colleges based on your score.\n"
        "Type /start to begin.",
        parse_mode="Markdown"
    )

# Handle input
async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip().upper()

    try:
        if text.startswith("CET"):
            user_score = float(text.split()[1])
            top_colleges = get_top_colleges(data_cet, label_encoder_cet, user_score, model_cet)
            response = "\n".join([f"{i+1}. {college}" for i, college in enumerate(top_colleges)])
            await update.message.reply_text(f"Top 10 Colleges for CET Percentile {user_score}:\n\n{response}")
        elif text.startswith("JEE"):
            user_score = int(text.split()[1])
            top_colleges = get_top_colleges(data_jee, label_encoder_jee, user_score, model_jee)
            response = "\n".join([f"{i+1}. {college}" for i, college in enumerate(top_colleges)])
            await update.message.reply_text(f"Top 10 Colleges for JEE Rank {user_score}:\n\n{response}")
        else:
            await update.message.reply_text(
                "Invalid format! Use `CET <percentile>` or `JEE <rank>`.",
                parse_mode="Markdown"
            )
    except Exception as e:
        await update.message.reply_text(
            "Error processing your input. Please use the format:\n"
            "`CET <percentile>` or `JEE <rank>`\n"
            "Example: `CET 98.5`",
            parse_mode="Markdown"
        )

# Main function
def main() -> None:
    TOKEN = "BOT_TOKEN"

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
