# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import random
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted, SessionStarted
from swiplserver import PrologMQI
import requests
from random import randint, choice
from datetime import datetime, timedelta
import os
import re
#Red Neuronal
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

countries_dict = {
        "China": 0,
        "Tailandia": 1,
        "Inglaterra": 2,
        "Singapur": 3,
        "Francia": 4,
        "Emiratos Arabes Unidos": 5,
        "Estados Unidos": 6,
        "Turquia": 7,
        "Italia": 8,
        "Japon": 9,
        "Espana": 10,
        "Paises Bajos": 11,
        "Austria": 12,
        "Alemania": 13,
        "Sudafrica": 14,
        "Irlanda": 15,
        "Rusia": 16,
        "Grecia": 17,
        "Hungria": 18,
        "Mexico": 19,
        "Canada": 20,
        "Republica Dominicana": 21,
        "Australia": 22,
        "Belgica": 23,
        "Chile": 24,
        "Qatar": 25,
        "Portugal": 26,
        "Egipto": 27,
        "Polonia": 28,
        "Peru": 29,
        "Nueva Zelanda": 30,
        "Argentina": 31
    }

attraction_dict = {
        "playa": 0,
        "montana": 1,
        "ciudad": 2
    }

def RedNeuronal():
    #cargar dataset
    df= pd.read_csv("C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/PROGRAMACION EXPLORATORIA/Ciudades.csv", delimiter=';')
    print(df)
    #Preprocesar datos

    

    label_encoder = LabelEncoder()
    df["Pais"] = df["Pais"].map(countries_dict)
    df["Tiene"] = df["Tiene"].map(attraction_dict)
    df['Tiene'] = label_encoder.fit_transform(df['Tiene'])
    df['Pais'] = label_encoder.fit_transform(df['Pais'])

    # Dividir el dataset en datos de entrenamiento y prueba
    x = df[['Precio', 'Pais', 'Tiene']].values
    y = df['Gusta'].values

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Construir modelo de clasificación
    model = keras.Sequential([
        keras.layers.Input(shape=(X_train.shape[1],)),
        keras.layers.Dense(16, activation='relu'),
        keras.layers.Dense(8, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Entrenar el modelo
    model.fit(X_train, y_train, epochs=10, batch_size=64, validation_data=(X_test, y_test))

    # Evaluar el modelo
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Loss: {loss}, Accuracy: {accuracy}')

    # Predicción para un viaje específico
    precio = 1000
    sample_travel = np.array([[precio, countries_dict['Estados Unidos'],attraction_dict['playa'] ]])

    prediction = model.predict(sample_travel)
    if prediction >= 0.5:
        print("Te va a gustar el viaje")
    else:
        print("No te va a gustar el viaje")
    return model, accuracy

while True:
    modelo_entrenado, accuracy = RedNeuronal()  # Llama a la función y guarda el valor de accuracy

    if accuracy > 0.6:
        break

class CustomSessionStartAction(Action):
    def name(self) -> Text:
        return "action_session_start"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Utiliza una decisión aleatoria para determinar si se debe ejecutar la acción personalizada
        should_execute = choice(["ProcesarDatos"])
        if should_execute == True:
            dispatcher.utter_message("Hola! Que te parece este paquete?")
            action = RecomiendoPaquetesAction()
            return action.run(dispatcher, tracker,domain)
        elif should_execute == "ProcesarDatos":
            historico = "C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/PROGRAMACION EXPLORATORIA/Mateo.txt"
            gustos = "C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/PROGRAMACION EXPLORATORIA/Ciudades.csv"

            # Obtener la fecha actual
            fecha_formateada = datetime.now()            
            # Leer el archivo de gustos y procesar las líneas
            with open(historico, "r") as file_historico:
                for linea_historico in file_historico:
                    dato=linea_historico
                    linea_historico=linea_historico.strip()
                    partes = linea_historico.split(';')
                    if len(partes)>=6:
                        del partes[0:5]
                        pruebafecha = ';'.join(partes)
                        fechaVuelta = datetime.strptime(pruebafecha, "%d/%m/%Y")
                        print(f"{fechaVuelta}<{fecha_formateada}")
                        if fechaVuelta < fecha_formateada:
                            print("LA FECHA ES MENOR QUE HOY")
                            elements = dato.split(';')
                            if len(elements)>=6:
                                elements.pop(5)
                                elements.pop(4)
                                linea_historico = ';'.join(elements)
                                esta=False                    
                                with open(gustos, "r") as file_gustos:
                                    next(file_gustos)
                                    for linea_ciudades in file_gustos:
                                        elements = linea_ciudades.split(';')
                                        if len(elements) >= 4:
                                            elements.pop(3)
                                            linea_ciudades = ';'.join(elements)
                                        print(f"{linea_historico} == {linea_ciudades}")
                                        if linea_historico.strip()==linea_ciudades.strip():
                                            print(f"La línea '{linea_historico}' se encontró en el archivo Ciudades.csv.")
                                            esta=True
                                            break
                            if not esta:
                                print(f"La línea '{linea_historico.strip()}' no está en el .csv, deberemos preguntar si le gusto")
                                ciudad = dato.split(";")[3]
                                solofecha= fechaVuelta.date()
                                dispatcher.utter_message(f"Hola! ¿Cómo te fue en tu viaje a {ciudad} del cual volviste el {solofecha}")
                                dispatcher.utter_message("¿Te gusto?")
                                return [SlotSet("gusta", linea_historico)]
            print("No se encontraron viajes recientes o pendientes de revisar.")
                            
        else:
            dispatcher.utter_message("Hola, como estas?")
            # No ejecutar la acción personalizada, simplemente marca como completada
            return [SessionStarted()]


class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    async def run(
        self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any],) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Creo que no te entendí muy bien, ¿podés reformular lo que dijiste?")
        return [UserUtteranceReverted()]
    
class ActionBuscarVuelos(Action):
    def name(self) -> Text:
        return "action_buscar_vuelo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_buscar_vuelo")
                departure = tracker.get_slot("departure")
                destination = tracker.get_slot("destination")
                print(f"{departure} a {destination}")
                if departure==None or destination==None:
                    print("entendi mal alguno")
                    dispatcher.utter_message(text=f"Creo que esa ciudad no esta en mi base de datos")
                    return [UserUtteranceReverted()]
                inicio = tracker.get_slot("inicio")
                fin = tracker.get_slot("fin")
                search_query = f'buscando vuelos desde {departure} hasta {destination} desde el día {inicio} hasta el {fin}'
                dispatcher.utter_message(text=search_query)
                dispatcher.utter_message(text=f"Encontré estas ofertas para que puedas ir a conocer {destination}:")
                dispatcher.utter_message(text=f"Opcion 1: el madrugador 😴💤")
                horas=random.randint(3,9)
                valor=random.randint(700,1700)
                opcion1=f'''Vuelo desde {departure} hasta {destination} el día {inicio} a las {horas}:00 horas con vuelo de vuelta desde {destination} hasta {departure} el día {fin} a las {24-horas}:30 horas. Valor: ${valor}'''
                dispatcher.utter_message(text=opcion1)
                dispatcher.utter_message(text=f"Opcion 2: el más barato  🧠💡💲")
                horas=random.randint(12,23)
                valor=random.randint(300,700)
                opcion2=f'''Vuelo desde {departure} hasta {destination} el día {inicio} a las {horas}:30 horas con vuelo de vuelta desde {destination} hasta {departure} el día {fin} a las {24-horas}:00 horas. Valor: ${valor}'''
                dispatcher.utter_message(text=opcion2)
                dispatcher.utter_message(text=f"Opcion 3: primera clase 💰🤑💲")
                horas=random.randint(3,9)
                valor=random.randint(2000,3500)
                opcion3=f'''Vuelo desde {departure} hasta {destination} el día {inicio} a las 10:00 horas con vuelo de vuelta desde {destination} hasta {departure} el día {fin} a las 18:00 horas. Valor: ${valor}'''
                dispatcher.utter_message(text=opcion3)
                dispatcher.utter_message(text=f"Que opción te gusta mas? Si ninguna es de tu agrado, proba consultando mas tarde o cambiando las fechas")
                    
        return [SlotSet("opcion1", opcion1),
                    SlotSet("opcion2", opcion2),
                    SlotSet("opcion3", opcion3),
                    SlotSet("hayopcion", True)
                    ]    


class ActionElegirOpcionVuelo(Action):
    def name(self) -> Text:
        return "action_elegir_opcion"
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_elegir_opcionVuelo")
                opcion=tracker.get_slot("opcion")
                print(f"elegiste la opcion {opcion}")
                nro_vuelo=f"opcion{opcion}"
                if 1 <= int(opcion) <= 3:
                    dispatcher.utter_message(text=f"Comprando la opcion {opcion}")
                    slot_opcion=tracker.get_slot(nro_vuelo)
                    dispatcher.utter_message(text=f"{slot_opcion}")
                    # Define el patrón regex
                    patron = r"Vuelo desde (\w+) hasta (\w+) el día (\d{2}/\d{2}/\d{4}) a las (\d{1,2}:\d{2}) horas con vuelo de vuelta desde (\w+) hasta (\w+) el día (\d{2}/\d{2}/\d{4}) a las (\d{1,2}:\d{2}) horas\. Valor: \$(\d+)"
                    # Encuentra la coincidencia en el texto
                    coincidencia = re.search(patron, slot_opcion)
                    # Verifica si se encontró una coincidencia
                    if coincidencia:
                        print("coincidencia")
                        # Extrae los datos
                        hasta_origen = coincidencia.group(2)
                        fecha_origen = coincidencia.group(3)
                        fecha_retorno = coincidencia.group(7)
                        valor = coincidencia.group(9)
                        prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")      
                        result3 = prolog_thread.query(f"pais(Pais,'{hasta_origen}')")
                        result2 = prolog_thread.query(f"tiene('{hasta_origen}', Atraccion)")
                        print("preguntonta")
                        if result3 and result2:
                            pais = result3[0]["Pais"]
                            print(pais)
                            tiene = result2[0]["Atraccion"]
                            nombre_persona = tracker.get_slot("name")
                            if nombre_persona==None:
                                input_data=tracker.latest_message
                                nombre_persona=input_data["metadata"]["message"]["from"]["first_name"]
                            nombre_archivo = f"{nombre_persona}.txt"
                            ruta_especifica = "C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Programacion Exploratoria/"
                            ruta_completa = os.path.join(ruta_especifica, nombre_archivo)
                            try:
                                # Abre el archivo en modo de escritura para agregar contenido ('a+')
                                with open(ruta_completa, 'a+') as file:
                                    # Lee el contenido existente (si hay alguno)
                                    contenido_existente = file.read()
                                    data = ";".join([valor,pais,tiene,hasta_origen, fecha_origen, fecha_retorno])
                                    # Agrega nueva información al archivo
                                    file.write(f"\n{data}")
                                print(f"Información agregada al archivo '{nombre_archivo}' correctamente.")
                            except Exception as e:
                                print(f"Error al modificar el archivo: {str(e)}")
                    dispatcher.utter_message(text="Queres reservar hotel tambien?")
                else:
                    dispatcher.utter_message(text=f"Opción no válida, intentelo de nuevo")
                    return [UserUtteranceReverted()]
        return []    

class ActionElegirOpcionHotel(Action):
    def name(self) -> Text:
        return "action_elegir_opcion_hotel"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_elegir_opcion_hotel")
                opcion=tracker.get_slot("opcion")
                print(f"elegiste la opcion {opcion}")
                nro_hotel=f"hotel{opcion}"
                if 1 <= int(opcion) <= 3:
                    dispatcher.utter_message(text=f"Comprando la opcion {opcion}")
                    slot_opcion=tracker.get_slot(nro_hotel)
                    dispatcher.utter_message(text=f"{slot_opcion}")
                    dispatcher.utter_message(text="Muchas gracias por su compra")
                else:
                    dispatcher.utter_message(text=f"Opción no válida, intentelo de nuevo")
                    return [UserUtteranceReverted()]
        return []

class ActionListarCiudades(Action):
    def name(self) -> Text:
        return "action_listar_ciudades"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_listar_ciudades")
                #Retorno todas las ciudades de PROLOG
                prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")               
                result = prolog_thread.query("mostrar_city(Cities)")
                if result:
                    lista_city = result[0]["Cities"]
                    dispatcher.utter_message(text=f"Las ciudades son: ")
                    for ciudad in lista_city:
                        dispatcher.utter_message(text=ciudad)
                else :
                    dispatcher.utter_message(text="No se encontraron ciudades.")
        return[]              

class ActionCiudadesPais(Action):
    def name(self) -> Text:
        return "action_ciudades_de_pais"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_ciudades_de_pais")
                pais = tracker.get_slot("slot_pais")
                if pais!=None:
                    print(pais)
                    #Retorno todas las ciudades de un PAIS de PROLOG
                    prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")               
                    result = prolog_thread.query(f"ciudad_pais('{pais}', Ciudades)")
                    if result:
                        lista_city = result[0]["Ciudades"]
                        dispatcher.utter_message(text=f"Las ciudades en {pais} son: ")
                        for ciudad in lista_city:
                            dispatcher.utter_message(text=ciudad)
                else :
                    dispatcher.utter_message(text=f"No tengo destinos en ese pais actualmente.Estamos en continua expansion")
                    return [UserUtteranceReverted()]
        return[]    
    
class ActionAtraccionCiudad(Action):
    def name(self) -> Text:
        return "action_atraccion_de_ciudad"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_atraccion_de_ciudad")
                ciudad = tracker.get_slot("slot_ciudad")
                if ciudad!=None:
                    #Retorno todas las atracciones de una ciudad de PROLOG
                    prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")               
                    result = prolog_thread.query(f"ciudad_tiene('{ciudad}', Atraccion)")
                    if result:
                        lista_atrac = result[0]["Atraccion"]
                        atrac= lista_atrac[0]
                        print(atrac)
                        if atrac=="montana":
                            dispatcher.utter_message(text=f"En {ciudad} hay unas vistas muy lindas a las montañas ")
                        if atrac=="playa":
                            dispatcher.utter_message(text=f"{ciudad} tiene unas de las playas mas lindas")
                        if atrac=="ciudad":
                            dispatcher.utter_message(text=f"En {ciudad} tenes una ciudad muy bella para conocer, con miles de cosas por hacer y una rica cultura por explorar")
                else :
                    dispatcher.utter_message(text=f"No tengo esa ciudad en mi base de datos. Estamos en continua expansion")
                    return [UserUtteranceReverted()]
        return[]  

class ActionAtraccionEn(Action):
    def name(self) -> Text:
        return "action_atraccion_en"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_atraccion_en")
                atraccion = tracker.get_slot("slot_atraccion")
                if atraccion!=None:
                    if atraccion=="montaña" or atraccion=="montañas":
                        atraccion="montana"
                    #Retorno todas las ciudades que tienen una atraccion de PROLOG
                    prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")               
                    result = prolog_thread.query(f"tiene_ciudad('{atraccion}', Ciudades)")
                    if result:
                        lista_city = result[0]["Ciudades"]
                        if atraccion=="montana":
                            atraccion="montaña"

                        dispatcher.utter_message(text=f"Las ciudades donde hay {atraccion} son: ")
                        for ciudad in lista_city:
                            dispatcher.utter_message(text=ciudad)
                else :
                    dispatcher.utter_message(text=f"No tengo esa atraccion guardada en mi base de datos. Estamos en continua expansion")
                    return [UserUtteranceReverted()]
        return[] 

class RecomiendoPaquetesAction(Action):
    def name(self):
        return "action_recomendar_paquetes"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_recomendar_paquetes")
                #Retorno todos los paquetes de PROLOG
                prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")               
                result = prolog_thread.query(f"paquete(Nombre, Destinos)")
        if result:
            cant=len(result)
            rand=randint(0, cant - 1)
            paquete=result[rand]
            nombre_paquete = paquete['Nombre']
            destinos = paquete['Destinos']
            valor=random.randint(5000,10000)
            fecha_minima = datetime.now()
            fecha_maxima = fecha_minima + timedelta(days=365)
            fecha1 = fecha_minima + timedelta(days=random.randint(0, (fecha_maxima - fecha_minima).days))
            dias_restantes = (fecha_maxima - fecha1).days
            fecha2 = fecha1 + timedelta(days=random.randint(1, dias_restantes))
            fecha1 = fecha1.strftime("%d/%m/%Y")
            fecha2 = fecha2.strftime("%d/%m/%Y")
            dispatcher.utter_message(text="Te recomiendo el siguiente paquete 🌟: ")
            recomendacion=f"Yo lo llamo: {nombre_paquete}, y vas a poder visitar: {', '.join(destinos)},desde el {fecha1} hasta el dia {fecha2} por el valor de ${valor}"
            dispatcher.utter_message(recomendacion)
            slot_paquete=f"Nombre del paquete: {nombre_paquete} hacia: {', '.join(destinos)}, fecha inicio: {fecha1}, fecha fin: {fecha2}, precio: ${valor}"
            dispatcher.utter_message(text="Deseas comprarlo?")
        else:
            dispatcher.utter_message("Disculpame, no tengo ningun paquete ahora mismo")

        return [SlotSet("paquete", slot_paquete)]

class ActionComprarPaquete(Action):
    def name(self) -> Text:
        return "action_comprar_paquete"
        
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("action_comprar_paquete")
                paquete=tracker.get_slot("paquete")
                ruta_especifica = "C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Programacion Exploratoria/"
                nombre_persona = tracker.get_slot("name")
                if nombre_persona==None:
                    input_data=tracker.latest_message
                    nombre_persona=input_data["metadata"]["message"]["from"]["first_name"]
                nombre_archivo = f"{nombre_persona}.txt"
                ruta_completa = os.path.join(ruta_especifica, nombre_archivo)
                print(paquete)
                try:
                    patron = r"hacia: (.*?), fecha inicio: (\d{2}/\d{2}/\d{4}), fecha fin: (\d{2}/\d{2}/\d{4}), precio: \$([\d.]+)"
                    # Encuentra la coincidencia en el texto
                    coincidencia = re.search(patron, paquete)
                    # Verifica si se encontró una coincidencia
                    if coincidencia:
                        # Extrae los datos
                        destinos = coincidencia.group(1).split(', ')
                        fecha_inicio = coincidencia.group(2)
                        fecha_fin = coincidencia.group(3)
                        precio = float(coincidencia.group(4))
                        
                        # Imprime los datos extraídos
                        print(f"Destinos: {', '.join(destinos)}")
                        print(f"Fecha de inicio: {fecha_inicio}")
                        print(f"Fecha de fin: {fecha_fin}")
                        print(f"Precio: ${precio}")
                        cant=len(destinos)
                        valor= precio/cant
                    # Abre el archivo en modo de escritura para agregar contenido ('a+')
                    with open(ruta_completa, 'a+') as file:
                        # Lee el contenido existente (si hay alguno)
                        contenido_existente = file.read()
                        pais=None
                        tiene=None
                        # Agrega nueva información al archivo
                        for destino in destinos:
                            prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")      
                            result3 = prolog_thread.query(f"pais(Pais,'{destino}')")
                            result2 = prolog_thread.query(f"tiene('{destino}', Atraccion)")
                            if result3 and result2:
                                pais= result3[0]["Pais"]
                                print(pais)
                                tiene = result2[0]["Atraccion"]
                                print(tiene)
                                datos_destino=f"{valor};{pais};{tiene};{destino};{fecha_inicio};{fecha_fin}"
                                file.write(f"\n{datos_destino}")
                                print(f"Información agregada al archivo '{nombre_archivo}.txt' correctamente.")
                        # Muestra el contenido existente (si hay alguno)
                        if contenido_existente:
                            print("Contenido existente en el archivo:")
                            print(contenido_existente)
                   
                except Exception as e:
                    print(f"Error al modificar el archivo: {str(e)}")
                dispatcher.utter_message(text=f"Paquete comprado correctamente, muchas gracias.")
                dispatcher.utter_message(text=f"Hay algo mas en lo que te pueda ayudar?")
        return [SlotSet("paquete", "None")]


class ActionListarHoteles(Action):
    def name(self) -> Text:
        return "action_listar_hoteles"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_listar_hoteles")
                #Retorno todas las ciudades de PROLOG
                hotel1 = "None"
                hotel2 = "None"
                hotel3 = "None"
                prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")               
                result = prolog_thread.query("mostrar_hoteles(Hoteles)")
                if result:
                    lista_hoteles= result[0]["Hoteles"]
                    num_nombres_a_mostrar = 3
                    # Verificar que num_nombres_a_mostrar no sea mayor que la longitud de la lista
                    # Usar random.sample para obtener una muestra aleatoria sin repetición
                    nombres_mostrados = random.sample(lista_hoteles, num_nombres_a_mostrar)
                    # Imprimir los nombres de hoteles mostrados
                    dispatcher.utter_message(text="Estos son los hoteles que tengo disponibles: ")
                    arr_hoteles=[]
                    inicio = tracker.get_slot("inicio")
                    fin = tracker.get_slot("fin")
                    for nombre in nombres_mostrados:
                        valor=random.randint(50,500)
                        if inicio and fin:
                            # Convierte las cadenas de fecha en objetos datetime
                            fecha1 = datetime.strptime(inicio, "%d/%m/%Y")
                            fecha2 = datetime.strptime(fin, "%d/%m/%Y")
                            # Calcula la diferencia en días
                            diferencia = (fecha2 - fecha1).days
                            valorFinal=diferencia*valor
                            hotel=f"Hotel {nombre} por ${valor} la noche, total: ${valorFinal} "
                        else: 
                            hotel=f"Hotel {nombre} por ${valor} la noche"
                        arr_hoteles.append(hotel)
                        dispatcher.utter_message(text=hotel)   
                    if len(arr_hoteles) >= 3:
                        hotel1 = arr_hoteles[0]
                        hotel2 = arr_hoteles[1]
                        hotel3 = arr_hoteles[2]
                    dispatcher.utter_message(text="Que opcion de hotel te gusta mas?") 
                else :
                    dispatcher.utter_message(text="No tengo hoteles disponibles en esa ubicacion")
        return[SlotSet("hotel1", hotel1),
                SlotSet("hotel2", hotel2),
                SlotSet("hotel3", hotel3)
                ]   


class ActionCheckSlots(Action):
    def name(self) -> Text:
        return "action_check_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        departure = tracker.get_slot("departure")
        destination = tracker.get_slot("destination")
        inicio = tracker.get_slot("inicio")
        fin = tracker.get_slot("fin")
        ciudad = tracker.get_slot("slot_ciudad")
        pais = tracker.get_slot("slot_pais")
        atraccion = tracker.get_slot("slot_atraccion")
        
        if departure and destination:
            dispatcher.utter_message(f"El valor del slot 'departure' es {departure} y el valor del slot 'destination' es {destination}")
        else:
            dispatcher.utter_message("origen y/o destino son null.")
        
        if inicio and fin:
            dispatcher.utter_message(f"El valor del slot 'inicio' es {inicio} y el valor del slot 'fin' es {fin}")
        else:
            dispatcher.utter_message("inicio y/o fin son null.")

        if ciudad:
            dispatcher.utter_message(f"El valor del slot 'ciudad' es {ciudad} ")
        else:
            dispatcher.utter_message("El valor del slot 'ciudad' es null.")
        
        if pais:
            dispatcher.utter_message(f"El valor del slot 'pais' es {pais} ")
        else:
            dispatcher.utter_message("El valor del slot 'pais' es null.")

        if atraccion:
            dispatcher.utter_message(f"El valor del slot 'atraccion' es {atraccion} ")
        else:
            dispatcher.utter_message("El valor del slot 'atraccion' es null.")
        return []

class ActionBorrarSlots(Action):
    def name(self) -> Text:
        return "action_erase_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("departure", "None"),
                SlotSet("destination", "None"),
                SlotSet("inicio", "None"),
                SlotSet("fin", "None"),
                SlotSet("slot_ciudad", "None"),
                SlotSet("slot_pais", "None"),
                SlotSet("slot_atraccion", "None"),
                SlotSet("hotel1", "None"),
                SlotSet("hotel2", "None"),
                SlotSet("hotel3", "None"),
                SlotSet("opcion1", "None"),
                SlotSet("opcion2", "None"),
                SlotSet("opcion3", "None"),
                SlotSet("hayopcion", False),
                SlotSet("opcion", "None"),   
                ]


