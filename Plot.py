from tkinter import BOTTOM
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from CargaConcentrada import *

class Plot:
      
   def __init__(self, estrutura):
      self.estrutura = estrutura
      self.pontos = estrutura.pontos
      self.barras = estrutura.barras
      self.ax = plt.axes(projection='3d')
         
   def vetorCarga(self, Ri, carga):
      tamanho = -carga.valor/abs(carga.valor)*1
      seta = -carga.valor/abs(carga.valor)*0.08
      fimSeta = 0.25/abs(seta)
      if carga.tipo == 0 or carga.tipo == 3:
         Rf = [Ri[0] + tamanho, Ri[1], Ri[2]]
         fim = Ri[0] + seta*fimSeta
         if carga.tipo == 0:
            setas = [
               [fim, Ri[1] + seta, Ri[2]],
               [fim, Ri[1] - seta, Ri[2]],
               [fim, Ri[1], Ri[2] + seta],
               [fim, Ri[1], Ri[2] - seta]
            ]
            return [Ri, Rf, "blue", setas, carga.valor]
         else:
            setas = [
               [fim, Ri[1] + seta, Ri[2]],
               [fim, Ri[1] - seta, Ri[2]],
               [fim, Ri[1], Ri[2] + seta],
               [fim, Ri[1], Ri[2] - seta],

               [fim, Ri[1], Ri[2]],
               [fim*2, Ri[1] + seta, Ri[2]],
               [fim*2, Ri[1] - seta, Ri[2]],
               [fim*2, Ri[1], Ri[2] + seta],
               [fim*2, Ri[1], Ri[2] - seta]
            ]
            return [Ri, Rf, "red", setas, carga.valor]
      elif carga.tipo == 1 or carga.tipo == 4:
         Rf = [Ri[0], Ri[1] + tamanho, Ri[2]]
         fim = Ri[1] + seta*fimSeta
         if carga.tipo == 1: 
            setas = [
               [Ri[0] + seta, fim, Ri[2]],
               [Ri[0] - seta, fim, Ri[2]],
               [Ri[0], fim, Ri[2] + seta],
               [Ri[0], fim, Ri[2] - seta]
            ]
            return [Ri, Rf, "blue", setas, carga.valor]
         else:
            setas = [
               [Ri[0] + seta, fim, Ri[2]],
               [Ri[0] - seta, fim, Ri[2]],
               [Ri[0], fim, Ri[2] + seta],
               [Ri[0], fim, Ri[2] - seta],

               [Ri[0], fim, Ri[2]],
               [Ri[0] + seta, fim*2, Ri[2]],
               [Ri[0] - seta, fim*2, Ri[2]],
               [Ri[0], fim*2, Ri[2] + seta],
               [Ri[0], fim*2, Ri[2] - seta]
            ]
            return[Ri, Rf, "red", setas, carga.valor]
      else:
         Rf = [Ri[0], Ri[1], Ri[2] + tamanho]
         fim = Ri[2] + seta*fimSeta
         if carga.tipo == 2:
            setas = [
               [Ri[0] + seta, Ri[1], fim],
               [Ri[0] - seta, Ri[1], fim],
               [Ri[0], Ri[1] + seta, fim],
               [Ri[0], Ri[1] - seta, fim]
            ]
            return [Ri, Rf, "blue", setas, carga.valor]
         else:
            setas = [
               [Ri[0] + seta, Ri[1], fim],
               [Ri[0] - seta, Ri[1], fim],
               [Ri[0], Ri[1] + seta, fim],
               [Ri[0], Ri[1] - seta, fim],

               [Ri[0], Ri[1], fim],
               [Ri[0] + seta, Ri[1], fim*2],
               [Ri[0] - seta, Ri[1], fim*2],
               [Ri[0], Ri[1] + seta, fim*2],
               [Ri[0], Ri[1] - seta, fim*2]
            ]
            return[Ri, Rf, "red", setas, carga.valor]

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
         Ri = [xi, yi, zi]
         vetores.append(self.vetorCarga(Ri, carga))
      return vetores

   def plotCargaConcentrada(self, vetor):
      for C in vetor:
         #self.ax.scatter(C[0][0], C[0][2], C[0][1], marker=".", c=C[2])
         self.ax.plot([C[0][0],C[1][0]], [C[0][2],C[1][2]], [C[0][1],C[1][1]], c=C[2], linewidth=0.7)
         for i in range(0,4):
            self.ax.plot([C[0][0],C[3][i][0]], [C[0][2],C[3][i][2]], [C[0][1],C[3][i][1]], c=C[2], linewidth=0.7)
         if C[2] == "red":
            for j in range(5,9):
               self.ax.plot([C[3][4][0],C[3][j][0]],
                            [C[3][4][2],C[3][j][2]],
                            [C[3][4][1],C[3][j][1]], c=C[2], linewidth=0.7)
         self.ax.text(C[1][0], C[1][2], C[1][1], C[4], color=C[2], fontsize=6)
               
   def plotBarras(self, barra, i):
      X = []
      Y = []
      Z = []
      X.append(barra.inicio.x)
      X.append(barra.fim.x)
      Y.append(barra.inicio.z)
      Y.append(barra.fim.z)
      Z.append(barra.inicio.y)
      Z.append(barra.fim.y)
      self.ax.plot(X, Y, Z, c='k', linewidth=0.7)
      self.ax.text((X[0]+X[1])/2,
                   (Y[0]+Y[1])/2,
                   (Z[0]+Z[1])/2,
                   "{}".format(i+1),
                  color="black", fontsize=6
                  )

      #plotar cargas nas barras
      plotCargas = self.vetorCargasBarra(barra)
      self.plotCargaConcentrada(plotCargas)

      
   def plot(self):
      #ax = plt.axes(projection='3d')
      for ponto in self.pontos:
         plotCargas = self.vetorCargasPonto(ponto)
         self.plotCargaConcentrada(plotCargas)
           
      #plotar barras
      for i in range(len(self.barras)):
         self.plotBarras(self.barras[i], i)
      
      self.ax.set_facecolor('grey')
      #ax.invert_yaxis()
      #self.ax.set_axis_off()
      self.ax.set_xticks([0, 10])
      self.ax.set_yticks([0, 10])
      self.ax.set_zticks([0, 10])
      self.ax.tick_params(bottom=False )
      plt.show()
