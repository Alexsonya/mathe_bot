"""Math problem generator for grades 5-9 (Russian school curriculum)."""

import random
from dataclasses import dataclass


@dataclass
class Task:
    question: str       # question text in German
    answer: str         # correct answer (string)
    options: list[str]  # 4 answer options
    topic: str          # topic key
    hint: str = ""      # optional hint
    explanation: str = ""  # explanation shown after answer
    difficulty: str = "mittel"  # leicht / mittel / schwer


# ---------------------------------------------------------------------------
# Grade 5: arithmetic, fractions basics, decimals, word problems
# ---------------------------------------------------------------------------

def _grade5() -> Task:
    generators = [_g5_arithmetic, _g5_order_of_ops, _g5_fractions_basic,
                  _g5_decimals, _g5_word_problem, _g5_divisibility]
    return random.choice(generators)()


def _g5_arithmetic() -> Task:
    op = random.choice(["+", "-", "*"])
    if op == "*":
        a, b = random.randint(12, 99), random.randint(2, 25)
    elif op == "+":
        a, b = random.randint(100, 9999), random.randint(100, 9999)
    else:
        a = random.randint(100, 9999)
        b = random.randint(10, a)
    result = eval(f"{a}{op}{b}")
    q = f"Berechne: {a} {op} {b} = ?"
    ops = {"+": "Addition", "-": "Subtraktion", "*": "Multiplikation"}
    return _make_task(q, result, "arithmetic", difficulty="leicht",
                      hint=f"Denke an die {ops[op]}.",
                      explanation=f"{a} {op} {b} = {result}")


def _g5_order_of_ops() -> Task:
    a, b, c = random.randint(2, 15), random.randint(2, 10), random.randint(1, 20)
    expr = f"{a} * {b} + {c}"
    result = a * b + c
    q = f"Berechne: {expr} = ?"
    return _make_task(q, result, "arithmetic", difficulty="leicht",
                      hint="Punkt vor Strich! Zuerst multiplizieren.",
                      explanation=f"Erst {a}×{b}={a*b}, dann +{c} = {result}")


def _g5_fractions_basic() -> Task:
    d = random.choice([2, 3, 4, 5, 6, 8, 10])
    n1 = random.randint(1, d - 1)
    n2 = random.randint(1, d - 1)
    while n1 + n2 >= d * 2:
        n2 = random.randint(1, d - 1)
    from fractions import Fraction
    f1, f2 = Fraction(n1, d), Fraction(n2, d)
    result = f1 + f2
    q = f"Berechne: {n1}/{d} + {n2}/{d} = ?"
    ans = f"{result.numerator}/{result.denominator}" if result.denominator != 1 else str(result.numerator)
    return _make_task_str(q, ans, "fractions", difficulty="leicht",
                          hint="Brüche mit gleichem Nenner: Zähler addieren.",
                          explanation=f"{n1}/{d} + {n2}/{d} = {ans}")


def _g5_decimals() -> Task:
    a = round(random.uniform(1, 50), 1)
    b = round(random.uniform(1, 50), 1)
    op = random.choice(["+", "-"])
    if op == "-" and b > a:
        a, b = b, a
    result = round(eval(f"{a}{op}{b}"), 1)
    q = f"Berechne: {a} {op} {b} = ?"
    return _make_task(q, result, "decimals", is_float=True, difficulty="leicht",
                      hint="Rechne wie mit ganzen Zahlen, achte auf das Komma.",
                      explanation=f"{a} {op} {b} = {result}")


def _g5_word_problem() -> Task:
    items = random.choice([
        ("Äpfel", "Birnen"), ("Bücher", "Hefte"),
        ("Jungen", "Mädchen"), ("rote Kugeln", "blaue Kugeln"),
    ])
    a = random.randint(12, 50)
    b = random.randint(5, a - 1)
    q = (f"In einer Kiste sind {a} {items[0]} und {b} {items[1]}. "
         f"Wie viele Stücke sind insgesamt in der Kiste?")
    return _make_task(q, a + b, "word_problems", difficulty="leicht",
                      hint="Addiere beide Mengen.",
                      explanation=f"{a} + {b} = {a+b}")


def _g5_divisibility() -> Task:
    n = random.randint(2, 12)
    m = random.randint(10, 30)
    product = n * m
    q = f"Ist {product} durch {n} teilbar? Wenn ja, was ist {product} ÷ {n}?"
    return _make_task(q, m, "arithmetic", difficulty="leicht",
                      hint=f"Teile {product} durch {n}.",
                      explanation=f"{product} ÷ {n} = {m}")


