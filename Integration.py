from sympy.core.sympify import SympifyError
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Function to handle the /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Welcome! I am a Math Bot that can help you with integration, differentiation, and limits problems.\n"
        "Send me an expression, and I will solve it step by step!\n"
        "Use /help for instructions."
    )

# Function to handle the /help command
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Instructions:\n"
        "1. For differentiation: Send the expression in the format 'diff(expression, variable)'.\n"
        "   Example: diff(x**2 + 2*x + 1, x)\n"
        "2. For integration: Send the expression in the format 'integrate(expression, variable)'.\n"
        "   Example: integrate(x**2 + 2*x + 1, x)\n"
        "3. For limits: Send the expression in the format 'limit(expression, variable, point)'.\n"
        "   Example: limit((x**2 - 1)/(x - 1), x, 1)"
    )

# Function to handle the math queries
async def solve_expression(update: Update, context: CallbackContext):
    expression_text = update.message.text.strip()

    try:
        # Extract the operation and the expression
        if expression_text.startswith('diff'):
            operation = 'diff'
            expression_text = expression_text[5:-1].strip()
        elif expression_text.startswith('integrate'):
            operation = 'integrate'
            expression_text = expression_text[10:-1].strip()
        elif expression_text.startswith('limit'):
            operation = 'limit'
            expression_text = expression_text[6:-1].strip()
        else:
            await update.message.reply_text("Invalid input format. Please use /help for guidance.")
            return

        # Differentiation and Integration: Extract expression and variable
        if operation in ['diff', 'integrate']:
            expression, variable = expression_text.split(',')
            var = symbols(variable.strip())
            expr = sympify(expression.strip())

            # Perform differentiation or integration
            if operation == 'diff':
                result = diff(expr, var)
            elif operation == 'integrate':
                result = integrate(expr, var)

        # Limits: Extract expression, variable, and the point at which limit is calculated
        elif operation == 'limit':
            expression, variable, point = expression_text.split(',')
            var = symbols(variable.strip())
            expr = sympify(expression.strip())
            point = sympify(point.strip())

            # Perform limit calculation
            result = limit(expr, var, point)

        # Reply with the result
        await update.message.reply_text(f"The result of the operation is:\n{result}")

    except SympifyError:
        await update.message.reply_text("Invalid mathematical expression. Please check your input and try again.")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

# Main function to start the bot
def main():
    # Replace 'YOUR_TOKEN' with your bot's API token
    application = Application.builder().token('YOUR TOKEN').build()

    # Command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    # Message handler to process math expressions
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, solve_expression))

    # Start the bot
    application.run_polling()

if name == 'main':
    main()