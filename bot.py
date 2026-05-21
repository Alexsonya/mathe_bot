#!/usr/bin/env python3
"""Telegram Math Quiz Bot — German interface, grades 5-9."""

import os
import random
import logging

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes,
)

from math_tasks import generate_task, generate_daily
from messages import (
    WELCOME, HELP, CHOOSE_GRADE, GRADE_SET, NO_GRADE,
    CORRECT, WRONG, SCORE_RESET, NO_SCORE,
    TASK_HEADER, TOPIC_NAMES,
    STREAK_LINE, STREAK_RECORD, SCORE_BEST_STREAK,
)

load_dotenv()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

DIFFICULTY_LABELS = {"leicht": "🟢 Leicht", "mittel": "🟡 Mittel", "schwer": "🔴 Schwer"}

# -- User data keys --
KEY_GRADE = "grade"
KEY_STATS = "stats"
KEY_ANSWER = "current_answer"
KEY_HINT = "current_hint"
KEY_EXPLANATION = "current_explanation"
KEY_QUESTION = "current_question"
KEY_DIFFICULTY = "difficulty"
KEY_DAILY_DATE = "daily_date"
KEY_STREAK = "streak"
KEY_BEST_STREAK = "best_streak"


def _get_stats(ctx, grade) -> dict:
    if KEY_STATS not in ctx.user_data:
        ctx.user_data[KEY_STATS] = {}
    stats = ctx.user_data[KEY_STATS]
    key = str(grade)
    if key not in stats:
        stats[key] = {"correct": 0, "total": 0}
    return stats[key]


# -- Command handlers --

async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME)


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP)


