import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_qr_with_logo_text(url, logo_path, text, output_path="qr_with_logo_text.png"):
    # Generate QR code
    qr = qrcode.QRCode(
        version=5,  # Controls the QR code size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill_color="#ffffff", back_color="#ee04f2").convert("RGB")

    # Load and resize logo
    logo = Image.open(logo_path)
    qr_size = qr_img.size[0]
    logo_size = qr_size // 4  # Set logo size to 1/4th of QR code size
    logo = logo.resize((logo_size, logo_size))

    # Paste the logo in the center
    pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
    qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    # Add text below the QR code
    new_height = qr_img.size[1] + 50  # Extra space for text
    qr_with_text = Image.new("RGB", (qr_img.size[0], new_height), "white")
    qr_with_text.paste(qr_img, (0, 0))

    # Draw text
    draw = ImageDraw.Draw(qr_with_text)

    try:
        # Load a better font (Optional: Download a TTF font)
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        # Use default font if custom font is unavailable
        font = ImageFont.load_default()

    # Calculate text position
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    text_x = (qr_with_text.size[0] - text_width) // 2
    text_y = qr_img.size[1] + 10  # Below the QR code

    draw.text((text_x, text_y), text, fill="black", font=font)

    # Save the final QR code
    qr_with_text.save(output_path)
    print(f"QR Code saved at: {output_path}")

# Example usage
generate_qr_with_logo_text("https://chatgpt.com/", "logo.png", "Chat GPT")

