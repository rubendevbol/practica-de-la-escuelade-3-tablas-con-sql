from flask import Flask, render_template, redirect, request, url_for, flash
import  sqlite3 as sql
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")




#Funcion para conectar la base de datos
def get_db_conn():
    conn = sql.connect("db_instituto.db")
    conn.row_factory = sql.Row
    return conn

def init_db():
    conn = get_db_conn()
    conn.execute("""
                    CREATE TABLE IF NOT EXISTS estudiantes(
                        id INTEGER PRIMARY KEY,
                        nombres TEXT NOT NULL,
                        apellidos TEXT NOT NULL,
                        fecha_nacimiento DATE not null
                    )
                """)
    
    conn.execute('''
                    CREATE TABLE IF NOT EXISTS cursos(
                        id INTEGER PRIMARY KEY,
                        descripcion TEXT NOT NULL,
                        horas INTEGER NOT NULL
                    )
                ''')
    
    conn.execute('''
                    CREATE TABLE IF NOT EXISTS inscripciones(
                        id INTEGER PRIMARY KEY,
                        fecha DATE NOT NULL,
                        estudiante_id INTEGER,
                        curso_id INTEGER,
                        FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
                        FOREIGN KEY (curso_id) REFERENCES cursos(id)
                    )
                ''')
    conn.commit()
    conn.close()
    
init_db()

    
@app.route("/")
def index():
    return redirect(url_for("estudiantes"))

@app.route("/estudiantes")
def estudiantes():
    conn = get_db_conn()
    estudiantes = conn.execute("SELECT * FROM estudiantes").fetchall()
    conn.close()
    return render_template("estudiantes.html",estudiantes = estudiantes)

@app.route("/cursos")
def cursos():
    conn = get_db_conn()
    cursos = conn.execute("SELECT * FROM cursos").fetchall()
    conn.close()
    return render_template("cursos.html",cursos=cursos)

@app.route("/inscripciones")
def inscripciones():
    conn = get_db_conn()
    inscripciones = conn.execute('''
                                    SELECT i.id,
                                        i.fecha,
                                        e.nombres ||" "|| e.apellidos as estudiante,
                                        c.descripcion as curso
                                    FROM inscripciones i
                                    JOIN estudiantes e ON i.estudiante_id = e.id
                                    JOIN cursos c ON i.curso_id = c.id
                                ''').fetchall()
    conn.close()
    return render_template("inscripciones.html", inscripciones=inscripciones)






@app.route("/new_estudent",methods=["POST","GET"])
def nuevo_estudiante():
    if request.method == "POST":
        nombres = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        fecha_nac = request.form.get("fecha_nac")
        
        conn = get_db_conn()
        conn.execute("INSERT INTO estudiantes(nombres,apellidos,fecha_nacimiento) VALUES (?,?,?)",(nombres, apellidos, fecha_nac))
        conn.commit()
        conn.close()
        
        flash("Curso Agregado Correctamente", "success")
        return redirect(url_for("estudiantes"))
        
    return render_template("formulario_estudiantes.html")

@app.route("/estudiante/editar/<int:id>", methods=["Post","get"])
def editar_estudiante(id):
    conn = get_db_conn()
    estudiante = conn.execute("SELECT * FROM estudiantes WHERE id = ?",(id,)).fetchone()
    if request.method == "Post":
        nombre = request.form.get("nombres")
        apellidos = request.form.get("apellidos")
        fecha_nac = request.form.get("fecha_nac")
        conn.execute("UPDATE estudiantes SET nombres=?, apellidos=?, fecha_nacimiento=?",(nombre, apellidos, fecha_nac))
        conn.commit()
        conn.close()
        
        flash("Estudiante Actulaizado", "Success")
        return redirect(url_for("estudiantes"))
    return render_template("formulario_estudiantes.html",estudiante=estudiante)

