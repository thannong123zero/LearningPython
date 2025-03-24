from flask import Flask,  request, send_file, jsonify
from Services.QRCodeGenerator import GenerateQRCode
from Models.QRCodeModel import QRCodeModel
import io
app = Flask(__name__)

@app.route('/api/generateqrcode', methods=['POST'])  # Fixed 'Post' -> 'POST'
def GenerateQRCodeAPI():
    try:
        # Parse form data from request
        data = request.form
        logo_file = request.files.get("Logo")  # Get file (if provided)
        if not data:
            return jsonify({'error': 'Invalid form input'}), 400  # Return error for missing input

         # Read logo file into memory (if provided)
        logo_bytes = None
        if logo_file:
            logo_bytes = io.BytesIO(logo_file.read())  # Store image in memory
            logo_bytes.seek(0)  # Reset stream position

        # Create QRCodeModel instance from received data
        qr_model = QRCodeModel(
            content=data.get("Content", None),
            logo=logo_bytes,
            text=data.get("Text", None),
            size=int(data.get("Size", 5)),
            border=int(data.get("Border", 1)),
            fontSize=int(data.get("FontSize", 16)),
            fontFamily=data.get("FontFamily", "arial.ttf"),
            fillColor=data.get("FillColor", "#000000"),
            backgroundColor=data.get("BackgroundColor", "#ffffff"),
            textColor=data.get("TextColor", "#000000")
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