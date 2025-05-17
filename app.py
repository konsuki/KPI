from flask import Flask, Response, request, stream_with_context, render_template, abort
import queue

app = Flask(__name__)

# デフォルトのチャートデータ (初期表示用、またはPOSTデータがない場合に使用)
# POSTされるJSONの形式に合わせてキーを定義しておくと良いでしょう
initial_chart_data = [
    {
        # 階層1: 代表
        "id": "代表かず",
        "parent": "",
        "cssClass": "ceo-content",
        "title": "代表かず",
        "rinen": "1番になる",             # D列
        "mokuhyo": "年商100億",           # E列
        "kpi": "売上3億",                # F列
        "tasseiRitsu": 300000000,        # G列
        "tooltip": ""
    },
    {
        # 階層2: 統括（セールスチーム）
        "id": "セールスチーム",
        "parent": "代表かず",
        "cssClass": "team-b-content",
        "title": "セールスチーム",
        "rinen": "誰よりも稼ぐ",
        "mokuhyo": "年商200億",
        "kpi": "売上4億",
        "tasseiRitsu": 400000000,
        "tooltip": ""
    },
    {
        # 階層3: チーム内1 – セールス上野
        "id": "セールス上野",
        "parent": "セールスチーム",
        "cssClass": "sub-b-content",
        "title": "セールス上野",
        "rinen": "成約率を上げる(上野)",
        "mokuhyo": "見込みありの成約率100%",
        "kpi": "成約率",
        "tasseiRitsu": 100,
        "tooltip": ""
    },
    {
        # 階層3: チーム内1 – セールス帆風
        "id": "セールス帆風",
        "parent": "セールスチーム",
        "cssClass": "sub-b-content",
        "title": "セールス帆風",
        "rinen": "セールス機会を最大化する(帆風)",
        "mokuhyo": "日程確定率を45%にする",
        "kpi": "日程確定率",
        "tasseiRitsu": 43,
        "tooltip": ""
    },
    {
        # 階層2: 統括（ライター高橋）
        "id": "ライター高橋",
        "parent": "代表かず",
        "cssClass": "team-e-content",
        "title": "ライター高橋",
        "rinen": "SEOを独占する",
        "mokuhyo": "10位以内を自社記事にする",
        "kpi": "記事作成50本",
        "tasseiRitsu": 0.5,
        "tooltip": ""
    },
    {
        # 階層3: チーム内1 – 前田さん
        "id": "前田さん",
        "parent": "ライター高橋",
        "cssClass": "sub-e-content",
        "title": "前田さん",
        "rinen": "前田の理念",
        "mokuhyo": "前田の目標",
        "kpi": "記事作成10本(物販サーチ)",
        "tasseiRitsu": 10,
        "tooltip": ""
    },
    {
        # 階層3: チーム内1 – パンちゃんさん
        "id": "パンちゃんさん",
        "parent": "ライター高橋",
        "cssClass": "sub-e-content",
        "title": "パンちゃんさん",
        "rinen": "パンちゃんの理念",
        "mokuhyo": "パンちゃんの目標",
        "kpi": "記事作成10本(もえか)",
        "tasseiRitsu": 10,
        "tooltip": ""
    },
]

# グローバル変数などで最新のデータを保持（デモ用、実際のアプリではDBなどを使う方が良い）
current_chart_data = initial_chart_data

# SSE 用にクライアントごとのキューを保持
clients = []

@app.route('/')
def index():
    """ ルートURLにアクセスがあった場合、現在のチャートデータで index.html を表示 """
    # templatesフォルダ内の index.html をレンダリングして返す
    # chart_data という名前でテンプレートにデータを渡す
    return render_template('index.html', chart_data=current_chart_data)

# ① SSE ストリーム用エンドポイント
@app.route('/stream')
def stream():
    def event_stream(q):
        try:
            while True:
                data = q.get()         # queue に何か入るまでブロック
                yield f"data: {data}\n\n"
        except GeneratorExit:
            pass

    q = queue.Queue()
    clients.append(q)
    # text/event-stream でレスポンスを返す
    return Response(stream_with_context(event_stream(q)),
                    mimetype='text/event-stream')

# ② チャート更新エンドポイント（POST）
@app.route('/update', methods=['POST'])
def update_chart():
    global current_chart_data
    if not request.is_json:
        abort(400, "Request must be JSON")
    received = request.get_json()
    # 🔽 ここで毎回 JSON 内容をターミナルに出力
    print("▶ 受信したJSONデータ:")
    print(received)

    if not isinstance(received, list):
        abort(400, "Expected list")
    current_chart_data = received

    # クライアント全員に「reload」イベントをキューイング
    for q in clients:
        q.put('reload')
    
    # ✅ 更新成功メッセージを出力
    print("✅ データが更新されました！")

    # レスポンスは 204（No Content）で OK
    return render_template('index.html', chart_data=current_chart_data)

if __name__ == '__main__':
    # debug=True なら print() がリアルタイムでターミナルに出ます
    app.run(debug=True, host='0.0.0.0', port=8000)