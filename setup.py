from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/list-sessions', methods=['GET'])
def list_sessions():
    try:
        uiautomator2
        # รันคำสั่ง `tmux list-sessions` เพื่อดึง Session ทั้งหมด
        result = subprocess.run(['tmux', 'list-sessions'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            return jsonify({
                'status': 'error',
                'msg': 'Failed to list sessions',
                'error': result.stderr
            }), 500
        
        # แปลงผลลัพธ์ให้เป็นรายการของ Session
        sessions = result.stdout.strip().split('\n')
        return jsonify({
            'status': 'success',
            'msg': 'Sessions listed successfully',
            'sessions': sessions
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': 'An error occurred',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
