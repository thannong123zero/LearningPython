import qrcode
import io
from PIL import Image, ImageDraw, ImageFont


def GenerateQRCode(qr_model):
    if qr_model is None or qr_model.content is None or qr_model.fillColor is None or qr_model.backgroundColor is None or qr_model.size < 1:
        print("Invalid QR model")
        return
    elif qr_model.text is not None and qr_model.fontSize < 10 or qr_model.text is not None and  qr_model.textColor is None:
        print("Invalid QR model")
        return
    # Generate QR code
    qr = qrcode.QRCode(
        version=5,  # Controls the QR code size
        error_correction = qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size = qr_model.size,
        border = qr_model.border,
    )
    qr.add_data(qr_model.content)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color = qr_model.fillColor, back_color = qr_model.backgroundColor).convert("RGB")

    # Load and resize logo
    if qr_model.logo is not None:
        logo = Image.open(qr_model.logo)
        qr_size = qr_img.size[0]
        logo_size = qr_size // 4  # Set logo size to 1/4th of QR code size
        logo = logo.resize((logo_size, logo_size))
        
        # Paste the logo in the center
        pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    # Add text below the QR code
    if qr_model.text is not None:
        new_height = qr_img.size[1] + qr_model.fontSize + (qr_model.border * qr_model.size) # Extra space for text
        qr_code_image = Image.new("RGB", (qr_img.size[0], new_height), qr_model.backgroundColor)
        qr_code_image.paste(qr_img, (0, 0))
        
        # Draw text
        draw = ImageDraw.Draw(qr_code_image)
        if qr_model.fontFamily is  None:
            font = ImageFont.load_default()
        else:
            try:
                # Load a better font (Optional: Download a TTF font)
                font = ImageFont.truetype(qr_model.fontFamily, qr_model.fontSize)
            except IOError:
                # Use default font if custom font is unavailable
                font = ImageFont.load_default()

        # Calculate text position
        text_width, text_height = draw.textbbox((0, 0), qr_model.text, font=font)[2:]
        text_x = (qr_code_image.size[0] - text_width) // 2
        if qr_model.border < 1:
            text_y = qr_img.size[1] + 5  # Below the QR code
        else:
            text_y = qr_img.size[1] 

        draw.text((text_x, text_y), qr_model.text, fill=qr_model.textColor, font=font)

        # Save the final QR code to a byte array
        byte_arr = io.BytesIO()
        qr_code_image.save(byte_arr, format='PNG')
        byte_arr = byte_arr.getvalue()
        return byte_arr
    else:
        # Save the final QR code to a byte array
        byte_arr = io.BytesIO()
        qr_img.save(byte_arr, format='PNG')
        byte_arr = byte_arr.getvalue()
        return byte_arr