# ---------------------------------------------------------------------------
# Grade 6: percentages, negative numbers, ratios, simple equations
# ---------------------------------------------------------------------------

def _grade6() -> Task:
    generators = [_g6_percentages, _g6_negative, _g6_ratios,
                  _g6_simple_equation, _g6_fractions_mixed]
    return random.choice(generators)()


def _g6_percentages() -> Task:
    base = random.choice([50, 100, 150, 200, 250, 300, 400, 500])
    pct = random.choice([10, 20, 25, 30, 50, 75])
    result = base * pct / 100
    is_float = result != int(result)
    if not is_float:
        result = int(result)
    q = f"Wie viel sind {pct}% von {base}?"
    return _make_task(q, result, "percentages", difficulty="mittel",
                      is_float=is_float,
                      hint=f"Teile {base} durch 100 und multipliziere mit {pct}.",
                      explanation=f"{base} × {pct}/100 = {result}")


def _g6_negative() -> Task:
    a = random.randint(-20, -1)
    b = random.randint(-20, 20)
    op = random.choice(["+", "-", "*"])
    result = eval(f"({a}){op}({b})")
    q = f"Berechne: ({a}) {op} ({b}) = ?"
    return _make_task(q, result, "negative_numbers", difficulty="mittel",
                      hint="Achte auf die Vorzeichen!",
                      explanation=f"({a}) {op} ({b}) = {result}")


def _g6_ratios() -> Task:
    a, b = random.randint(2, 8), random.randint(2, 8)
    total = (a + b) * random.randint(3, 10)
    first_part = total * a // (a + b)
    q = (f"Teile {total} im Verhältnis {a}:{b}. "
         f"Wie groß ist der erste Teil?")
    return _make_task(q, first_part, "ratios", difficulty="mittel",
                      hint=f"Gesamt = {a}+{b} = {a+b} Teile.",
                      explanation=f"{total} × {a}/{a+b} = {first_part}")


def _g6_simple_equation() -> Task:
    x = random.randint(2, 20)
    a = random.randint(2, 10)
    b = a * x + random.randint(1, 30)
    c = b - a * x
    q = f"Löse die Gleichung: {a}x + {c} = {b}\nx = ?"
    return _make_task(q, x, "equations", difficulty="mittel",
                      hint=f"Bringe {c} auf die andere Seite und teile durch {a}.",
                      explanation=f"{a}x = {b} - {c} = {b-c}, x = {b-c}/{a} = {x}")


def _g6_fractions_mixed() -> Task:
    from fractions import Fraction
    d1 = random.choice([3, 4, 5, 6])
    d2 = d1
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    f1, f2 = Fraction(n1, d1), Fraction(n2, d2)
    op = random.choice(["*", "+"])
    if op == "*":
        result = f1 * f2
        q = f"Berechne: {n1}/{d1} × {n2}/{d2} = ?"
    else:
        result = f1 + f2
        q = f"Berechne: {n1}/{d1} + {n2}/{d2} = ?"
    ans = f"{result.numerator}/{result.denominator}" if result.denominator != 1 else str(result.numerator)
    return _make_task_str(q, ans, "fractions", difficulty="mittel",
                          hint="Brüche multiplizieren: Zähler×Zähler, Nenner×Nenner.",
                          explanation=f"{ans}")


# ---------------------------------------------------------------------------
# Grade 7: linear equations, powers, polynomials, basic geometry
# ---------------------------------------------------------------------------

def _grade7() -> Task:
    generators = [_g7_powers, _g7_linear_equation, _g7_geometry_triangle,
                  _g7_geometry_rectangle, _g7_polynomial]
    return random.choice(generators)()


def _g7_powers() -> Task:
    base = random.randint(2, 10)
    exp = random.randint(2, 4)
    result = base ** exp
    q = f"Berechne: {base}^{exp} = ?"
    return _make_task(q, result, "powers", difficulty="mittel",
                      hint=f"Multipliziere {base} mit sich selbst {exp}-mal.",
                      explanation=f"{base}^{exp} = {result}")


def _g7_linear_equation() -> Task:
    x = random.randint(-10, 10)
    while x == 0:
        x = random.randint(-10, 10)
    a = random.randint(2, 8)
    b = random.randint(1, 20)
    right_side = a * x + b
    q = f"Löse: {a}x + {b} = {right_side}\nx = ?"
    return _make_task(q, x, "equations", difficulty="mittel",
                      hint=f"Bringe {b} auf die andere Seite.",
                      explanation=f"{a}x = {right_side} - {b} = {right_side-b}, x = {right_side-b}/{a} = {x}")