@app.route("/estudiante/eliminar/<int:id>")
def elimianar_estudiante(id):
    conn = get_db_conn()
    conn.execute("DELETE FROM estudiantes WHERE id=?",(id,))
    conn.commit()
    conn.close()
    
    flash("Estudiante eliminado", "success")
    return redirect(url_for("estudiantes"))








@app.route("/cursos/nuevo", methods=["POST","GET"])
def nuevo_curso():
    if request.method == "POST":
        descripcion = request.form.get("descripcion")
        horas = request.form.get("horas")
        
        conn = get_db_conn()
        conn.execute("INSERT INTO cursos(descripcion, horas) VALUES(?,?)",(descripcion, horas,))
        conn.commit()
        conn.close()
        flash("Curso Agregado", "success")
        return redirect(url_for("cursos"))
    return render_template("formulario_curso.html")

@app.route("/cursos/editar/<int:id>", methods=["POST"])
def editar_curso(id):
    conn = get_db_conn()
    curso = conn.execute("SELECT * FROM cursos WHERE id = ?",(id,)).fetchone()
    if request.method == "POST":
        descripcion = request.form.get("descripcion")
        horas = request.form.get("horas")
        
        conn.execute("UPDATE cursos SET descripcion=?,horas=?",(descripcion,horas,))
        conn.commit()
        conn.close()
        flash("Curso Actualizado", "seccess")
        return redirect(url_for("cursos"))
    return render_template("formulario_curso.html",curso=curso)

@app.route("/cursos/eliminar/<int:id>")
def eliminar_curso(id):
    conn = get_db_conn()
    conn.execute("DELETE FROM cursos WHERE id=?",(id,))
    conn.commit()
    conn.close()
    flash("Curso eliminado","success")
    return redirect(url_for("cursos"))



@app.route("/inscripciones/nueva", methods=["GET","POST"])
def nueva_inscripcion():
    conn = get_db_conn()
    if request.method == "POST":
        fecha = request.form.get("fecha")
        estudiante_id = request.form.get("estudiante_id") 
        curso_id = request.form.get("curso_id") 
        
        conn.execute("INSERT INTO inscripciones(fecha,estudiante_id,curso_id) VALUES(?,?,?)",(fecha,estudiante_id,curso_id))
        conn.commit()
        conn.close()
        
        flash("Inscripcion Realizada", "success")
        return redirect(url_for("inscripciones"))
    estudiantes = conn.execute('''
                                    SELECT id, concat(nombres," ",apellidos)  as nombre FROM estudiantes
                            ''').fetchall()
    cursos = conn.execute('''
                            SELECT id, descripcion FROM cursos
                        ''').fetchall()
    conn.close()
    return render_template("formulario_inscripciones.html", estudiantes=estudiantes, cursos=cursos)

@app.route("/inscripciones/editar/<int:id>")
def editar_inscripcion(id):
    conn = get_db_conn()
    inscripcion = conn.execute("SELECT * FROM inscripciones WHERE id=?",(id,))
    if request.method == "POST":
        fecha = request.form.get("fecha")
        estudiante_id = request.form.get("estudiante_id") 
        curso_id = request.form.get("curso_id") 
        conn.execute("UPDATE inscripciones SET fecha=?,estudiante_id=?,curso_id=?",(fecha,estudiante_id,curso_id,))
        conn.commit()
        conn.close()
        flash("Inscripcion Actualizada", "success")
        return redirect(url_for("inscripciones"))
    return render_template("formulario_inscripciones.html",inscripcion=inscripcion)

@app.route("/inscripcion/eliminar/<int:id>")
def elimianr_inscripcion():
    conn= get_db_conn()
    conn.execute("DELETE FROM inscripciones WHERE id = ?",(id,))
    conn.commit()
    conn.close()
    flash("Curso Eliminado", "seccess")
    return redirect(url_for("inscripciones"))


if __name__ == "__main__":
    app.run(debug=True,port=3000)
    