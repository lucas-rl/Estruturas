class Secao:
    def __init__(self, altura, largura):
        self.altura = altura
        self.largura = largura
        self.Ax = largura * altura
        self.Ix = largura**3 * altura / 12 + largura * altura**3 / 12
        self.Iy = largura**3 * altura / 12
        self.Iz = largura * altura**3 / 12
        