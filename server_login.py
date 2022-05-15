from flask import Flask, render_template, request, jsonify

import io

def build(app, filepath):
    # query login data from file
    with io.open(filepath, "r") as ifile:
        data = ifile.readlines()
        database = [tuple(l.strip().split()) for l in data if l.strip() != ""]
        print(database)
        
    @app.route("/login")
    def login_html():
        return render_template("client_login.html")
        
    @app.route("/auth", methods=["POST"])
    def authenticate():
        data = request.get_json()
        found = any( (data["username"] == u and data["password"]) == p for u, p in database )
        # print([(u, p, data["username"] == u and data["password"] == p) for u, p in database], found)
        return jsonify(found=found)
    

if __name__ == '__main__':
    app = Flask(__name__, template_folder="html")
    # blueprint = flask.Blueprint('websocket_server', __name__, template_folder=template_path)
    build(app, "database.txt")
    print(app.url_map)
    app.run(debug=True)