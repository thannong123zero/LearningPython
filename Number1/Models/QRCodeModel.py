class QRCodeModel:
    def __init__(self, content, logo = None, text = None, fontFamily = None,
                  size = 1, border = 0, fontSize = 16, fillColor="#000000", backgroundColor="#ffffff", textColor="#ffffff"):
        self.content = content
        self.size = size
        self.logo = logo
        self.text = text
        self.fontSize = fontSize
        self.textColor = textColor
        self.backgroundColor = backgroundColor
        self.fillColor = fillColor
        self.fontFamily = fontFamily
        self.border = border
