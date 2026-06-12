import tkinter as tk
from tkinter import messagebox

class CalculadoraAvanzada:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Calculadora Pro")
        self.ventana.geometry("360x520")
        self.ventana.configure(bg="#1e1e2e")  # Fondo oscuro elegante
        self.ventana.resizable(False, False)   # Congela el tamaño de la ventana

        # Variable para rastrear si el último botón presionado fue un resultado
        self.resultado_mostrado = False

        self.crear_pantalla()
        self.crear_botones()
        self.vincular_teclado()

    def crear_pantalla(self):
        # Pantalla de entrada con bordes suaves y tipografía moderna
        self.pantalla = tk.Entry(
            self.ventana, 
            font=("Segoe UI", 28), 
            bg="#252538", 
            fg="#f8f8f2", 
            borderwidth=0, 
            justify="right",
            insertbackground="#f8f8f2" # Color del cursor
        )
        # Usamos pack para darle un margen superior cómodo
        self.pantalla.pack(padx=15, pady=20, fill="x", ipady=15)

    def crear_botones(self):
        # Contenedor para la cuadrícula de botones
        contenedor_botones = tk.Frame(self.ventana, bg="#1e1e2e")
        contenedor_botones.pack(padx=10, pady=5, fill="both", expand=True)

        # Configuración de estilos por tipo de botón
        estilo_base = {"font": ("Segoe UI", 14, "bold"), "borderwidth": 0, "activeforeground": "#ffffff"}
        
        estilos = {
            "numero": {**estilo_base, "bg": "#313244", "fg": "#cdd6f4", "activebackground": "#45475a"},
            "operador": {**estilo_base, "bg": "#f38ba8", "fg": "#11111b", "activebackground": "#f5e0dc"},
            "accion": {**estilo_base, "bg": "#a6e3a1", "fg": "#11111b", "activebackground": "#94e2d5"},
            "limpiar": {**estilo_base, "bg": "#fab387", "fg": "#11111b", "activebackground": "#f9e2af"}
        }

        # Distribución de los botones (Texto, Fila, Columna, Tipo de Estilo)
        distribucion = [
            ('C', 0, 0, "limpiar"), ('(', 0, 1, "operador"), (')', 0, 2, "operador"), ('/', 0, 3, "operador"),
            ('7', 1, 0, "numero"),  ('8', 1, 1, "numero"),   ('9', 1, 2, "numero"),   ('*', 1, 3, "operador"),
            ('4', 2, 0, "numero"),  ('5', 2, 1, "numero"),   ('6', 2, 2, "numero"),   ('-', 2, 3, "operador"),
            ('1', 3, 0, "numero"),  ('2', 3, 1, "numero"),   ('3', 3, 2, "numero"),   ('+', 3, 3, "operador"),
            ('0', 4, 0, "numero"),  ('.', 4, 1, "numero"),   ('=', 4, 2, "accion")
        ]

        # Configurar peso de filas y columnas para que se expandan proporcionalmente
        for i in range(5):
            contenedor_botones.rowconfigure(i, weight=1)
        for i in range(4):
            contenedor_botones.columnconfigure(i, weight=1)

        # Renderizar botones en la interfaz
        for texto, fila, col, tipo in distribucion:
            # El botón '=' ocupa dos columnas en la última fila
            colspan = 2 if texto == '=' else 1
            
            comando = self.obtener_comando(texto)
            btn = tk.Button(contenedor_botones, text=texto, command=comando, **estilos[tipo])
            btn.grid(row=fila, column=col, columnspan=colspan, sticky="nsew", padx=4, pady=4)

    def obtener_comando(self, texto):
        """Asigna la función correcta a cada botón"""
        if texto == '=':
            return self.calcular_resultado
        elif texto == 'C':
            return self.limpiar_pantalla
        else:
            return lambda: self.presionar_tecla(texto)

    def presionar_tecla(self, valor):
        # Si acabamos de mostrar un resultado y el usuario presiona un número, borra la pantalla
        if self.resultado_mostrado and valor.isdigit():
            self.limpiar_pantalla()
        self.resultado_mostrado = False
        self.pantalla.insert(tk.END, valor)

    def limpiar_pantalla(self):
        self.pantalla.delete(0, tk.END)

    def calcular_resultado(self):
        try:
            expresion = self.pantalla.get()
            # Validar que no esté vacía
            if not expresion: 
                return
            
            # Reemplazar caracteres visuales si los hubiera (ej. si usaras 'x' en vez de '*')
            resultado = eval(expresion)
            
            # Si el resultado es flotante pero termina en .0, lo mostramos como entero
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)

            self.limpiar_pantalla()
            self.pantalla.insert(tk.END, str(resultado))
            self.resultado_mostrado = True
        except ZeroDivisionError:
            messagebox.showerror("Error", "No se puede dividir entre cero.")
            self.limpiar_pantalla()
        except Exception:
            messagebox.showerror("Error", "Expresión matemática inválida.")

    def vincular_teclado(self):
        """Permite usar el teclado físico para operar la calculadora"""
        self.ventana.bind("<Key>", self.evento_teclado)

    def evento_teclado(self, evento):
        tecla = evento.char
        if tecla in "0123456789+-*/().":
            self.presionar_tecla(tecla)
        elif tecla == "\r" or tecla == "=":  # Enter o signo igual
            self.calcular_resultado()
        elif tecla == "\x08":  # Retroceso (Backspace)
            # Borra el último carácter
            texto_actual = self.pantalla.get()
            self.limpiar_pantalla()
            self.pantalla.insert(tk.END, texto_actual[:-1])
        elif evento.keysym == "Escape":
            self.limpiar_pantalla()


# Ejecución de la aplicación
if __name__ == "__main__":
    raiz = tk.Tk()
    app = CalculadoraAvanzada(raiz)
    raiz.mainloop()
    