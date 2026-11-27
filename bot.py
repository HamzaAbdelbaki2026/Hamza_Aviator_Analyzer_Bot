import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

results = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 مرحبا بك في Hamza Aviator Analyzer!\n\n"
        "📊 /add 2.5 - إضافة نتيجة\n"
        "📈 /stats - الإحصائيات\n"
        "🗑 /reset - مسح النتائج"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        value = float(context.args[0])

        if value <= 0:
            raise ValueError

        results.append(value)

        await update.message.reply_text(
            f"✅ تمت إضافة النتيجة: {value}x"
        )

    except (IndexError, ValueError):
        await update.message.reply_text(
            "استعمل هكذا: /add 2.5"
        )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not results:
        await update.message.reply_text("لا توجد نتائج بعد.")
        return

    average = sum(results) / len(results)
    highest = max(results)
    lowest = min(results)

    message = (
        "📊 إحصائيات النتائج\n\n"
        f"🔢 عدد النتائج: {len(results)}\n"
        f"📈 المتوسط: {average:.2f}x\n"
        f"⬆️ أعلى نتيجة: {highest}x\n"
        f"⬇️ أقل نتيجة: {lowest}x\n"
        f"🔻 أقل من 2x: {sum(x < 2 for x in results)}\n"
        f"🔺 2x أو أكثر: {sum(x >= 2 for x in results)}"
    )

    await update.message.reply_text(message)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    results.clear()
    await update.message.reply_text("🗑 تم مسح النتائج.")

def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN غير موجود")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("reset", reset))

    app.run_polling()

if __name__ == "__main__":
    main()
