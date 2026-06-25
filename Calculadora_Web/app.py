# app.py
from flask import Flask, render_template, request, session
from calculadora import Calculadora  # Importación modular de nuestra clase

app = Flask(__name__)
app.secret_key = "clave_secreta_para_sesiones_flask" # Necesario para usar 'session'

@app.route("/", methods=["GET", "POST"])
def index():
    # Inicializar la pantalla en la sesión si no existe
    if "pantalla" not in session:
        session["pantalla"] = ""

    if request.method == "POST":
        accion = request.form.get("accion")
        
        if accion == "C":
            session["pantalla"] = ""
        
        elif accion == "=":
            # Instanciamos el objeto usando el constructor de la clase modular
            calc = Calculadora(session["pantalla"])
            resultado = calc.calcular()
            
            # Si hay un error, lo mostramos, si no, guardamos el resultado
            session["pantalla"] = resultado
            # Bandera para que la siguiente tecla borre el error si es necesario
            session["resultado_mostrado"] = True 
            
        else:
            # Controlar si reescribir la pantalla tras un error o resultado previo
            if session.get("resultado_mostrado") and (accion.isdigit() or accion == "("):
                session["pantalla"] = ""
            elif "Error" in session["pantalla"]:
                session["pantalla"] = ""
                
            session["resultado_mostrado"] = False
            session["pantalla"] += accion

    return render_template("index.html", pantalla=session["pantalla"])

if __name__ == "__main__":
    app.run(debug=True)