class ActionRecomiendoDestino(Action):
    def name(self) -> Text:
        return "action_recomendar_destino"

    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                print("entre a action_recomendar_destino")
                #Retorno todas las ciudades de PROLOG
                prolog_thread.query("consult('C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Bot.pl')")               
                result = prolog_thread.query("mostrar_city(Cities)")
                if result:
                    lista_city = result[0]["Cities"]
                    valor=random.randint(500,1500)
                    random.shuffle(lista_city)
                    for ciudad in lista_city:
                        result2 = prolog_thread.query(f"tiene('{ciudad}', Atraccion)")
                        print(f"Consultando: pais('Pais',{ciudad})")
                        result3 = prolog_thread.query(f"pais(Pais,'{ciudad}')")
                        if result2 and result3:
                            pais= result3[0]["Pais"]
                            atraccion = result2[0]["Atraccion"]
                            sample_travel = np.array([[valor, countries_dict[pais], attraction_dict[atraccion]]])
                            prediction = modelo_entrenado.predict(sample_travel)
                            if prediction >= 0.5:
                                valor=random.randint(600,1500)
                                fecha1 = datetime.now()
                                fecha2 = fecha1 + timedelta(days=15)
                                fecha1 = fecha1.strftime("%d/%m/%Y")
                                fecha2 = fecha2.strftime("%d/%m/%Y")
                                if atraccion=="montana":
                                    atraccion="montaña"
                                if ciudad=="Espana":
                                    ciudad="España"
                                recomendacion=f"Tal vez podria gustarte un viaje a {ciudad}, desde el {fecha1} hasta el dia {fecha2} por el valor de ${valor}"
                                recom=f"{valor};{pais};{atraccion};{ciudad};{fecha1};{fecha2}"
                                dispatcher.utter_message(recomendacion)
                                dispatcher.utter_message("¿Te gustaria comprarlo?")
                                return[SlotSet("recomendacion", recom)]
                                break
                            else:
                                print(f"No te va a gustar el viaje a {ciudad},en {pais}, a ${valor}, probemos con otro")           
                else :
                    dispatcher.utter_message(text=f"No tengo los suficientes datos para recomendarte un destino")
                    print("No te va a gustar ninguno")
        return[] 


