from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__)
app.secret_key = "12638149lp"

# Usuarios registrados (se mantienen mientras la app corre)
usuarios_registrados = {}

# Lista de colores disponibles
colores_disponibles = {
    "rojo": "#FF0000",
    "azul": "#0000FF",
    "verde": "#00FF00",
    "amarillo": "#FFFF00",
    "morado": "#800080",
    "naranja": "#FFA500",
    "rosa": "#FFC0CB",
    "celeste": "#00FFFF",
    "gris": "#808080",
    "marron": "#8B4513",
    "violeta": "#EE82EE",
    "turquesa": "#40E0D0"
}

@app.route("/")
def index():
    # Verificar si hay cookie de usuario
    usuario = request.cookies.get('usuario_actual')
    if usuario and usuario in usuarios_registrados:
        return redirect(url_for('bienvenido'))
    return redirect(url_for('login'))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        color_favorito = request.form.get("color")
        
        # Verificar si el usuario ya existe
        if usuario in usuarios_registrados:
            return render_template('registro.html', mensaje="Usuario o contraseña incorrectos", colores=colores_disponibles)
        
        # Guardar el nuevo usuario
        usuarios_registrados[usuario] = {
            "password": password,
            "color": color_favorito
        }
        
        # Redirigir al login sin cookies temporales
        return redirect(url_for('login'))
    
    return render_template('registro.html', colores=colores_disponibles)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")
        
        # Verificar credenciales
        if usuario in usuarios_registrados and usuarios_registrados[usuario]["password"] == password:
            # Crear respuesta con cookies permanentes
            response = make_response(redirect(url_for('bienvenido')))
            response.set_cookie('usuario_actual', usuario, max_age=3600)
            response.set_cookie('color_actual', usuarios_registrados[usuario]["color"], max_age=3600)
            return response
        else:
            return render_template('login.html', mensaje="Usuario o contraseña incorrectos")
    
    return render_template('login.html')

@app.route("/bienvenido")
def bienvenido():
    usuario = request.cookies.get('usuario_actual')
    color = request.cookies.get('color_actual')
    
    if not usuario or usuario not in usuarios_registrados:
        return redirect(url_for('login'))
    
    # Obtener el valor hexadecimal del color
    color_hex = colores_disponibles.get(color, "#FFFFFF")
    
    return render_template('bienvenido.html', usuario=usuario, color=color, color_hex=color_hex)

@app.route("/logout")
def logout():
    response = make_response(redirect(url_for('login')))
    response.set_cookie('usuario_actual', '', expires=0)
    response.set_cookie('color_actual', '', expires=0)
    return response

if __name__ == "__main__":
    app.run(debug=True)