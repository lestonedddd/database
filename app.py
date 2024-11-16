from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 解決跨域問題

# 配置 MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/employees_db"
mongo = PyMongo(app)
db = mongo.db

# 首頁路由
@app.route("/")
def index():
    return render_template("index.html")

# 獲取所有員工資料
@app.route("/api/employees", methods=["GET"])
def get_employees():
    employees = list(db.employees.find({}, {"_id": 0}))  # 不返回 _id
    return jsonify(employees)

# 新增員工
@app.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.json
    db.employees.insert_one(data)
    return jsonify({"message": "Employee added successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)
