# calculadora.py

class Calculadora:
    def __init__(self, expresion=""):
        """Constructor que inicializa la expresión matemática."""
        self.expresion = expresion

    def limpiar_expresion(self):
        """Sanitiza la entrada por seguridad antes de evaluar."""
        # Permitir solo números, operadores básicos, puntos y paréntesis
        caracteres_validos = "0123456789+-*/(). "
        self.expresion = "".join([c for c in self.expresion if c in caracteres_validos])

    def calcular(self):
        """Evalúa la expresión y maneja errores matemáticos."""
        self.limpiar_expresion()
        
        if not self.expresion:
            return ""

        try:
            # Evaluar la expresión sanitizada
            resultado = eval(self.expresion)
            
            # Formatear el resultado para mejorar la experiencia de usuario
            if isinstance(resultado, float):
                if resultado.is_integer():
                    return str(int(resultado))
                else:
                    return str(round(resultado, 10)) # Evita flotantes infinitos
            return str(resultado)
            
        except ZeroDivisionError:
            return "Error: División entre cero"
        except Exception:
            return "Error: Expresión inválida"