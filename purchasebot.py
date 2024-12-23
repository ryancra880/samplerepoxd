from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Replace 'YOUR_TOKEN_HERE' with your bot's API token
API_TOKEN = "7271303932:AAGywqIevTwnjSEtn2qTQlWzyt8IiX26uwA"

# Conversation states
WAITING_FOR_WALLET = 1

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send a welcome message asking for the Sol wallet address."""
    await update.message.reply_text(
        "Welcome to PullBot, please enter your Sol wallet address."
    )
    context.user_data["awaiting_wallet"] = True  # Flag to track wallet input phase
    return WAITING_FOR_WALLET

# Handle the user's wallet address
async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the wallet address and ask for payment."""
    if not context.user_data.get("awaiting_wallet", False):
        # Ignore messages if we're not expecting a wallet address
        return

    user_wallet = update.message.text
    context.user_data["wallet_address"] = user_wallet  # Store wallet address for later use
    context.user_data["awaiting_wallet"] = False  # Reset the flag as wallet has been provided

    await update.message.reply_text(
        f"Thank you, please send 0.5 SOL to this address:\n"f"`8jffsixa8n4nBkQXLiFwHYrvM4GFYCTc5ZueVpuqW1ny`\n"f"\n"
        f"Click the button below when you're done.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("I've sent the Sol", callback_data="payment_done")]
        ]),
        parse_mode="Markdown"  # To display the wallet address nicely
    )

# Handle the button click after payment
async def payment_done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the confirmation of payment."""
    query = update.callback_query
    await query.answer()  # Acknowledge the button click

    # Retrieve stored wallet address (if needed for processing)
    user_wallet = context.user_data.get("wallet_address", "Unknown")

    await query.message.reply_text(
        "Thank you for your payment. If the wallet address you provided earlier is valid, "
        "you will receive your PullBot API key within an hour. Thank you for your patience."
    )

# Fallback handler
async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unrecognized commands or messages."""
    await update.message.reply_text("I didn't understand that. Please follow the instructions.")

# Main function to start the bot
def main():
    """Run the bot."""
    app = Application.builder().token(API_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    app.add_handler(CallbackQueryHandler(payment_done, pattern="^payment_done$"))
    app.add_handler(MessageHandler(filters.COMMAND, fallback))  # Catch-all for unrecognized commands

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