class ActioSavePreferences(Action):
    def name(self) -> Text:
        return "action_save_preferences"
    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("entre a action_save_preferences")
        intent_anterior = tracker.latest_message.get("intent", {}).get("name")
        inicio = tracker.get_slot("gusta")
        if inicio!=None:
            campos = inicio.split(";")
            ruta_completa = "C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Programacion Exploratoria/Ciudades.csv"
            if intent_anterior == "affirm" or intent_anterior== "gustoviaje":
                # Hacer algo si el intent anterior fue afirmación y explicación de por qué gustó un viaje
                dispatcher.utter_message("¡Gracias por compartir tu experiencia positiva! ¿Puedo ayudarte con algo más?")
                nuevo_dato = f"{campos[0]};{campos[1]};{campos[2]};True;{campos[3]}"
            else:
                dispatcher.utter_message("Lamento escuchar que no disfrutaste tu viaje. ¿Puedo ayudarte con algo más?")
                nuevo_dato = f"{campos[0]};{campos[1]};{campos[2]};False;{campos[3]}"
            try:
                with open(ruta_completa, 'a+') as file:
                    # Lee el contenido existente (si hay alguno)
                    contenido_existente = file.read()
                    file.write(f"\n{nuevo_dato}")
                    print(f"Información agregada al archivo 'ciudades.csv' correctamente.")
            except Exception as e:
                print(f"Error al modificar el archivo: {str(e)}")
        return []

