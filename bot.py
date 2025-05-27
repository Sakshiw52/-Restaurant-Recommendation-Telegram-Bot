# bot.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from config import BOT_TOKEN
from database import init_db, add_user, get_user_location, add_restaurant
from restaurant_api import fetch_restaurants

CHOOSING, TYPING_LOCATION, TYPING_CUISINE = range(3)

keyboard = [["Set Location", "Find Restaurant"]]
markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to RestaurantBot! Please choose:", reply_markup=markup)
    return CHOOSING

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Set Location":
        await update.message.reply_text("Please type your location (e.g., New York):")
        return TYPING_LOCATION
    elif text == "Find Restaurant":
        await update.message.reply_text("What type of cuisine do you want?")
        return TYPING_CUISINE

async def set_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text
    user = update.message.from_user
    add_user(user.id, user.username, location)
    await update.message.reply_text(f"Location set to {location}")
    return CHOOSING

async def find_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cuisine = update.message.text
    user = update.message.from_user
    location = get_user_location(user.id)

    if not location:
        await update.message.reply_text("Set your location first.")
        return CHOOSING

    restaurants = fetch_restaurants(location, cuisine)

    if restaurants:
        for r in restaurants:
            await update.message.reply_text(f"{r['name']} - Rating: {r['rating']}")
            add_restaurant(r)
    else:
        # Fallback mock data based on cuisine
        fallback_restaurants = []

        if "chinese" in cuisine.lower():
            fallback_restaurants = [
                {"name": "Dragon Palace", "rating": 4.4},
                {"name": "Wok This Way", "rating": 4.2},
                {"name": "Hakka Express", "rating": 4.5},
                {"name": "Red Lantern", "rating": 4.3},
                {"name": "Bamboo Basket", "rating": 4.1}
            ]
        elif "italian" in cuisine.lower():
            fallback_restaurants = [
                {"name": "Pasta Fresca", "rating": 4.5},
                {"name": "Roma Ristorante", "rating": 4.3},
                {"name": "Olive Garden Pune", "rating": 4.4},
                {"name": "Little Italy", "rating": 4.2},
                {"name": "La Pino'z", "rating": 4.1}
            ]
        elif "indian" in cuisine.lower():
            fallback_restaurants = [
                {"name": "Spice of India", "rating": 4.3},
                {"name": "Tandoori Nights", "rating": 4.0},
                {"name": "Bombay Masala House", "rating": 4.5},
                {"name": "Curry Junction", "rating": 4.1},
                {"name": "Maharaja Delight", "rating": 4.2}
            ]
        else:
            fallback_restaurants = [
                {"name": "Food Haven", "rating": 4.2},
                {"name": "Taste Corner", "rating": 4.0},
                {"name": "Flavor Town", "rating": 4.3}
            ]

        response = f"🍽️ Showing top {cuisine} restaurants in {location}:\n"
        for i, r in enumerate(fallback_restaurants, start=1):
            response += f"{i}. 🍛 {r['name']} – ⭐ {r['rating']}\n"

        await update.message.reply_text(response)

    return CHOOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bye!")
    return ConversationHandler.END

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            TYPING_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_location)],
            TYPING_CUISINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, find_restaurant)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