async def cmd_choose_grade(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(f"Klasse {g}", callback_data=f"grade_{g}")]
        for g in range(5, 10)
    ]
    keyboard.append(
        [InlineKeyboardButton("🧩 Knobelaufgaben", callback_data="grade_0")]
    )
    await update.message.reply_text(
        CHOOSE_GRADE, reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def cb_set_grade(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    grade = int(query.data.split("_")[1])
    ctx.user_data[KEY_GRADE] = grade
    label = "🧩 Knobelaufgaben" if grade == 0 else f"Klasse {grade}"

    # Show difficulty selection
    keyboard = [
        [InlineKeyboardButton(v, callback_data=f"diff_{k}")]
        for k, v in DIFFICULTY_LABELS.items()
    ]
    keyboard.append([InlineKeyboardButton("🎲 Zufällig", callback_data="diff_any")])

    await query.edit_message_text(
        f"{label} ausgewählt! ✅\nWähle den Schwierigkeitsgrad:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def cb_set_difficulty(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    diff = query.data.removeprefix("diff_")
    ctx.user_data[KEY_DIFFICULTY] = None if diff == "any" else diff
    diff_label = DIFFICULTY_LABELS.get(diff, "🎲 Zufällig")
    await query.edit_message_text(
        f"Schwierigkeit: {diff_label} ✅\n"
        f"Schreibe /quiz für eine Aufgabe!"
    )


async def cmd_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    grade = ctx.user_data.get(KEY_GRADE)
    if grade is None:
        await update.message.reply_text(NO_GRADE)
        return

    difficulty = ctx.user_data.get(KEY_DIFFICULTY)
    task = generate_task(grade, difficulty=difficulty)
    await _send_task(update.message, ctx, task, grade)


async def cmd_daily(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the daily challenge."""
    from datetime import date
    today = date.today().isoformat()

    if ctx.user_data.get(KEY_DAILY_DATE) == today:
        await update.message.reply_text(
            "Du hast die Tagesaufgabe schon gelöst! 📅\n"
            "Morgen gibt es eine neue."
        )
        return

    task = generate_daily()
    ctx.user_data[KEY_DAILY_DATE] = today
    ctx.user_data[KEY_GRADE] = ctx.user_data.get(KEY_GRADE)  # keep grade

    # Build text
    text = "📅 Aufgabe des Tages\n\n"
    topic_label = TOPIC_NAMES.get(task.topic, task.topic)
    text += f"Thema: {topic_label}\n"
    diff_label = DIFFICULTY_LABELS.get(task.difficulty, task.difficulty)
    text += f"Schwierigkeit: {diff_label}\n\n"
    text += task.question

    ctx.user_data[KEY_ANSWER] = task.answer
    ctx.user_data[KEY_HINT] = task.hint
    ctx.user_data[KEY_EXPLANATION] = task.explanation
    ctx.user_data[KEY_QUESTION] = text

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"ans_{opt}")]
        for opt in task.options
    ]
    if task.hint:
        keyboard.append([InlineKeyboardButton("💡 Hinweis", callback_data="hint")])

    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def _send_task(message, ctx, task, grade) -> None:
    """Format and send a task."""
    ctx.user_data[KEY_ANSWER] = task.answer
    ctx.user_data[KEY_HINT] = task.hint
    ctx.user_data[KEY_EXPLANATION] = task.explanation

    topic_label = TOPIC_NAMES.get(task.topic, task.topic)
    diff_label = DIFFICULTY_LABELS.get(task.difficulty, task.difficulty)

    if grade == 0:
        text = f"🧩 Knobelaufgabe | {diff_label}\n\n"
    else:
        text = TASK_HEADER.format(grade=grade)
        text += f"Thema: {topic_label} | {diff_label}\n\n"
    text += task.question

    ctx.user_data[KEY_QUESTION] = text

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"ans_{opt}")]
        for opt in task.options
    ]
    if task.hint:
        keyboard.append([InlineKeyboardButton("💡 Hinweis", callback_data="hint")])

    await message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def cb_hint(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Show hint without removing answer buttons."""
    query = update.callback_query
    hint = ctx.user_data.get(KEY_HINT, "")
    if hint:
        await query.answer(f"💡 {hint}", show_alert=True)
    else:
        await query.answer("Kein Hinweis verfügbar.", show_alert=True)


async def cb_answer(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user_answer = query.data.removeprefix("ans_")
    correct_answer = ctx.user_data.get(KEY_ANSWER, "")
    explanation = ctx.user_data.get(KEY_EXPLANATION, "")

    grade = ctx.user_data.get(KEY_GRADE, 5)
    st = _get_stats(ctx, grade)
    st["total"] += 1

    streak = ctx.user_data.get(KEY_STREAK, 0)
    best = ctx.user_data.get(KEY_BEST_STREAK, 0)

    if user_answer == correct_answer:
        st["correct"] += 1
        streak += 1
        response = random.choice(CORRECT)
        if streak > best:
            best = streak
            if streak >= 3:
                response += f"\n{STREAK_RECORD}"
    else:
        streak = 0
        response = WRONG.format(answer=correct_answer)

    ctx.user_data[KEY_STREAK] = streak
    ctx.user_data[KEY_BEST_STREAK] = best

    # Add explanation
    if explanation:
        response += f"\n\n📖 Erklärung: {explanation}"

    # Stats
    grade_label = "Knobel" if grade == 0 else f"Klasse {grade}"
    response += f"\n\n📊 {grade_label}: {st['correct']}/{st['total']}"
    if streak >= 2:
        response += f"\n{STREAK_LINE.format(streak=streak)}"

    # "Next task" button
    keyboard = [[InlineKeyboardButton("➡️ Nächste Aufgabe", callback_data="next")]]

    await query.edit_message_text(
        response, reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def cb_next(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate next task inline."""
    query = update.callback_query
    await query.answer()

    grade = ctx.user_data.get(KEY_GRADE)
    if grade is None:
        await query.edit_message_text(NO_GRADE)
        return

    difficulty = ctx.user_data.get(KEY_DIFFICULTY)
    task = generate_task(grade, difficulty=difficulty)

    # Edit old message to just show "—"
    await query.edit_message_text("—")

    # Send new task as a new message
    await _send_task(query.message, ctx, task, grade)


async def cmd_score(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    stats = ctx.user_data.get(KEY_STATS, {})
    if not stats:
        await update.message.reply_text(NO_SCORE)
        return

    lines = ["📊 Dein Punktestand:\n"]
    total_correct = 0
    total_all = 0

    for key in sorted(stats.keys(), key=lambda x: int(x)):
        st = stats[key]
        if st["total"] == 0:
            continue
        rate = round(st["correct"] / st["total"] * 100)
        label = "Knobel" if key == "0" else f"Klasse {key}"
        lines.append(f"  {label}: {st['correct']}/{st['total']} ({rate}%)")
        total_correct += st["correct"]
        total_all += st["total"]

    if total_all > 0:
        total_rate = round(total_correct / total_all * 100)
        lines.append(f"\n  Gesamt: {total_correct}/{total_all} ({total_rate}%)")

    best = ctx.user_data.get(KEY_BEST_STREAK, 0)
    if best > 0:
        lines.append(f"  {SCORE_BEST_STREAK.format(best=best)}")

    await update.message.reply_text("\n".join(lines))


async def cmd_reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    ctx.user_data[KEY_STATS] = {}
    ctx.user_data[KEY_STREAK] = 0
    ctx.user_data[KEY_BEST_STREAK] = 0
    await update.message.reply_text(SCORE_RESET)


def main() -> None:
    if not TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set.")
        print("Copy .env.example to .env and add your token from @BotFather.")
        return

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("hilfe", cmd_help))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("klasse", cmd_choose_grade))
    app.add_handler(CommandHandler("quiz", cmd_quiz))
    app.add_handler(CommandHandler("tagesaufgabe", cmd_daily))
    app.add_handler(CommandHandler("daily", cmd_daily))
    app.add_handler(CommandHandler("punkte", cmd_score))
    app.add_handler(CommandHandler("zuruecksetzen", cmd_reset))
    app.add_handler(CommandHandler("reset", cmd_reset))

    # Callbacks
    app.add_handler(CallbackQueryHandler(cb_set_grade, pattern=r"^grade_\d$"))
    app.add_handler(CallbackQueryHandler(cb_set_difficulty, pattern=r"^diff_"))
    app.add_handler(CallbackQueryHandler(cb_hint, pattern=r"^hint$"))
    app.add_handler(CallbackQueryHandler(cb_next, pattern=r"^next$"))
    app.add_handler(CallbackQueryHandler(cb_answer, pattern=r"^ans_"))

    logger.info("Bot started!")
    app.run_polling()


if __name__ == "__main__":
    main()
