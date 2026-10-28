from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Core Business Logic for Push 1
def calculate_metrics(marks_list):
    if not marks_list:
        return 0, 0
    total = sum(marks_list)
    average = total / len(marks_list)
    return total, round(average, 2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Student Grade Calculator</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }
        .container { max-width: 500px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { color: #333; }
        input[type="text"] { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background-color: #2b7a78; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background-color: #172a3a; }
        .result { margin-top: 20px; padding: 15px; background-color: #e8f1f5; border-radius: 4px; color: #172a3a; }
    </style>
</head>
<body>
<div class="container">
    <h2>Student Grade Calculator (v1: Metrics)</h2>
    <form method="POST">
        <label>Enter Marks (comma-separated, e.g., 85,90,78):</label>
        <input type="text" name="marks" placeholder="85, 90, 78" required value="{{ input_marks }}">
        <button type="submit">Calculate</button>
    </form>
    
    {% if error %}
        <div class="result" style="background-color: #f8d7da; color: #721c24;">{{ error }}</div>
    {% elif total is not none %}
        <div class="result">
            <strong>Total Marks:</strong> {{ total }} <br>
            <strong>Average Marks:</strong> {{ average }}
        </div>
    {% endif %}
</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    total, average = None, None
    error = None
    input_marks = ""
    if request.method == 'POST':
        input_marks = request.form.get('marks', '')
        try:
            marks_list = [float(x.strip()) for x in input_marks.split(',') if x.strip()]
            total, average = calculate_metrics(marks_list)
        except ValueError:
            error = "Invalid input! Please enter numbers separated strictly by commas."
            
    return render_template_string(HTML_TEMPLATE, total=total, average=average, error=error, input_marks=input_marks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
