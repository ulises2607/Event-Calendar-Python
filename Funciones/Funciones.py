from calendar import monthrange,monthcalendar
import json
import os


class Manipulacion():

    @staticmethod
    def mes_int_a_string(month: int):

        meses_dict = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo",
                        6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre",
                        11: "Noviembre", 12: "Diciembre"}

        return meses_dict[month]

    #print(mes_int_a_string(8))
    #print(type(mes_int_a_string(3)))

    @staticmethod
    def fecha_lista(año: int, mes: int): 
            """
            Retorna una lista representando a un mes calendario. Los dias fueras del mes estan representados por ceros y cada semana comienza en Lunes.

            """
            lista_dias = []
            mes_calendario = monthcalendar(año, mes)

            for semana in mes_calendario:
                for dia in semana:
                    if dia == 0:
                        lista_dias.append(0)
                    else:
                        lista_dias.append(dia)
            
            return lista_dias
    
    
   
