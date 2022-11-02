class Ponto:
    def __init__(self, x, y, z, restricaoLinearX, restricaoLinearY, restricaoLinearZ,
                 restricaoRotacaoX, restricaoRotacaoY, restricaoRotacaoZ):
        self.x = x
        self.y = y
        self.z = z

        self.restricaoLinearX = restricaoLinearX
        self.restricaoLinearY = restricaoLinearY
        self.restricaoLinearZ = restricaoLinearZ

        self.restricaoRotacaoX = restricaoRotacaoX
        self.restricaoRotacaoY = restricaoRotacaoY
        self.restricaoRotacaoZ = restricaoRotacaoZ

        self.cargas = [0,0,0,0,0,0]

        self.deslocamentosPrescritos = []

    #0, 1 e 2 -> linear x, y e z
    #3, 4 e 5 -> momento x, y e z
    def adicionarCarga(self, valor, tipo):
        self.cargas[tipo] += valor

    def adicionarDeslocamentoPrescrito(self, deslocamento):
        self.deslocamentosPrescritos.append(deslocamento)
