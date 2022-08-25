from tkinter import BOTTOM
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from cargaConcentrada import *

class Plot:
      
      def __init__(self, estrutura):
         self.estrutura = estrutura
         self.pontos = estrutura.pontos
         self.barras = estrutura.barras
         self.ax = plt.axes(projection='3d')
         

      def vetorCarga(self, Ri, carga):
         tamanho = 1
         if carga.tipo == 0 or carga.tipo == 3:
            Rf = [Ri[0] -carga.valor/abs(carga.valor)*tamanho, Ri[1], Ri[2]]
            if carga.tipo == 0:
               return [Ri, Rf, "blue"]
            else:
               return [Ri, Rf, "red"]
         elif carga.tipo == 1 or carga.tipo == 4:
            Rf = [Ri[0], Ri[1] - carga.valor/abs(carga.valor)*tamanho, Ri[2]]
            if carga.tipo == 1:
               return [Ri, Rf, "blue"]
            else:
               return[Ri, Rf, "red"]
         else:
            Rf = [Ri[0], Ri[1], Ri[2] - carga.valor/abs(carga.valor)*tamanho]
            if carga.tipo == 2:
               return [Ri, Rf, "blue"]
            else:
               return[Ri, Rf, "red"]

      def vetorCargasPonto(self, ponto):
         vetores = []
         Ri = [ponto.x, ponto.y, ponto.z]
         for i in range(0,6):
            if ponto.cargas[i] != 0:
               carga = CargaConcentrada(0, ponto.cargas[i], i)
               vetores.append(self.vetorCarga(Ri, carga))
         return vetores

      def vetorCargasBarra(self, barra):
         vetores = []
         inicio = barra.inicio
         fim = barra.fim
         for carga in barra.cargas:   
            fracao = carga.distanciaNoInicio / barra.comprimento
            xi = inicio.x + (fim.x - inicio.x) * fracao
            yi = inicio.y + (fim.y - inicio.y) * fracao
            zi = inicio.z + (fim.z - inicio.z) * fracao
            vetor = [[xi],[yi],[zi]]
            R = np.dot(barra.matrizR(), vetor)
            #Ri = [R[0][0], R[1][0], R[2][0]]
            Ri = [xi, yi, zi]
            vetores.append(self.vetorCarga(Ri, carga))
         return vetores

      def plot(self):
         #ax = plt.axes(projection='3d')
         for ponto in self.pontos:
            plotCargas = self.vetorCargasPonto(ponto)
            for C in plotCargas:
               self.ax.scatter(C[0][0], C[0][2], C[0][1], marker=".", c=C[2])
               self.ax.plot([C[0][0],C[1][0]], [C[0][2],C[1][2]], [C[0][1],C[1][1]], c=C[2], linewidth=0.7) 
      #      ax.scatter(ponto.x,ponto.z,ponto.y, marker=".", c='lime')
         
         #plotar barras
         for barra in self.barras:
            X = []
            Y = []
            Z = []
            X.append(barra.inicio.x)
            X.append(barra.fim.x)
            Y.append(barra.inicio.z)
            Y.append(barra.fim.z)
            Z.append(barra.inicio.y)
            Z.append(barra.fim.y)
            self.ax.plot(X, Y, Z, c='k', label="barra", linewidth=0.7)
            #plotar cargas nas barras
            plotCargas = self.vetorCargasBarra(barra)
            for C in plotCargas:
               self.ax.scatter(C[0][0], C[0][2], C[0][1], marker=".", c=C[2])
               self.ax.plot([C[0][0],C[1][0]], [C[0][2],C[1][2]], [C[0][1],C[1][1]], c=C[2], linewidth=0.7)      
         
      
         #ax.set_facecolor('grey')
         #ax.invert_yaxis()
         self.ax.set_axis_off()
         self.ax.set_xticks([0, 10])
         self.ax.set_yticks([0, 10])
         self.ax.set_zticks([0, 10])
         self.ax.tick_params(bottom=False )
         plt.show()
