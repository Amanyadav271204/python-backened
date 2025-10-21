# server.py
from flask import Flask, request
from flask_socketio import SocketIO
import base64
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

connected_users = ""  # { sid: username }
@app.route('/')
def home():
    print("Server is running")
    return"hello "
@socketio.on('connect')
def handle_connect():
    print(f"Client connected")

datas=[{'sender':'vivek','msg':'hello sir ji ','receiver':'yash'},
{'sender': 'aman', 'msg': 'good morning', 'receiver': 'yash'},
{'sender': 'aman', 'msg': 'name is vivek', 'receiver': 'vivek'}
       ]

@socketio.on('fetch_data')
def retrieve_data():
    print("📤 Sending fetch_data_response")
    socketio.emit('fetch_data_response', datas)

@socketio.on('send_data')
def get_data(data):
    datas.append(data)
    socketio.emit('fetch_data_response',datas)

all_users = []

@socketio.on('personal_detail')
def get_data(data):
    username = data.get('name')
    if username not in all_users:
        all_users.append(username)

    # Prepare list of objects with id and username
    users_for_emit = [{'id': str(i+1), 'username': name} for i, name in enumerate(all_users)]

    # Emit to all clients
    socketio.emit("username_is", users_for_emit)

@socketio.on('upload_pdf')
def handle_upload(data):
    name = data['name']
    base64_data = data['data']

    # Remove the "data:application/pdf;base64," prefix if present
    if ',' in base64_data:
        base64_data = base64_data.split(',')[1]

    file_bytes = base64.b64decode(base64_data)
    with open(name, 'wb') as f:
        f.write(file_bytes)
    print(f"Saved PDF: {name}")
    socketio.emit('encoded_base64',{'name':name,'data':base64_data})


if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 9600)), app)
