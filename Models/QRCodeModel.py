class QRCodeModel:
    def __init__(self, content, logo_path = None, text = None, font_family = None, size = 1, border = 0, font_size = 16, fill_color="#000000", back_color="#ffffff", text_color="#ffffff"):
        self.content = content
        self.logo_path = logo_path
        self.text = text
        self.fill_color = fill_color
        self.back_color = back_color
        self.text_color = text_color
        self.font_size = font_size
        self.font_family = font_family
        self.size = size
        self.border = border
