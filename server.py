#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for, session
from flask_httpauth import HTTPBasicAuth
from bot import Bot
import threading


app = Flask(__name__, static_url_path="")
auth = HTTPBasicAuth()
app.session_count = 0
chat_bot_dict = {}
id_accept = {}
app.secret_key = b'112_5#y2L"F4Q8z\n\xec]/'


@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'admin'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/hello/', methods=['GET'])
def hello():
    return "hello"

"""
server : client post câu nói, chatbot xử lý và chuyển node và đưa ra Speak
"""
@app.route('/say/', methods=['POST'])
@auth.login_required
def get_tasks():
    if not request.is_json:
        return abort(400)
    sentence = request.get_json()['sentence']
    if sentence is None:
        return abort(400)
    if 'id_session' not in session or id_accept.get(session['id_session']) is None:
        app.session_count += 1
        print(app.session_count)
        session['id_session'] = app.session_count
        id_accept[app.session_count] = 1
        chat_bot_dict[session['id_session']] = Bot()
    chat_bot = chat_bot_dict[session['id_session']]
    chat_bot.reset_time()
    answer = chat_bot.next_sentence(sentence)
    print(answer)
    id_session = session['id_session']
    return jsonify({"sentence": answer, "id_session": id_session})

"""
Luồng check client không hoạt động, sẽ thực hiện xóa chat_bot tương ứng trong hệ thống
"""
def thread_check_live_time():
    while True:
        for key, value in chat_bot_dict.items():
            if value.check_over_time():
                id_accept.pop(key)
                chat_bot_dict.pop(key)
                print("REMOVE: ", key)
                break


if __name__ == '__main__':
    threading.Thread(name="check_live_time", target=thread_check_live_time).start()
    app.run(debug=True, host="10.198.41.31", port=5000)
