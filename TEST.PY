from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('template.html')  # 確保 template.html 存在

if __name__ == '__main__':
    app.run(debug=True)