def _g7_geometry_triangle() -> Task:
    a = random.randint(3, 15)
    h = random.randint(2, 12)
    area = a * h / 2
    q = (f"Berechne die Fläche eines Dreiecks.\n"
         f"Grundseite: {a} cm, Höhe: {h} cm\n"
         f"Fläche = ?")
    hint = "Formel: (Grundseite × Höhe) / 2"
    expl = f"{a} × {h} / 2 = {area}"
    if area == int(area):
        return _make_task(q, int(area), "geometry", suffix=" cm²",
                          hint=hint, explanation=expl, difficulty="mittel")
    else:
        return _make_task(q, area, "geometry", is_float=True, suffix=" cm²",
                          hint=hint, explanation=expl, difficulty="mittel")


def _g7_geometry_rectangle() -> Task:
    a = random.randint(3, 20)
    b = random.randint(3, 20)
    what = random.choice(["perimeter", "area"])
    if what == "perimeter":
        result = 2 * (a + b)
        q = f"Berechne den Umfang eines Rechtecks.\nSeiten: {a} cm und {b} cm\nUmfang = ?"
        return _make_task(q, result, "geometry", suffix=" cm",
                          hint="Formel: 2 × (a + b)",
                          explanation=f"2 × ({a} + {b}) = 2 × {a+b} = {result}",
                          difficulty="leicht")
    else:
        result = a * b
        q = f"Berechne die Fläche eines Rechtecks.\nSeiten: {a} cm und {b} cm\nFläche = ?"
        return _make_task(q, result, "geometry", suffix=" cm²",
                          hint="Formel: a × b",
                          explanation=f"{a} × {b} = {result}",
                          difficulty="leicht")


def _g7_polynomial() -> Task:
    a, b = random.randint(1, 5), random.randint(1, 5)
    result = a**2 + 2*a*b + b**2
    q = f"Vereinfache: ({a} + {b})² = ?"
    return _make_task(q, result, "powers", difficulty="mittel",
                      hint=f"({a}+{b})² = ({a}+{b}) × ({a}+{b})",
                      explanation=f"({a}+{b})² = {a+b}² = {result}")


# ---------------------------------------------------------------------------
# Grade 8: quadratic equations, Pythagorean theorem, roots, systems
# ---------------------------------------------------------------------------

def _grade8() -> Task:
    generators = [_g8_roots, _g8_pythagorean, _g8_quadratic,
                  _g8_system, _g8_circle]
    return random.choice(generators)()


def _g8_roots() -> Task:
    perfect = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
    result = int(perfect ** 0.5)
    q = f"Berechne: √{perfect} = ?"
    return _make_task(q, result, "roots", difficulty="leicht",
                      hint="Welche Zahl mal sich selbst ergibt diese Zahl?",
                      explanation=f"{result} × {result} = {perfect}, also √{perfect} = {result}")


def _g8_pythagorean() -> Task:
    triples = [(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15)]
    a, b, c = random.choice(triples)
    what = random.choice(["hyp", "leg"])
    if what == "hyp":
        q = (f"Satz des Pythagoras:\n"
             f"Katheten: {a} cm und {b} cm.\n"
             f"Wie lang ist die Hypotenuse?")
        return _make_task(q, c, "pythagorean", suffix=" cm", difficulty="schwer",
                          hint="a² + b² = c²",
                          explanation=f"{a}² + {b}² = {a**2} + {b**2} = {c**2}, √{c**2} = {c}")
    else:
        q = (f"Satz des Pythagoras:\n"
             f"Hypotenuse: {c} cm, eine Kathete: {a} cm.\n"
             f"Wie lang ist die andere Kathete?")
        return _make_task(q, b, "pythagorean", suffix=" cm", difficulty="schwer",
                          hint="b² = c² - a²",
                          explanation=f"{c}² - {a}² = {c**2} - {a**2} = {b**2}, √{b**2} = {b}")


def _g8_quadratic() -> Task:
    x1 = random.randint(1, 8)
    x2 = random.randint(1, 8)
    b_coeff = -(x1 + x2)
    c_coeff = x1 * x2
    b_str = f" - {abs(b_coeff)}x" if b_coeff < 0 else f" + {b_coeff}x"
    c_str = f" - {abs(c_coeff)}" if c_coeff < 0 else f" + {c_coeff}"
    q = f"Löse: x²{b_str}{c_str} = 0\nDie größere Lösung x = ?"
    return _make_task(q, max(x1, x2), "quadratic", difficulty="schwer",
                      hint="Finde zwei Zahlen, deren Summe und Produkt passen.",
                      explanation=f"x₁ = {min(x1,x2)}, x₂ = {max(x1,x2)}")


