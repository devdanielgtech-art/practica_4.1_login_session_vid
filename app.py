from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]
        
        if usuario == 'admin' and password == '123':
            return render_template("dashboard.html", usuario=usuario)
        else:
            return render_template("index.html", error="Credenciales incorrectas")
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)