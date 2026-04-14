from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # verificar si esta logueado
    usuario = request.form["usuario"]
    password = request.form["password"]
    return render_template("login.html", usuario=usuario, password=password)


    if usuario == 'admin' and password == '123':
        return render_template("dashboard.html", usuario=usuario)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)