def _g8_system() -> Task:
    x, y = random.randint(1, 8), random.randint(1, 8)
    a1, b1 = random.randint(1, 4), random.randint(1, 4)
    c1 = a1 * x + b1 * y
    q = (f"Gleichungssystem:\n"
         f"{a1}x + {b1}y = {c1}\n"
         f"x - y = {x - y}\n"
         f"x = ?")
    return _make_task(q, x, "systems", difficulty="schwer",
                      hint="Drücke y durch x aus der 2. Gleichung aus.",
                      explanation=f"x = {x}, y = {y}")


def _g8_circle() -> Task:
    r = random.randint(2, 10)
    import math
    area = round(math.pi * r ** 2, 1)
    q = (f"Berechne die Fläche eines Kreises (π ≈ 3.14).\n"
         f"Radius: {r} cm\n"
         f"Fläche = ? (auf eine Dezimalstelle runden)")
    result = round(3.14 * r ** 2, 1)
    return _make_task(q, result, "geometry", is_float=True, suffix=" cm²",
                      difficulty="mittel",
                      hint="Formel: π × r²",
                      explanation=f"3.14 × {r}² = 3.14 × {r**2} = {result}")


# ---------------------------------------------------------------------------
# Grade 9: probability, sequences, functions, statistics
# ---------------------------------------------------------------------------

def _grade9() -> Task:
    generators = [_g9_probability, _g9_arithmetic_seq, _g9_geometric_seq,
                  _g9_linear_function, _g9_statistics]
    return random.choice(generators)()


def _g9_probability() -> Task:
    total = random.choice([6, 10, 12, 20, 36, 52])
    favorable = random.randint(1, total - 1)
    from fractions import Fraction
    prob = Fraction(favorable, total)
    q = (f"In einem Beutel sind {total} Kugeln, davon {favorable} rot.\n"
         f"Wie groß ist die Wahrscheinlichkeit, eine rote Kugel zu ziehen?\n"
         f"Antwort als Bruch:")
    ans = f"{prob.numerator}/{prob.denominator}" if prob.denominator != 1 else str(prob.numerator)
    return _make_task_str(q, ans, "probability", difficulty="mittel",
                          hint=f"P = günstige / mögliche = {favorable}/{total}",
                          explanation=f"{favorable}/{total} = {ans}")


def _g9_arithmetic_seq() -> Task:
    a1 = random.randint(1, 10)
    d = random.randint(1, 5)
    n = random.randint(5, 15)
    an = a1 + (n - 1) * d
    q = (f"Arithmetische Folge:\n"
         f"Erstes Glied a₁ = {a1}, Differenz d = {d}.\n"
         f"Berechne das {n}. Glied:")
    return _make_task(q, an, "sequences", difficulty="mittel",
                      hint=f"Formel: a₁ + (n-1) × d",
                      explanation=f"{a1} + ({n}-1) × {d} = {a1} + {(n-1)*d} = {an}")


def _g9_geometric_seq() -> Task:
    a1 = random.randint(1, 5)
    r = random.choice([2, 3])
    n = random.randint(3, 6)
    an = a1 * r ** (n - 1)
    q = (f"Geometrische Folge:\n"
         f"Erstes Glied a₁ = {a1}, Quotient q = {r}.\n"
         f"Berechne das {n}. Glied:")
    return _make_task(q, an, "sequences", difficulty="schwer",
                      hint=f"Formel: a₁ × q^(n-1)",
                      explanation=f"{a1} × {r}^{n-1} = {a1} × {r**(n-1)} = {an}")


def _g9_linear_function() -> Task:
    k = random.randint(1, 5)
    b = random.randint(-10, 10)
    x = random.randint(-5, 5)
    y = k * x + b
    q = (f"Lineare Funktion: f(x) = {k}x {'+' if b >= 0 else '-'} {abs(b)}\n"
         f"Berechne f({x}) = ?")
    return _make_task(q, y, "linear_functions", difficulty="mittel",
                      hint=f"Setze x = {x} in die Formel ein.",
                      explanation=f"f({x}) = {k}×{x} {'+' if b >= 0 else '-'} {abs(b)} = {y}")


def _g9_statistics() -> Task:
    numbers = [random.randint(1, 20) for _ in range(5)]
    avg = sum(numbers) / len(numbers)
    nums_str = ", ".join(str(n) for n in numbers)
    q = (f"Berechne den Mittelwert:\n"
         f"{nums_str}\n"
         f"Mittelwert = ?")
    if avg == int(avg):
        return _make_task(q, int(avg), "statistics", difficulty="leicht",
                          hint="Addiere alle Zahlen und teile durch die Anzahl.",
                          explanation=f"({'+'.join(str(n) for n in numbers)}) / {len(numbers)} = {int(avg)}")
    else:
        return _make_task(q, round(avg, 1), "statistics", is_float=True,
                          difficulty="leicht",
                          hint="Addiere alle Zahlen und teile durch die Anzahl.",
                          explanation=f"({'+'.join(str(n) for n in numbers)}) / {len(numbers)} = {round(avg,1)}")


