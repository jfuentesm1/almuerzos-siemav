from flask import Flask, render_template, request
import datetime
import buscador as bus
app = Flask(__name__)

def usuarios():
    ip_user = request.remote_addr
    usuario = bus.identificador(ip_user)
    return usuario

def semana():
    fecha = datetime.datetime.now()
    hora_actual = datetime.datetime.now().time()
    semana = fecha.isocalendar()[1]
    return semana , hora_actual

def escritura_excel():

    direccion= r'/home/pi/FlaskAppv2/registro almuerzos/registro.xlsx'
    usuario = usuarios()

    if 'pedido' in request.form:
        almuerzos = request.form.get('recibidas')
        try:
            if int(almuerzos)>5:
                return False
            else:        
                excel_registro = bus.escritura_excel(almuerzos, usuario, direccion)              
                return excel_registro
        except ValueError:
            return False

def lectura_excel():
    if 'revisar_almuerzos' in request.form:
        año = request.form['year']
        mes = request.form['month']
        dia = request.form['day']
        try:
            df = bus.filtrar_registros(año,mes,dia) 
            return df
        except ValueError:
            return False

@app.route('/', methods=['GET', 'POST'])
def index():
    hora_referencia = datetime.time(8,30,0) 
    titulo = usuarios()
    fecha, hora = semana()

    if titulo is False:
        return render_template('exit.html')
    
    elif hora < hora_referencia:
        return render_template('error.html')
    
    else:
        return render_template('index.html', titulo=titulo, fecha = fecha)


@app.route('/reporte', methods=['POST'])
def reporte_diario():
    titulo = usuarios()
    registro = escritura_excel()

    if registro is False:
        return render_template('error.html')
    else:
        return render_template('final.html', titulo=titulo) 
    
@app.route('/lecturas', methods=['POST'])
def lectura():
    df = lectura_excel()

    if df is False:
        return render_template('error.html')
    else:
        return render_template('dataframe.html', table= df.to_html(classes='table table-striped'))

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
