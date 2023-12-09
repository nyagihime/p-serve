#!/home/pi/app/venv/bin/python
# -*- config: utf-8 -*-
from bottle import Bottle, route, get, HTTPResponse, static_file, run, request
import base64, io, re, json
from pathlib import Path
from PIL import Image, ImageDraw

# 設定用JSONのロード
with open('settings.json', 'r', encoding='utf-8') as cf: SETTINGS = json.load(cf)

# このファイルを起点として、相対パスでファイルを定義する
path_here = Path(__file__)
ROOT = path_here.parent
VUE_DIST = f'{ROOT}/dist'

# Bottle インスタンス作成
server = Bottle()
server.config['autojson'] = True

# ----------------------------------------
# for Vue artifacts
# ----------------------------------------
# 静的ファイルはそのまま返す
# assets
# (assets 以外にもなんかあるなら適宜追加）
@server.route('/assets/<name:path>')
def assets(name):
    return static_file(name, root=f'{VUE_DIST}/assets')

# favicon
@server.route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root=f'{VUE_DIST}')

@server.route('/')
@server.route('/<:re:.*>')
def index():
    return static_file('index.html', root=f'{VUE_DIST}')


# ----------------------------------------
# for API
# ----------------------------------------

from brother_ql import BrotherQLRaster, create_label
from brother_ql.backends import backend_factory, guess_backend

commonApiHeaders = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
}

# ラベルサイズの一覧を返す
@server.get('/api/help/size')
def get_supported_label_sizes():
    data = {
        'status': 'ok',
        'message': 'supported label sizes.',
        'data': []
    }

    res = HTTPResponse(
        status=200,
        body=json.dumps(data, ensure_ascii=False, indent=2),
        headers=commonApiHeaders
    )
    return res

# 印刷処理
@server.post('/api/print')
def print_req():
    # 印刷するラベルのサイズ
    size = request.forms.get('size')

    # 自動でカットするかどうか
    auto_cut = request.forms.get('auto_cut', True)


    # 印刷データ（Base64エンコードされた画像データ）
    b64data = request.forms.get('image')
    # base64 のヘッダーを削除してからバイト列にエンコード
    image_data_bytes = re.sub('^data:image/.+;base64,', '', b64data).encode('utf-8')
    # バイト列を base64 としてデコード
    image_data = base64.b64decode(image_data_bytes)
    # デコードしたデータをファイルとして開いて Pillow の Image インスタンスを生成
    image_instance = Image.open(io.BytesIO(image_data))

    # BrotherQLRaster インスタンスを生成
    qlr = BrotherQLRaster(SETTINGS['printer']['model'])
    create_label(
        qlr,
        image_instance,
        label_size=size,
        red=False,
        threshold=SETTINGS['printer']['threshold'],
        cut=auto_cut
    )

    printer_path = f"usb://{SETTINGS['printer']['idVendor']}:{SETTINGS['printer']['idProduct']}/{SETTINGS['printer']['iSerial']}"
    selected_backend = guess_backend(printer_path)
    backend_class = backend_factory(selected_backend)['backend_class']

    try:
        backend = backend_class(printer_path)
        backend.write(qlr.data)
        backend.dispose()

        response_msg = {
            'status': 'ok',
            'message': 'your request is accepted.'
        }
    except Exception as e:
        response_msg = {
            'status': 'error',
            'message': str(e)
        }

    res = HTTPResponse(
        status=200,
        body=json.dumps(response_msg, ensure_ascii=False, indent=2),
        headers=commonApiHeaders
    )
    return res

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=SETTINGS['bottle']['port'], debug=True, reloader=True)