# ---------------------------------------------------------------------------
# Knobelaufgaben (brain teasers) — no grade, just fun
# ---------------------------------------------------------------------------

def _knobel() -> Task:
    generators = [
        _knobel_matchsticks, _knobel_sequence_pattern, _knobel_age,
        _knobel_clock, _knobel_digits, _knobel_logic,
        _knobel_trick, _knobel_chess, _knobel_river,
        _knobel_coins, _knobel_speed, _knobel_cake,
    ]
    return random.choice(generators)()


def _knobel_matchsticks() -> Task:
    puzzles = [
        ("Bewege 1 Streichholz, damit die Gleichung stimmt:\n"
         "6 + 4 = 4\nWelche Gleichung entsteht?",
         "0 + 4 = 4",
         ["0 + 4 = 4", "6 - 4 = 2", "6 + 4 = 10", "1 + 4 = 5"],
         "Schau dir die 6 genauer an...",
         "Aus der 6 wird eine 0, wenn man ein Streichholz bewegt."),
        ("Aus 4 Streichhölzern kann man ein Quadrat legen.\n"
         "Wie viele Streichhölzer braucht man für 3 Quadrate in einer Reihe?",
         "10",
         ["10", "12", "8", "9"],
         "Benachbarte Quadrate teilen sich eine Seite.",
         "3 Quadrate in einer Reihe teilen 2 Seiten: 4+3+3 = 10."),
        ("Lege 6 Streichhölzer so, dass 4 gleichseitige Dreiecke entstehen.\n"
         "Welche Form hat die Figur?",
         "Tetraeder (Pyramide)",
         ["Tetraeder (Pyramide)", "Stern", "Hexagon", "Würfel"],
         "Denke dreidimensional!",
         "Ein Tetraeder hat 4 Dreiecksflächen und 6 Kanten."),
    ]
    q, ans, opts, hint, expl = random.choice(puzzles)
    random.shuffle(opts)
    return Task(question=q, answer=ans, options=opts, topic="knobel",
                hint=hint, explanation=expl, difficulty="schwer")


def _knobel_sequence_pattern() -> Task:
    patterns = [
        ("Welche Zahl fehlt?\n1, 1, 2, 3, 5, 8, 13, ?", 21,
         "Jede Zahl ist die Summe der zwei vorherigen.",
         "Fibonacci: 8 + 13 = 21"),
        ("Welche Zahl fehlt?\n2, 6, 18, 54, ?", 162,
         "Jede Zahl wird mit dem gleichen Faktor multipliziert.",
         "×3: 54 × 3 = 162"),
        ("Welche Zahl fehlt?\n1, 4, 9, 16, 25, ?", 36,
         "Das sind alles besondere Zahlen... n²",
         "Quadratzahlen: 6² = 36"),
        ("Welche Zahl fehlt?\n1, 3, 6, 10, 15, ?", 21,
         "Die Differenz wächst um 1: +2, +3, +4, +5...",
         "Dreieckszahlen: 15 + 6 = 21"),
        ("Welche Zahl fehlt?\n2, 3, 5, 7, 11, 13, ?", 17,
         "Diese Zahlen haben nur zwei Teiler.",
         "Primzahlen: nach 13 kommt 17"),
        ("Welche Zahl fehlt?\n1, 8, 27, 64, ?", 125,
         "Jede Zahl ist eine dritte Potenz.",
         "Kubikzahlen: 5³ = 125"),
    ]
    q, ans, hint, expl = random.choice(patterns)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="mittel")


