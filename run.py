from flask import Flask, request, render_template_string

app = Flask(__name__)

abjad_values = {
    'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1,
    'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'ة': 5,
    'و': 6, 'ؤ': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ى': 10, 'ئ': 10, 'ی': 10,
    'ك': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60,
    'ع': 70, 'ف': 80, 'ص': 90, 'ق': 100, 'ر': 200,
    'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600,
    'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000
}

def calculate_abjad_value(text):
    return sum(abjad_values.get(char, 0) for char in text)

def generate_odd_magic_square(n):
    square = [[0] * n for _ in range(n)]
    num, i, j = 1, 0, n // 2
    while num <= n * n:
        square[i][j] = num
        num += 1
        newi, newj = (i - 1) % n, (j + 1) % n
        if square[newi][newj]:
            i += 1
        else:
            i, j = newi, newj
    return square

def generate_doubly_even_magic_square(n):
    square = [[(n * y) + x + 1 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if (i % 4 == j % 4) or ((i % 4 + j % 4) == 3):
                square[i][j] = (n * n + 1) - square[i][j]
    return square

def generate_singly_even_magic_square(n):
    half = n // 2
    sub = generate_odd_magic_square(half)
    square = [[0] * n for _ in range(n)]
    add = [0, 2, 3, 1]
    for i in range(half):
        for j in range(half):
            for k in range(4):
                r = i + (k // 2) * half
                c = j + (k % 2) * half
                square[r][c] = sub[i][j] + add[k] * half * half
    k = (n - 2) // 4
    for i in range(n):
        for j in range(n):
            if (i < half and (j < k or j >= n - k)) or (i >= half and (k <= j < n - k)):
                if not (i == half and j == k):
                    square[i][j], square[i - half][j] = square[i - half][j], square[i][j]
    return square

def generate_magic_square(n):
    if n % 2 == 1:
        return generate_odd_magic_square(n)
    elif n % 4 == 0:
        return generate_doubly_even_magic_square(n)
    else:
        return generate_singly_even_magic_square(n)

def scale_magic_square(square, multiplier):
    return [[val * multiplier for val in row] for row in square]

def recommend_waffaq_type(value):
    for size in range(3, 20):
        cells = size * size
        if value % cells == 0:
            multiplier = value // cells
            square = generate_magic_square(size)
            scaled = scale_magic_square(square, multiplier)
            return size, multiplier, scaled
    return None, None, None

def format_magic_square(square):
    return "\n".join("<tr>" + "".join(f"<td>{val}</td>" for val in row) + "</tr>" for row in square)

@app.route("/", methods=["GET", "POST"])
def index():
    text = request.form.get("text", "")
    value = size = multiplier = table = None
    if text:
        value = calculate_abjad_value(text)
        size, multiplier, square = recommend_waffaq_type(value)
        table = format_magic_square(square) if square else None
    return render_template_string('''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Waffaq - توليد الوفق</title>
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      font-family: 'Arial', sans-serif;
      margin: 0;
      padding: 20px;
      background-color: #f2f2f2;
      text-align: center;
      direction: rtl;
    }

    .container {
      max-width: 800px;
      margin: auto;
      background: white;
      padding: 20px;
      border-radius: 12px;
      box-shadow: 0 0 10px rgba(0,0,0,0.1);
    }

    h2 {
      color: #333;
      margin-bottom: 10px;
    }

    textarea {
      width: 100%;
      height: 150px;
      font-size: 16px;
      padding: 10px;
      border-radius: 8px;
      border: 1px solid #ccc;
      resize: vertical;
    }

    button {
      margin-top: 15px;
      padding: 10px 20px;
      font-size: 16px;
      background-color: #007BFF;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
    }

    button:hover {
      background-color: #0056b3;
    }

    table {
      margin: 20px auto;
      border-collapse: collapse;
      width: 100%;
      max-width: 500px;
    }

    td {
      border: 1px solid #000;
      padding: 10px;
      width: 50px;
      text-align: center;
    }

    @media (max-width: 600px) {
      td {
        padding: 8px;
        width: 40px;
      }

      textarea {
        height: 120px;
        font-size: 14px;
      }

      button {
        width: 100%;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <h2>🔢 حساب الوفاق</h2>
    <p>أدخل نصًا عربيًا ثم اضغط "احسب"</p>
<form method="post">
  <textarea name="text">{{ text or "" }}</textarea><br><br>
  <div class="button-group">
    <button type="submit">احسب</button>
    <button type="button" onclick="window.location.href='/'">مسح</button>
  </div>
</form>



    {% if value %}
      <h3>📘 القيمة العددية: <span style="color:blue;">{{ value }}</span></h3>
      {% if size and multiplier %}
        <h4>📐 نوع الوفق: {{ size }}x{{ size }}</h4>
        <h4>📊 معامل الضرب: {{ multiplier }}</h4>
        <table>{{ table|safe }}</table>
      {% endif %}
    {% endif %}
  </div>
</body>
</html>
''', text=text, value=value, size=size, multiplier=multiplier, table=table)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1010, debug=True)
