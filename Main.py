import tkinter as tk
import json
from collections import deque

def load_db(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def add_newData(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent= 2)

def start(database: dict):
    database['actual'].clear()
    add_newData('Database.json',database)
    for q in database["types"]:
        database["actual"].append(q)
        add_newData('Database.json',database)
    return

def get_Question(database: dict, questions: deque):
    if len(list(database['actual'])) <= 1: return
    found: bool = False
    i,k = 0,0
    while found == False:
        q:str = database['actual'][i]
        x: str = q.keys()
        j = 1
        while True:
            aQuestion = list(x)[j]
            if aQuestion in questions:
                print(f'ya existe la pregunta : {aQuestion}')
                
            else:
                questions.append(aQuestion)
                found = True
                break
            if j < len(x)-1: j = j+1
            else:
                break
        if i < len(list(database['actual']))-1: i = i+1
        else: found = True
    while True:
        y = list(database['preguntas'][0].keys())[k]
        if y == aQuestion:
            print(list(database['preguntas'][0].values())[k])
            pregunta:str = (list(database['preguntas'][0].values())[k])
            break
        if k < len(list(database['preguntas'][0].values())[k])-1: k = k+1
        else: break
    return aQuestion, pregunta

def get_Answer(question: str,answer: str, database: dict) -> str | None:
    for q in database["actual"]:
        if q[question] != answer.lower():
            database["actual"].remove(q)
            add_newData('Database.json',database)
    return q["name"]

class Interfaz(tk.Tk):
    def __init__(self):
        super().__init__()
        database: dict = load_db('Database.json')
        qList = deque([])
        start(database)

        p, question = get_Question(database,qList)

        # Inicializar variables
        self.geometry("600x400")
        self.resizable(False,False)
        self.title("Test de estudiante")
        self.texto_actual = f"{question}"
        self.respuesta_seleccionada = tk.StringVar()

        # Crear elementos de la interfaz
        self.label_pregunta = tk.Label(self, text=self.texto_actual)
        self.label_pregunta.pack(pady=10)

        self.opciones = [("si"), ("no")]
        self.caja_seleccion = tk.OptionMenu(self, self.respuesta_seleccionada, *self.opciones)
        self.caja_seleccion.pack(pady=10)

        self.boton_siguiente = tk.Button(self, text="Siguiente", command=lambda: (self.siguiente_pregunta(database,qList)))
        self.boton_siguiente.pack(pady=10)

    def siguiente_pregunta(self,database,qList):
        # Obtener la respuesta seleccionada

        respuesta = self.respuesta_seleccionada.get()
        question, pregunta = get_Question(database,qList)
        get_Answer(question,respuesta,database)

        # Cambiar la pregunta y limpiar la selección
        self.texto_actual = f"{pregunta}"
        self.label_pregunta.config(text=self.texto_actual)
        self.respuesta_seleccionada.set("")

        if len(list(database['actual'])) <= 1:
           self.texto_actual = f"Eres el estudiante {list(database['actual'][0].values())[0]}"
           self.label_pregunta.config(text=self.texto_actual)
           self.caja_seleccion.destroy()
           self.boton_siguiente.config(state=tk.DISABLED,text="Finalizado")

if __name__ == "__main__":
    app = Interfaz()
    app.mainloop()
