from flask import Flask,  request, send_file, jsonify
from Services.QRCodeGenerator import GenerateQRCode
from Models.QRCodeModel import QRCodeModel
import io
app = Flask(__name__)

@app.route('/Index', methods=['GET'])
def IndexAPI():
    # Define QR Code properties using the model
    qr_model = QRCodeModel(
        content="https://www.example.com",
        logo_path="logo.png",
        text="Scan the QR code",
        size=5,
        border=1,
        font_size=16,
        font_family="arial.ttf",
        fill_color="#000000",
        back_color="#ffffff",
        text_color="#000000"
    )

    # Generate QR Code (ensure this function returns bytes)
    byte_array = GenerateQRCode(qr_model)

    # Convert byte array to a BytesIO stream
    qr_stream = io.BytesIO(byte_array)

    # Reset stream position to the beginning
    qr_stream.seek(0)

    # Return the QR code image
    return send_file(
        qr_stream,
        mimetype='image/png',
        as_attachment=True,
        download_name='qrcode.png'  # Corrected for Flask 2.x+
    )

@app.route('/GenerateQRCode', methods=['POST'])  # Fixed 'Post' -> 'POST'
def GenerateQRCodeAPI():
    try:
        # Parse JSON input from request body
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON input'}), 400  # Return error for missing input

        # Create QRCodeModel instance from received data
        qr_model = QRCodeModel(
            content=data.get("content", None),
            logo_path=data.get("logo_path", None),
            text=data.get("text", None),
            size=data.get("size", 5),
            border=data.get("border", 1),
            font_size=data.get("font_size", 16),
            font_family=data.get("font_family", "arial.ttf"),
            fill_color=data.get("fill_color", "#000000"),
            back_color=data.get("back_color", "#ffffff"),
            text_color=data.get("text_color", "#000000")
        )

        # Generate QR Code (ensure this function returns bytes)
        byte_array = GenerateQRCode(qr_model)

        # Convert byte array to a BytesIO stream
        qr_stream = io.BytesIO(byte_array)
        qr_stream.seek(0)  # Reset stream position

        # Return QR code image as response
        return send_file(
            qr_stream,
            mimetype='image/png',
            as_attachment=True,
            download_name='qrcode.png'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return server error

if __name__ == '__main__':
    app.run(debug=True)