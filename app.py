from flask import Flask, request, jsonify, render_template
from data.chart_data import initial_chart_data

app = Flask(__name__)

# ── 初期データを読み込む
current_chart_data = initial_chart_data

@app.route('/')
def index():
    """ ルートURLにアクセスがあった場合、現在のチャートデータで index.html を表示 """
    return render_template('index.html', chart_data=current_chart_data)

@app.route('/update', methods=['GET', 'POST'])
def update_chart():
    global current_chart_data

    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"status": "error", "message": "JSON を送ってください"}), 400
        received = request.get_json()
        if not isinstance(received, list):
            return jsonify({"status": "error", "message": "リスト形式で送ってください"}), 400

        current_chart_data = received
        print("▶ データを更新しました:", received)
        return jsonify({"status": "success"})

    else:
        return jsonify({"chart_data": current_chart_data})

if __name__ == '__main__':
    # debug=True なら print() がリアルタイムでターミナルに出ます
    app.run(debug=True, host='0.0.0.0', port=8000)