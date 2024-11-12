import pandas as pd
import numpy as np

#por logica el valor de un jugador se mide por los goles asistencias y loa edad
#este codigo estrapola los datos de cada jugador y los compara con los promedios de goles y asistencias de los 5 mas valiosos
#este codigo se puede utilizar para comparar multiples dataframes y arrojar conclusiones
#guarda los atributos que hacen que su valor baje o suba en una lista
#si son muchos atrbutos que hacen que su valor baje, se dara esa cocnlusion de lo contrario sube


### CLASE DE JUGADORES
class players:

    def __init__(self):     ###iniciacion de la clase jugadores 
        self.data = pd.read_csv("PLAYERS.csv")      ###lee el csv para conseguir los datos necesarios 
        self.Promedio_goles = self.data['Goals'].head(5).mean()     ###consigue el promedio de los goles de los cinco mejores jugadores
        self.Promedio_asistencias = self.data['Assists'].head(5).mean()     ###consigue el promedio de las asistencias de los 5 mejores jugadores

    ###metodo Down_value_for_age 
    def Down_value_for_age(self, fila):     

        age = self.data.loc[fila,'Age']     ###metodo que me indica si la edad del jugador es mayor de 30 años
        
        if (age > 30):      ###si la edad del jugador supera los 30 devuelve 1
            return 1
        else:       ###si eso es falso devuelve 0
            return 0

    ###metodo Donw_value_for_goals    
    def Donw_value_for_goals(self, fila):

        goals = self.data.loc[fila,'Goals']     ###busca los goles que tiene el jugador en especifico

        if (goals < (self.Promedio_goles)):     ###si la marca de los goles es mas baja que el promedio devuelve 1
            return 1
        else:       ###si no devuelve 0
            return 0


    ###metodo Donw_value_for_assists    
    def Donw_value_for_assists(self, fila):

        assists = self.data.loc[fila,'Assists']     ###busca las asistencias de un jugador en particular

        if (assists < (self.Promedio_asistencias)):     ###si la marca de las asistencias es menor que el promedio devuelve 1
            return 1
        else:       ###si es falso devuelve 0
            return 0

### espacio de pruebas

pl = players()  ###objeto de la clase players
fila = 16   ###inidcativo de la fila a la que queremos llamar

print(pl.data[['Player_name','Age','Goals','Assists']])

list_of_capacity = [    ###esta lista tiene como objetivo registrar cuantos valores que hcane que los precios de los jugadore bajen son 1
    pl.Down_value_for_age(fila),
    pl.Donw_value_for_goals(fila),
    pl.Donw_value_for_assists(fila)
]

Capacity_for_download = len(list(filter(lambda x: x == 1, list_of_capacity)))   ###mew indica la cantidad de valores que son 1 en list_of_capacity

if (Capacity_for_download > (len(list_of_capacity) // 2)):  ###si tiene la mitad entera de la lista como 1 su precio bajara
    print('su precio bajara')
else:       ###si no su precio subira
    print('su precio subira')


print(list_of_capacity)
print(pl.Promedio_asistencias)
print(pl.Promedio_goles)