def _knobel_age() -> Task:
    puzzles = [
        ("Anna ist doppelt so alt wie Ben.\n"
         "In 5 Jahren ist Anna 25.\n"
         "Wie alt ist Ben jetzt?",
         10, "Finde zuerst Annas Alter jetzt.",
         "Anna jetzt: 25-5=20. Ben = 20/2 = 10."),
        ("Ein Vater ist 4-mal so alt wie sein Sohn.\n"
         "In 20 Jahren wird er nur doppelt so alt sein.\n"
         "Wie alt ist der Sohn jetzt?",
         10, "Stelle zwei Gleichungen auf.",
         "V=4S und V+20=2(S+20) → 4S+20=2S+40 → S=10."),
        ("Maria ist 3 Jahre älter als Tom.\n"
         "Zusammen sind sie 29 Jahre alt.\n"
         "Wie alt ist Tom?",
         13, "T + (T+3) = 29",
         "2T + 3 = 29 → T = 13."),
        ("Oma ist 60 Jahre alt. Ihre Enkelin ist 12.\n"
         "Vor wie vielen Jahren war Oma 10-mal so alt wie die Enkelin?",
         6, "Vor x Jahren: Oma = 60-x, Enkelin = 12-x",
         "60-x = 10(12-x) → 60-x=120-10x → 9x=60 → x=6 (fast 7)."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="mittel")


def _knobel_clock() -> Task:
    puzzles = [
        ("Wie oft am Tag überlappen sich der Stunden- und der Minutenzeiger?",
         22, "Es passiert nicht genau jede Stunde...",
         "In 12h überlappen sie 11-mal (nicht 12!). Also 22 pro Tag."),
        ("Um 12:00 stehen beide Zeiger übereinander.\n"
         "Wann passiert das das nächste Mal?\n"
         "Ungefähr nach wie vielen Minuten?",
         65, "Der Minutenzeiger muss den Stundenzeiger einholen.",
         "Der Minutenzeiger holt ~5.5 Min/Std auf → 60/55×60 ≈ 65 Min."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="schwer")


def _knobel_digits() -> Task:
    puzzles = [
        ("Verwende die Ziffern 1, 2, 3 und die Rechenzeichen +, -, ×\n"
         "um genau 7 zu erhalten.\nWelche Rechnung stimmt?",
         "1 + 2 × 3",
         ["1 + 2 × 3", "1 × 2 + 3", "3 × 2 + 1", "3 + 2 + 1"],
         "Punkt vor Strich!", "1 + 2×3 = 1 + 6 = 7"),
        ("Wie viele zweistellige Zahlen gibt es,\n"
         "deren Quersumme 10 ist?\n"
         "(z.B. 19, 28, ...)",
         "9",
         ["9", "8", "10", "11"],
         "Zähle systematisch: 19, 28, 37...",
         "19, 28, 37, 46, 55, 64, 73, 82, 91 = 9 Zahlen."),
        ("Die Summe von 3 aufeinanderfolgenden Zahlen ist 99.\n"
         "Welche ist die mittlere Zahl?",
         "33",
         ["33", "32", "34", "31"],
         "Die mittlere Zahl ist der Durchschnitt.",
         "99 ÷ 3 = 33. Die Zahlen: 32, 33, 34."),
        ("Wie viele Nullen hat die Zahl 100! (Fakultät) am Ende?",
         "24",
         ["24", "20", "25", "10"],
         "Zähle die Faktoren 5 in 100!",
         "100/5=20, 100/25=4, 100/125=0 → 20+4 = 24 Nullen."),
    ]
    q, ans, opts, hint, expl = random.choice(puzzles)
    random.shuffle(opts)
    return Task(question=q, answer=ans, options=opts, topic="knobel",
                hint=hint, explanation=expl, difficulty="mittel")


def _knobel_logic() -> Task:
    puzzles = [
        ("3 Katzen fangen 3 Mäuse in 3 Minuten.\n"
         "Wie viele Katzen fangen 100 Mäuse in 100 Minuten?",
         3, "Jede Katze fängt 1 Maus in 3 Minuten...",
         "1 Katze = 1 Maus pro 3 Min. In 100 Min fängt jede ~33. Also 3 reichen für 100."),
        ("Du hast 8 gleich aussehende Kugeln. Eine ist schwerer.\n"
         "Wie oft musst du mindestens wiegen, um sie zu finden?",
         2, "Teile die Kugeln in 3 Gruppen.",
         "3+3+2: Wiege 3 gegen 3. Dann die schwere Gruppe nochmal teilen."),
        ("Du hast 12 gleich aussehende Kugeln. Eine ist anders schwer.\n"
         "Wie oft musst du mindestens wiegen?",
         3, "Jede Wiegung gibt 3 Ergebnisse: links, rechts, gleich.",
         "3 Wiegungen = 3³ = 27 Möglichkeiten, genug für 12 Kugeln."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="schwer")


def _knobel_trick() -> Task:
    puzzles = [
        ("Ein Ziegelstein wiegt 1 kg plus einen halben Ziegelstein.\n"
         "Wie viel wiegt der Ziegelstein?",
         2, "Stelle eine Gleichung auf: x = 1 + x/2",
         "x = 1 + x/2 → x/2 = 1 → x = 2 kg"),
        ("Ein Seil ist 30 Meter lang. Es wird in 3-Meter-Stücke geschnitten.\n"
         "Wie viele Schnitte braucht man?",
         9, "Anzahl Schnitte ≠ Anzahl Stücke!",
         "30/3 = 10 Stücke, aber nur 9 Schnitte nötig (n-1)."),
        ("Auf einem Teich wachsen Seerosen.\n"
         "Jeden Tag verdoppelt sich ihre Fläche.\n"
         "Am Tag 20 ist der Teich ganz bedeckt.\n"
         "An welchem Tag war er halb bedeckt?",
         19, "Wenn sich die Fläche jeden Tag verdoppelt...",
         "Verdopplung: halb bedeckt = einen Tag vorher = Tag 19."),
        ("Eine Schnecke klettert einen 10m-Brunnen hoch.\n"
         "Tag: 3m hoch. Nacht: 2m zurück.\n"
         "Nach wie vielen Tagen ist sie oben?",
         8, "Am letzten Tag muss sie nicht mehr zurückrutschen!",
         "7 Tage: je 1m netto = 7m. Tag 8: +3m = 10m, oben!"),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="schwer")


def _knobel_chess() -> Task:
    puzzles = [
        ("Wie viele Quadrate kann man auf einem Schachbrett zählen?\n"
         "(nicht nur die 64 kleinen!)",
         204, "Es gibt 1×1, 2×2, 3×3... bis 8×8 Quadrate.",
         "8²+7²+6²+...+1² = 64+49+36+25+16+9+4+1 = 204"),
        ("Auf ein Schachbrett werden Reiskörner gelegt:\n"
         "1 auf Feld 1, 2 auf Feld 2, 4 auf Feld 3...\n"
         "Wie viele Körner liegen auf dem 10. Feld?",
         512, "Jedes Feld hat doppelt so viele wie das vorherige.",
         "2^(n-1): 2^9 = 512 Körner auf Feld 10."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="schwer")


def _knobel_river() -> Task:
    puzzles = [
        ("Ein Bauer muss einen Wolf, eine Ziege und Kohl\n"
         "über einen Fluss bringen. Das Boot fasst nur 1 Ding.\n"
         "Wie oft muss er mindestens über den Fluss fahren?",
         7, "Die Ziege darf nie allein mit Wolf oder Kohl bleiben.",
         "Ziege hin, zurück, Wolf hin, Ziege zurück, Kohl hin, zurück, Ziege hin = 7."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="schwer")


def _knobel_coins() -> Task:
    puzzles = [
        ("Du hast genau 1,00 € in Münzen.\n"
         "Du hast genau 50 Münzen (1ct, 2ct, 5ct).\n"
         "Wie viele 5-Cent-Münzen hast du?",
         2, "Stelle ein Gleichungssystem auf.",
         "a+b+c=50, a+2b+5c=100. Durch Probieren: c=2."),
        ("Mit wie vielen verschiedenen Arten kann man\n"
         "10 Cent aus 1ct, 2ct und 5ct zusammensetzen?",
         10, "Beginne mit den größten Münzen.",
         "2×5ct(1), 1×5ct(3), 0×5ct(6) = 1+3+6 = 10 Arten."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="schwer")


def _knobel_speed() -> Task:
    puzzles = [
        ("Ein Zug fährt 100 km mit 50 km/h hin\n"
         "und 100 km mit 100 km/h zurück.\n"
         "Wie hoch ist die Durchschnittsgeschwindigkeit?\n"
         "(auf ganze Zahl runden)",
         67, "Durchschnitt ≠ (50+100)/2!",
         "Gesamtstrecke/Gesamtzeit: 200/(2+1) ≈ 66.7 → 67 km/h."),
        ("Zwei Züge fahren aufeinander zu.\n"
         "Abstand: 100 km. Zug A: 40 km/h, Zug B: 60 km/h.\n"
         "Nach wie vielen Minuten treffen sie sich?",
         60, "Addiere die Geschwindigkeiten!",
         "40+60=100 km/h zusammen. 100km ÷ 100km/h = 1h = 60 Min."),
        ("Lisa läuft 3 km in 20 Minuten.\n"
         "Tom läuft mit doppelter Geschwindigkeit.\n"
         "Wie lange braucht Tom für 6 km?",
         20, "Doppelte Geschwindigkeit, aber auch doppelte Strecke!",
         "Tom: 3km in 10 Min → 6km in 20 Min."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="mittel")


def _knobel_cake() -> Task:
    puzzles = [
        ("Mit 3 geraden Schnitten — wie viele Stücke\n"
         "kann man maximal aus einem Kuchen schneiden?",
         7, "Die Schnitte müssen sich nicht im Zentrum kreuzen!",
         "1 Schnitt→2, 2→4, 3→7 (wenn kein Schnitt parallel ist)."),
        ("8 Personen sitzen am runden Tisch.\n"
         "Jeder gibt jedem einmal die Hand.\n"
         "Wie viele Handschläge gibt es?",
         28, "Formel: n×(n-1)/2",
         "8×7/2 = 28 Handschläge."),
    ]
    q, ans, hint, expl = random.choice(puzzles)
    return _make_task(q, ans, "knobel", hint=hint, explanation=expl,
                      difficulty="mittel")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

GRADE_GENERATORS = {
    5: _grade5,
    6: _grade6,
    7: _grade7,
    8: _grade8,
    9: _grade9,
    0: _knobel,  # 0 = Knobelaufgaben
}


def generate_task(grade: int, difficulty: str | None = None) -> Task:
    """Generate a random math task for the given grade (0=Knobel).

    If difficulty is set, retry up to 10 times to match it.
    """
    gen = GRADE_GENERATORS.get(grade, _grade5)
    if difficulty is None:
        return gen()
    for _ in range(10):
        task = gen()
        if task.difficulty == difficulty:
            return task
    return gen()  # fallback


def generate_daily() -> Task:
    """Generate today's daily challenge — same for all users."""
    import hashlib
    from datetime import date
    today = date.today().isoformat()
    seed = int(hashlib.md5(today.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed)
    grade = rng.choice([0, 7, 8, 9])
    gen = GRADE_GENERATORS.get(grade, _knobel)
    old_state = random.getstate()
    random.seed(seed)
    task = gen()
    random.setstate(old_state)
    return task


def _make_task(q: str, result, topic: str, is_float: bool = False,
               suffix: str = "", hint: str = "", explanation: str = "",
               difficulty: str = "mittel") -> Task:
    """Create a Task with numeric answer and generated wrong options."""
    if is_float:
        answer = str(round(float(result), 1))
    else:
        answer = str(int(result))

    options = _generate_options(result, is_float)
    options_str = [f"{o}{suffix}" for o in options]
    return Task(question=q, answer=f"{answer}{suffix}",
                options=options_str, topic=topic,
                hint=hint, explanation=explanation, difficulty=difficulty)


def _make_task_str(q: str, answer: str, topic: str,
                   hint: str = "", explanation: str = "",
                   difficulty: str = "mittel") -> Task:
    """Create a Task with string answer (e.g. fractions)."""
    # Generate plausible wrong fraction answers
    if "/" in answer:
        num, den = map(int, answer.split("/"))
        wrong = set()
        for delta in [-2, -1, 1, 2, 3]:
            candidate = f"{num + delta}/{den}"
            if candidate != answer and num + delta > 0:
                wrong.add(candidate)
        for delta in [-1, 1]:
            candidate = f"{num}/{den + delta}"
            if candidate != answer and den + delta > 1:
                wrong.add(candidate)
        wrong_list = list(wrong)[:3]
        while len(wrong_list) < 3:
            wrong_list.append(f"{num + len(wrong_list) + 2}/{den}")
        options = wrong_list + [answer]
    else:
        options = [answer, str(int(answer) + 1),
                   str(int(answer) - 1), str(int(answer) + 2)]

    random.shuffle(options)
    return Task(question=q, answer=answer, options=options, topic=topic,
                hint=hint, explanation=explanation, difficulty=difficulty)


def _generate_options(correct, is_float: bool = False) -> list[str]:
    """Generate 4 options including the correct answer."""
    correct_val = float(correct) if is_float else int(correct)
    wrong = set()

    # Add nearby wrong answers
    for offset in [1, -1, 2, -2, 3, -3, 5, 10, -10]:
        candidate = correct_val + offset
        if is_float:
            candidate = round(candidate, 1)
        else:
            candidate = int(candidate)
        if candidate != correct_val:
            wrong.add(candidate)

    # Also add some percentage-based offsets
    if abs(correct_val) > 10:
        for factor in [0.9, 1.1, 0.8]:
            candidate = correct_val * factor
            if is_float:
                candidate = round(candidate, 1)
            else:
                candidate = int(candidate)
            if candidate != correct_val:
                wrong.add(candidate)

    wrong_list = sorted(wrong, key=lambda x: abs(x - correct_val))[:3]

    if is_float:
        options = [str(round(w, 1)) for w in wrong_list] + [str(round(correct_val, 1))]
    else:
        options = [str(int(w)) for w in wrong_list] + [str(int(correct_val))]

    random.shuffle(options)
    return options
