from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'
@app.route('/')
def index():
    return render_template('index.html')
#----------------------------nuevo----------------------------------------
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        producto = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        if 'productos' not in session:
            session['productos'] = []
        for p in session['productos']:
            if p['id'] == producto['id']:
                flash('El ID ya existe. Introduce uno único.', 'error')
                return redirect(url_for('agregar_producto'))

        session['productos'].append(producto)
        session.modified = True
        flash('Producto agregado exitosamente.', 'success')
        return redirect(url_for('listar_productos'))

    return render_template('agregar_producto.html')
#------------------------lista-------------------------------------------
@app.route('/listar_productos')
def listar_productos():
    productos = session.get('productos', [])
    return render_template('listar_productos.html', productos=productos)
#---------------------------------editar------------------------------------
@app.route('/editar_producto/<string:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    productos = session.get('productos', [])
    
 
    producto_a_editar = next((p for p in productos if p['id'] == producto_id), None)
    
    if request.method == 'POST':
  
        producto_actualizado = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }


        for p in productos:
            if p['id'] != producto_id and p['id'] == producto_actualizado['id']:
                flash('El ID ya existe. Introduce uno único.', 'error')
                return redirect(url_for('editar_producto', producto_id=producto_id))


        session['productos'] = [producto_actualizado if p['id'] == producto_id else p for p in productos]
        session.modified = True
        flash('Producto editado exitosamente.', 'success')
        return redirect(url_for('listar_productos'))

    return render_template('editar_producto.html', producto=producto_a_editar)
#-----------------------------------ELIMINAR-----------------------------------
@app.route('/eliminar_producto/<string:producto_id>')
def eliminar_producto(producto_id):
    if 'productos' in session:
        session['productos'] = [p for p in session['productos'] if p['id'] != producto_id]
        session.modified = True
        flash('Producto eliminado exitosamente.', 'success')
    return redirect(url_for('listar_productos'))

if __name__ == '__main__':
    app.run(debug=True)
