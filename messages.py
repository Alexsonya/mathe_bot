"""German UI messages for the math quiz bot (B1-B2 level)."""

WELCOME = (
    "Willkommen beim Mathe-Quiz! 🎓\n\n"
    "Hier kannst du deine Mathematik-Kenntnisse testen.\n"
    "Wähle eine Klassenstufe und löse spannende Aufgaben!\n\n"
    "Befehle:\n"
    "/start — Startseite\n"
    "/quiz — Neue Aufgabe\n"
    "/klasse — Klassenstufe wählen\n"
    "/tagesaufgabe — Aufgabe des Tages 📅\n"
    "/punkte — Deine Punktzahl\n"
    "/hilfe — Hilfe anzeigen"
)

HELP = (
    "📚 So funktioniert der Bot:\n\n"
    "1. Wähle deine Klassenstufe (5–9) oder Knobelaufgaben\n"
    "2. Wähle den Schwierigkeitsgrad\n"
    "3. Du bekommst eine Mathe-Aufgabe\n"
    "4. Nutze 💡 Hinweis wenn du Hilfe brauchst\n"
    "5. Nach der Antwort siehst du eine Erklärung\n"
    "6. Drücke ➡️ für die nächste Aufgabe\n\n"
    "Befehle:\n"
    "/quiz — Neue Aufgabe bekommen\n"
    "/klasse — Klassenstufe ändern\n"
    "/tagesaufgabe — Aufgabe des Tages 📅\n"
    "/punkte — Punktestand anzeigen\n"
    "/zuruecksetzen — Punkte zurücksetzen"
)

CHOOSE_GRADE = "Wähle deine Klassenstufe:"

GRADE_SET = "Klassenstufe {grade} ausgewählt! ✅\nSchreibe /quiz, um eine Aufgabe zu bekommen."

NO_GRADE = "Bitte wähle zuerst eine Klassenstufe mit /klasse."

CORRECT = [
    "Richtig! ✅ Sehr gut gemacht!",
    "Super! ✅ Das ist korrekt!",
    "Genau richtig! ✅ Weiter so!",
    "Perfekt! ✅ Du bist auf dem richtigen Weg!",
    "Toll! ✅ Das stimmt!",
]

WRONG = "Leider falsch. ❌\nDie richtige Antwort ist: {answer}"

SCORE = (
    "📊 Dein Punktestand:\n\n"
    "Klassenstufe: {grade}\n"
    "Richtige Antworten: {correct}\n"
    "Gesamte Aufgaben: {total}\n"
    "Erfolgsquote: {rate}%"
)

SCORE_RESET = "Punkte wurden zurückgesetzt! 🔄"

NO_SCORE = "Du hast noch keine Aufgaben gelöst. Starte mit /quiz!"

TASK_HEADER = "📝 Klasse {grade} — Aufgabe\n\n"

TOPIC_NAMES = {
    "arithmetic": "Grundrechenarten",
    "fractions": "Brüche",
    "decimals": "Dezimalzahlen",
    "percentages": "Prozentrechnung",
    "equations": "Gleichungen",
    "geometry": "Geometrie",
    "powers": "Potenzen",
    "roots": "Wurzeln",
    "quadratic": "Quadratische Gleichungen",
    "probability": "Wahrscheinlichkeit",
    "sequences": "Zahlenfolgen",
    "word_problems": "Textaufgaben",
    "knobel": "Knobelaufgabe",
    "negative_numbers": "Negative Zahlen",
    "ratios": "Verhältnisse",
    "linear_functions": "Lineare Funktionen",
    "systems": "Gleichungssysteme",
    "pythagorean": "Satz des Pythagoras",
    "statistics": "Statistik",
}
