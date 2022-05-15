from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit

def build(app, socketio):
    # attempt to build necessary components to a Flask app
    client_dict = {}
    
    @app.route("/chat")
    def client():
        return render_template("client_chat.html")
    
    @socketio.on('connect')
    def send_connect(cnt):
        print("[{}] Connection started.".format(request.sid))
        client_dict[request.sid] = {"name": None}
    
    @socketio.on('send')
    def verify_client_send(data):
        # print("Sent data from client: " + data)
        client = client_dict[request.sid]
        if(client["name"]):
            # has a valid name; allow broadcast. Use sid for client to filter its own chat.
            message = "{}: {}".format(client["name"], data)
            emit('broadcast', {"msg": message, "sid": request.sid}, broadcast=True)
            print("[{}] broadcasted: {}".format(request.sid, message))
        else:
            # doesn't have a name, check for format
            if("client_id:" == data[:10]):
                # correct prefix, check if name is valid
                name = data.split(":")[-1].strip()
                if(name):
                    # correct format; throw them the client and told them they are good
                    emit('response_good', {"name": name, "sid": request.sid})
                    client["name"] = name
                    print("[{}] registered with name `{}`".format(request.sid, name))
                    return
            # wrong format
            emit('response_fail')
            print("[{}] send wrong registering payload `{}`".format(request.sid, data))

    @socketio.on('disconnect')
    def disconnect():
        client_dict.pop(request.sid, None)
        print("[{}] Connection ended.".format(request.sid))

if __name__ == '__main__':
    # blueprint = flask.Blueprint('websocket_server', __name__, template_folder=template_path)
    app = Flask(__name__, template_folder="html")
    app.config['SECRET_KEY'] = 'secret_websocket_server'
    socketio = SocketIO(app)
    build(app, socketio)
    print(app.url_map)
    socketio.run(app, debug=True)
    # app.run()