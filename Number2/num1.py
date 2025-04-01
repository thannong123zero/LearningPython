
import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_custom_qr(
    url, logo_path, text, size=300, border=4,
    qr_color="black", bg_color="white", text_color="black",
    output_path="custom_qr_code.png"
):
    # Create QR code
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=size // 50,  # Adjust size
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create QR code image
    qr_img = qr.make_image(fill=qr_color, back_color=bg_color).convert("RGB")

    # Load and resize logo
    logo = Image.open(logo_path)
    logo_size = qr_img.size[0] // 4  # Logo size (1/4 of QR size)
    logo = logo.resize((logo_size, logo_size))

    # Paste logo in center
    pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
    qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    # Add text below the QR code
    new_height = qr_img.size[1] + 50  # Extra space for text
    qr_with_text = Image.new("RGB", (qr_img.size[0], new_height), bg_color)
    qr_with_text.paste(qr_img, (0, 0))

    # Draw text
    draw = ImageDraw.Draw(qr_with_text)
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Custom font
    except IOError:
        font = ImageFont.load_default()  # Default font if arial.ttf is missing

    # Calculate text position
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    text_x = (qr_with_text.size[0] - text_width) // 2
    text_y = qr_img.size[1] + 10  # Below QR

    draw.text((text_x, text_y), text, fill=text_color, font=font)

    # Save QR code
    qr_with_text.save(output_path)
    print(f"QR Code saved at: {output_path}")

# Example Usage
generate_custom_qr(
    url="https://chatgpt.com/",
    logo_path="logo.png",
    text="Chat GPT",
    size=400,
    border=6,
    qr_color="blue",
    bg_color="white",
    text_color="red"
)
