from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Cliente
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from app import app, db
from app.models import Cliente
from werkzeug.security import generate_password_hash, check_password_hash

# Configura Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(cliente_id):
    return Cliente.query.get(int(cliente_id))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente.', 'success')
    return redirect(url_for('index'))
    
   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Busca el usuario en la base de datos
        cliente = Cliente.query.filter_by(email=email).first()

        # Verifica las credenciales
        if cliente and check_password_hash(cliente.password, password):
            login_user(cliente)  # Inicia sesión con el usuario
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo electrónico o contraseña incorrectos.', 'error')

    return render_template('login.html')

@app.route('/ubicaciones')
@login_required  # Solo usuarios logueados pueden acceder
def ubicaciones():
    # Datos de ejemplo
    gimnasios = [
        {
            "nombre": "PowerFit Centro",
            "direccion": "Av. Principal 123, Ciudad",
            "horario": "Lunes a Viernes: 5:00 AM - 10:00 PM",
            "imagen": "gym_centro.jpg"
        },
        {
            "nombre": "PowerFit Norte",
            "direccion": "Calle Secundaria 456, Ciudad",
            "horario": "Lunes a Domingo: 6:00 AM - 9:00 PM",
            "imagen": "gym_norte.jpg"
        }
    ]
    return render_template('ubicaciones.html', gimnasios=gimnasios)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
@login_required  # Requiere que el usuario esté autenticado
def products():
    return render_template('products.html')

@app.route('/pagar/<plan>')
@login_required  # Asegura que el usuario esté autenticado
def pagar(plan):
    # Define la información del plan según el parámetro
    if plan == 'basico':
        plan_info = {
            'nombre': 'Plan Básico',
            'precio': '$299/mes',
            'descripcion': 'Acceso a todas las áreas del gimnasio.'
        }
    elif plan == 'premium':
        plan_info = {
            'nombre': 'Plan Premium',
            'precio': '$599/mes',
            'descripcion': 'Acceso ilimitado + entrenador personal.'
        }
    elif plan == 'familiar':
        plan_info = {
            'nombre': 'Plan Familiar',
            'precio': '$899/mes',
            'descripcion': 'Para ti y tu familia, con descuentos especiales.'
        }
    else:
        flash('Plan no válido.', 'error')
        return redirect(url_for('index'))

    return render_template('pagar.html', plan_info=plan_info)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        telefono = request.form['telefono']

        # Verifica si las contraseñas coinciden
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('register'))

        # Verifica si el email ya está registrado
        cliente_existente = Cliente.query.filter_by(email=email).first()
        if cliente_existente:
            flash('Este email ya está registrado.', 'error')
            return redirect(url_for('register'))

        # Crea un nuevo cliente
        nuevo_cliente = Cliente(
            nombre=nombre,
            email=email,
            password=generate_password_hash(password),  # Hashea la contraseña
            telefono=telefono
        )
        db.session.add(nuevo_cliente)
        db.session.commit()

        flash('¡Gracias por registrarte en VitalFit!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html')
