import os
import webbrowser
import time
from flask import Flask, request, jsonify
from opentok import Client, OutputModes, MediaModes, ArchiveModes, Roles
from dotenv import load_dotenv
from threading import Timer

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("VIDEO_PROJECT_API_KEY")
API_SECRET = os.getenv("VIDEO_PROJECT_API_SECRET")
EC_URL = os.getenv("VIDEO_EXPERIENCE_COMPOSER_URL")

opentok = Client(API_KEY, API_SECRET)


def error_response(e):
    return jsonify({"ERROR": str(e)}),


@app.route("/manage")
def ec_manage():
    html = open("manage.html").read()
    return html


@app.route("/create-session", methods=["POST"])
def create_session():
    try:
        session = opentok.create_session(
            media_mode=MediaModes.routed,
            archive_mode=ArchiveModes.manual
        )
        session_id = session.session_id
        token = opentok.generate_token(
            session_id=session_id,
            role=Roles.moderator,
            expire_time=int(time.time()) + 300
        )
        return jsonify({
            "sessionId": session_id,
            "token": token
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/start-composer", methods=["POST"])
def start_composer():
    data = request.get_json()
    session_id = data.get("sessionId")
    token = data.get("token")
    try:
        composer = opentok.start_render(
            session_id=session_id,
            opentok_token=token,
            url=EC_URL,
            max_duration=3600
        )
        return jsonify({
            "composerId": composer.id,
            "status": composer.status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stop-composer", methods=["POST"])
def stop_composer():
    data = request.get_json()
    composer_id = data.get("composerId")
    try:
        opentok.stop_render(composer_id)
    except Exception as e:
        if "204" in str(e):
            return jsonify({"message": f"Composer {composer_id} stopped (204)."})
        return jsonify({"error": str(e)}), 500


@app.route("/start-archive", methods=["POST"])
def start_archive():
    data = request.get_json()
    session_id = data.get("sessionId")
    try:
        archive = opentok.start_archive(
            session_id=session_id,
            name="ec test",
            output_mode=OutputModes.composed
        )
        return jsonify({
            "archiveId": archive.id,
            "status": archive.status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stop-archive", methods=["POST"])
def stop_archive():
    data = request.get_json()
    archive_id = data.get("archiveId")
    try:
        archive = opentok.stop_archive(archive_id)
        return jsonify({
            "archiveId": archive.id,
            "status": archive.status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/start-broadcast", methods=["POST"])
def start_broadcast():
    data = request.get_json()
    session_id = data.get("sessionId")
    try:
        broadcast = opentok.start_broadcast(
            session_id=session_id,
            options={
                "outputs": {"hls": {"dvr": False, "lowLatency": True}},
                # "outputs": {
                #     "hls": {
                #         "dvr": False,
                #         "lowLatency": True
                #     },
                #     "rtmp": [{
                #         "id": "YOUTUBE",
                #         "serverUrl": "rtmp://a.rtmp.youtube.com/live2",
                #         "streamName": "srfc-..."
                #     }]
                # },
                "max_duration": 3600,
                "resolution": "1280x720",
            }
        )
        return jsonify({
            "broadcastId": broadcast.id,
            "status": broadcast.status,
            "hlsUrl": broadcast.broadcastUrls["hls"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/stop-broadcast", methods=["POST"])
def stop_broadcast():
    data = request.get_json()
    broadcast_id = data.get("broadcastId")
    try:
        broadcast = opentok.stop_broadcast(broadcast_id)
        return jsonify({
            "broadcastId": broadcast.id,
            "status": broadcast.status
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def open_browser():
    webbrowser.open_new("http://localhost:5000/manage")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(port=5000, debug=True, use_reloader=False)
