from flask import Flask, render_template, request,redirect,url_for, flash
from flaskext.mysql import MySQL
import pymysql
 

mysql = MySQL()
app = Flask(__name__)

db = pymysql.connect(
    host="localhost", port=3306, user="root",
    passwd="sacv4ecs", db="flaskcontacts"
)
#mysql.init_app(app)

app.secret_key='mysecretkey'

@app.route('/')

def Index():
    cur = db.cursor()
    cur.execute('select * from contacts')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'] )
def add_contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        cursor = db.cursor()
        cursor.execute('INSERT INTO contacts (nombre, telefono, email) VALUES (%s, %s, %s)', 
        (nombre,telefono,email))
        db.commit()
        flash('Contacto agregado correctamente')
        return redirect(url_for('Index'))

  
@app.route('/edit/<id>')
def get_contact(id):
    cur = db.cursor()
    cur.execute('SELECT * FROM contacts WHERE id= %s', (id))
    data = cur.fetchall()
    print(data)
    return render_template('edit-contact.html', contact = data[0] )

@app.route('/update/<id>', methods=['POST'] )
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = db.cursor()
        cur.execute("""
        UPDATE contacts
        SET nombre = %s,
            telefono =%s,
            email = %s
        WHERE id = %s       
        """, (nombre,telefono,email,id))
        db.commit()
        flash('Contacto actualizado correctamente... ')
        return redirect(url_for('Index')) 

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = db.cursor()
    cur.execute('DELETE FROM contacts WHERE id= {0}'.format(id))
    db.commit()
    flash('Contacto removido satisfactoriamente ')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