class ActionComprarRecomendacion(Action):
    def name(self) -> Text:
        return "action_comprar_recomendacion"
    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("entre a action_comprar_recomendacion")
        recomendacion = tracker.get_slot("recomendacion")
        historico = "C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/PROGRAMACION EXPLORATORIA/Mateo.txt"
        try:
            with open(historico, 'a+') as file:
                # Lee el contenido existente (si hay alguno)
                file.write(f"\n{recomendacion}")
                print(f"Información agregada al archivo 'Mateo.txt' correctamente.")
                dispatcher.utter_message("Perfecto, espero tengas un buen viaje!")
                dispatcher.utter_message("¿Se te ofrece algo mas?")
        except Exception as e:
            print(f"Error al modificar el archivo: {str(e)}")

        return[]


class ActionSaveLastMessage(Action):
    def name(self) -> Text:
        return "action_save_last_message"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Obtener el último mensaje del usuario
        last_message = tracker.latest_message.get("text", "")

        print("guardando mensaje: ")
        print (last_message)
        print ("\n")
        # Guardar el último mensaje en un archivo de texto
        with open ("C:/Users/matet/Documents/MATEO/MATERIAS/3 AÑO/2 CUATRIMESTRE/Programacion Exploratoria/archivo.txt", "a") as file:
            file.write(last_message+"\n")
            file.close()
        
        return []

class ActionGetName(Action):
    def name(self) -> Text:
        return "action_get_name"
    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        input_data=tracker.latest_message
        print(input_data["metadata"]["message"]["from"])
        if input_data:
            user_name=input_data["metadata"]["message"]["from"]["first_name"]
        
            print("Your name is "+user_name)
            return [SlotSet("name", user_name),SlotSet("name_value", True)]
        return []