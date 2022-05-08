import tkinter as tk
import sounddevice as sd
import numpy as np
from threading import Thread, Event

periodo_muestreo = 1.0 / 44100

class StreamThread(Thread):
    def __init__(self):
        super().__init__()
        self.dispositivo_input = 1
        self.dispositivo_output = 3
        self.tamano_bloque = 5500
        self.canales = 1
        self.tipo_dato = np.int16
        self.latencia = "high"
        self.frecuencia_muestreo = 44100
    
    def callback_stream(self, indata, outdata, frames, time, status):
        global app, periodo_muestreo
        app.etiqueta_valor_estado["text"] = "Grabando"
        data = indata[:,0]
        transformada = np.fft.rfft(data)
        frecuencias = np.fft.rfftfreq(len(data), periodo_muestreo)
        #print("Frecuencia fundamental: ", frecuencias[np.argmax(np.abs(transformada))])
        #app.etiqueta_valor_ff["text"] = (frecuencias[np.argmax(np.abs(transformada))])
        #frecuencia_valor = (frecuencias[np.argmax(np.abs(transformada))])
        app.etiqueta_valor_ff["text"] = frecuencias[transformada.argmax()] 
        frecuencia_valor = frecuencias[transformada.argmax()] 

        #prueba
        if frecuencia_valor > 77.0 and frecuencia_valor < 87.0:
            app.cuerda_valor["text"] = "La cuerda tocada es la 6ta con una frecuencia de: " + str(frecuencia_valor)
            if (frecuencia_valor < 81.6):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_valor > 83.0):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: print("La cuerda esta bien afinada")
        elif frecuencia_valor > 105.0 and frecuencia_valor < 115.0:
            app.cuerda_valor["text"] = "La cuerda tocada es la 5ta con una frecuencia de: " + str(frecuencia_valor)
            if (frecuencia_valor < 109.4):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_valor > 110.6):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: print("La cuerda esta bien afinada")
        elif frecuencia_valor > 141.0 and frecuencia_valor < 151.0:
            app.cuerda_valor["text"] = "La cuerda tocada es la 4ta con una frecuencia de: " + str(frecuencia_valor)
            if (frecuencia_valor < 146.23):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_valor > 147.43):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: print("La cuerda esta bien afinada")
        elif frecuencia_valor > 191.0 and frecuencia_valor < 201.0:
            app.cuerda_valor["text"] = "La cuerda tocada es la 3ta con una frecuencia de: " + str(frecuencia_valor)
            if (frecuencia_valor < 195.4):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_valor > 196.6):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: print("La cuerda esta bien afinada")
        elif frecuencia_valor > 242.0 and frecuencia_valor < 252.0:
            app.cuerda_valor["text"] = "La cuerda tocada es la 2ta con una frecuencia de: " + str(frecuencia_valor)
            if (frecuencia_valor < 246.34):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_valor > 247.54):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: print("La cuerda esta bien afinada")
        elif frecuencia_valor > 324.0 and frecuencia_valor < 334.0:
            app.cuerda_valor["text"] = "La cuerda tocada es la 1ta con una frecuencia de: " + str(frecuencia_valor)
            if (frecuencia_valor < 329.03):
                app.ajuste_valor["text"] = "Se debe apretar más la cuerda"
            elif(frecuencia_valor > 330.23):
                app.ajuste_valor["text"] = "Se debe aflojar la cuerda"
            else: print("La cuerda esta bien afinada")
        return

    def run(self):
        try:
            self.event = Event()
            with sd.Stream(
                device = (self.dispositivo_input, self.dispositivo_output),
                blocksize = self.tamano_bloque,
                samplerate = self.frecuencia_muestreo,
                channels = self.canales,
                dtype = self.tipo_dato,
                latency = self.latencia,
                callback = self.callback_stream

            ) as self.stream: 
                self.event.wait()

        except Exception as e:
            print(str(e))

# Heredamos de Tk para hacer una ventana
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # Establecer titulo de la ventana
        self.title("Aplicación de audio")
        # Establecemos tamaño
        self.geometry("500x300")

        #Iniciar Boton
        boton_iniciar = tk.Button(self, 
            width = 20, text = "Iniciar grabación",
            command = lambda: self.click_boton_iniciar())
        #Boton Funcional
        boton_iniciar.grid(column = 0, row = 0)

        boton_detener = tk.Button(self, 
            width = 20, text = "Detener grabación",
            command = lambda: self.click_boton_detener())
        boton_detener.grid(column = 1, row = 0)

        etiqueta_estado = tk.Label(text = "Estado: ")
        etiqueta_estado.grid(column = 0, row = 1)

        self.etiqueta_valor_estado = tk.Label(text = "- ")
        self.etiqueta_valor_estado.grid(column = 1, row = 1)

        etiqueta_frecuencias = tk.Label(text = "Frecuencia fundamental: ")
        etiqueta_frecuencias.grid(column=0, row=2)

        self.etiqueta_valor_ff = tk.Label(text = "-")
        self.etiqueta_valor_ff.grid(column=1, row=2)

        etiqueta_cuerda = tk.Label(text = "Cuerda: ")
        etiqueta_cuerda.grid(column = 0, row = 3)

        self.cuerda_valor = tk.Label(text = "-")
        self.cuerda_valor.grid(column=1, row=3)

        etiqueta_ajuste = tk.Label(text = "Ajuste: ")
        etiqueta_ajuste.grid(column = 0, row = 4)

        self.ajuste_valor = tk.Label(text = "-")
        self.ajuste_valor.grid(column=1, row=4)

        self.stream_thread = StreamThread()
    
    def click_boton_detener(self):
        if self.stream_thread.is_alive():
            self.etiqueta_valor_estado["text"] = "Grabación Detenida" 
            self.stream_thread.stream.abort()
            self.stream_thread.event.set()
            self.stream_thread.join()
            
    def click_boton_iniciar(self):
        if not self.stream_thread.is_alive():
            self.stream_thread.daemon = True
            self.stream_thread.start()
           
app = App()

def main():
    global app
    app.mainloop()

if __name__ == "__main__":
    main()