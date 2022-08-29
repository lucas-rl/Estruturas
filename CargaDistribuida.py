class CargaDistribuida:
    def __init__(self, distanciaNoInicio, comprimento, valor, tipo):
        self.distanciaNoInicio = distanciaNoInicio
        self.comprimento = comprimento
        self.valor = valor
        #0=força em x / 1=força em y / 2=força em z
        #3=momento em x / 4=momento em y / 5=momento em z
        self.tipo = tipo
        