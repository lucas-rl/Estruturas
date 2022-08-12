import numpy as np
from cargaConcentrada import CargaConcentrada
from ponto import *

class Barra:
    def __init__(self, inicio, fim, E, G, Ax, Ix, Iy, Iz, alfa):
        self.inicio = inicio
        self.fim = fim
        self.comprimento = ((inicio.x - fim.x)**2 + (inicio.y - fim.y)**2 + (inicio.z - fim.z)**2)**(1/2)
        self.E = E
        self.G = G
        self.Ax = Ax
        self.Ix = Ix
        self.Iy = Iy
        self.Iz = Iz
        self.alfa = np.radians(alfa)
        self.cargas = []
        self.matriz = [
            [E*Ax/self.comprimento, 0,0,0,0,0, -E*Ax/self.comprimento, 0,0,0,0,0],
            [0, 12*E*Iz/self.comprimento**3, 0,0,0, 6*E*Iz/self.comprimento**2, 0, -12*E*Iz/self.comprimento**3, 0,0,0, 6*E*Iz/self.comprimento**2],
            [0,0, 12*E*Iy/self.comprimento**3, 0, -6*E*Iy/self.comprimento**2, 0,0,0, -12*E*Iy/self.comprimento**3, 0, -6*E*Iy/self.comprimento**2, 0],
            [0,0,0, G*Ix/self.comprimento, 0,0,0,0,0, -G*Ix/self.comprimento, 0,0],
            [0,0, -6*E*Iy/self.comprimento**2, 0, 4*E*Iy/self.comprimento, 0,0,0, 6*E*Iy/self.comprimento**2, 0, 2*E*Iy/self.comprimento, 0],
            [0, 6*E*Iz/self.comprimento**2, 0,0,0, 4*E*Iz/self.comprimento, 0, -6*E*Iz/self.comprimento**2, 0,0,0, 2*E*Iz/self.comprimento],
            [-E*Ax/self.comprimento, 0,0,0,0,0, E*Ax/self.comprimento, 0,0,0,0,0],
            [0, -12*E*Iz/self.comprimento**3, 0,0,0, -6*E*Iz/self.comprimento**2, 0, 12*E*Iz/self.comprimento**3, 0,0,0, -6*E*Iz/self.comprimento**2],
            [0,0, -12*E*Iy/self.comprimento**3, 0, 6*E*Iy/self.comprimento**2, 0,0,0, 12*E*Iy/self.comprimento**3, 0, 6*E*Iy/self.comprimento**2, 0],
            [0,0,0, -G*Ix/self.comprimento, 0,0,0,0,0, G*Ix/self.comprimento, 0,0],
            [0,0, -6*E*Iy/self.comprimento**2, 0, 2*E*Iy/self.comprimento, 0,0,0, 6*E*Iy/self.comprimento**2, 0, 4*E*Iy/self.comprimento, 0],
            [0, 6*E*Iz/self.comprimento**2, 0,0,0, 2*E*Iz/self.comprimento, 0, -6*E*Iz/self.comprimento**2, 0,0,0, 4*E*Iz/self.comprimento]
        ]    
        
    def matrizR(self):
        Cx = (self.fim.x - self.inicio.x)/self.comprimento
        Cy = (self.fim.y - self.inicio.y)/self.comprimento
        Cz = (self.fim.z - self.inicio.z)/self.comprimento
        Cxy = (Cx**2 + Cy**2)**(1/2)
        cosa = np.cos(self.alfa)
        sena = np.sin(self.alfa)
        if self.inicio.x == self.fim.x and self.inicio.y == self.fim.y:
            R = [
                [0, Cz, 0],
                [-Cz*cosa, 0, sena],
                [Cz*sena, 0, cosa]
                ]
        else:
            R = [
                [Cx, Cy, Cz],
                [(-Cx*Cy*cosa - Cz*sena)/Cxy, Cxy*cosa, (-Cy*Cz*cosa + Cx*sena)/Cxy],
                [(Cx*Cy*sena - Cz*cosa)/Cxy, -Cxy*sena, (Cy*Cz*sena + Cx*cosa)/Cxy]
                ]
        return R

    def matrizRotacao(self):
        R = self.matrizR
        matrizRotacao = []
        for i in range(0, 12):
            matrizRotacao.append([])
            for j in range(0, 12):
                matrizRotacao[i].append([0])
        for i in range(0, 12, 3):
            for j in range(0, 3):
                for k in range(0,3):    
                    matrizRotacao[i+k][i+j] = R[k][j]
        return matrizRotacao

    def matrizRigidezGlobal(self):
        rotacaoTransposta = np.transpose(self.matrizRotacao)
        matrizRigidezGlobal = np.dot(np.dot(rotacaoTransposta, self.matriz), self.matrizRotacao)
        return matrizRigidezGlobal

    def addCarga(self, carga):
        self.cargas.append(carga)

    def distParaConc(self):
        cargasConcentradas = []
        for carga in self.cargas:
            if type(carga) is CargaConcentrada:
                cargasConcentradas.append(carga)
            else:
                novaCarga = CargaConcentrada(carga.distanciaNoInicio + carga.comprimento/2, 
                                             carga.valor*carga.comprimento, carga.tipo)
                cargasConcentradas.append(novaCarga)
        return cargasConcentradas

    def reacoesAsCargas(self):
        reacoesAsCargas = [
            [0],[0],[0],[0],[0],[0],
            [0],[0],[0],[0],[0],[0]
            ]
        for carga in self.cargas:
            if type(carga) is CargaConcentrada and carga.tipo == 0:
                reacoesAsCargas[0][0] += carga.valor/2
                reacoesAsCargas[3][0] += carga.valor/2
            elif type(carga) is CargaConcentrada and carga.tipo == 1:
                a = carga.distanciaNoInicio
                b = self.comprimento - a
                reacoesAsCargas[1][0] += carga.valor * b**2 * (3*a+b) / self.comprimento**3
                reacoesAsCargas[4][0] += carga.valor * a**2 * (a+3*b) / self.comprimento**3
                reacoesAsCargas[2][0] += carga.valor * a * b**2 / self.comprimento**2
                reacoesAsCargas[5][0] += -1 * carga.valor * a**2 * b / self.comprimento**2
            elif type(carga) is CargaConcentrada and carga.tipo == 2:
                a = carga.distanciaNoInicio
                b = self.comprimento - a
                reacoesAsCargas[1][0] += 6 * carga.valor * a* b / self.comprimento**3
                reacoesAsCargas[4][0] += -6 * carga.valor * a* b / self.comprimento**3
                reacoesAsCargas[2][0] += carga.valor * b * ( 2*a - b) / self.comprimento**2
                reacoesAsCargas[5][0] += carga.valor * a * ( 2*b - a) / self.comprimento**2
            else:
                a = carga.distanciaNoInicio + carga.comprimento/2
                b = self.comprimento - a
                c = carga.comprimento
                v = carga.valor
                Ma = v*c*(12*a*b**2 + c**2 * (self.comprimento - 3*b)) / (12 * self.comprimento**2)
                Mb = -Ma - 3*v*c**3 * (b-a) / (12 * self.comprimento**2)
                Ra = v*c*b/self.comprimento + (Ma+Mb)/self.comprimento
                Rb = v*c - Ra

                reacoesAsCargas[1][0] += Ra
                reacoesAsCargas[4][0] += Rb
                reacoesAsCargas[2][0] += Ma
                reacoesAsCargas[5][0] += Mb

        return reacoesAsCargas