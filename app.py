from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import qrcode

app = Flask(__name__)
CORS(app)

# temporary storage
bookings = []

# 🔍 Check availability
@app.route('/check', methods=['POST'])
def check():
    data = request.json

    for b in bookings:
        if b['room'] == data['room'] and b['time'] == data['time']:
            return jsonify({"status": "busy"})

    return jsonify({"status": "available"})


# ✅ Book + Generate QR
@app.route('/book', methods=['POST'])
def book():
    data = request.json

    # Save booking
    bookings.append(data)

    # QR content
    qr_data = f"Classroom: {data['room']}\nTime: {data['time']}"

    # Generate QR
    img = qrcode.make(qr_data)
    img.save("qr.png")

    return jsonify({
        "status": "success",
        "message": "Booking confirmed"
    })


# 📱 Show QR image
@app.route('/qr.png')
def get_qr():
    return send_file("qr.png", mimetype='image/png')


# ▶ Run server
if __name__ == '__main__':
    app.run(debug=True)