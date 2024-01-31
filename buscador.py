import pandas as pd
from datetime import datetime

def identificador(ip):
    lista_usuarios = {
        'JORGE FUENTES': '192.168.100.77',
        'laptop': '192.168.100.78'
        }
    
    for usuario, identificador in lista_usuarios.items():
        if ip == identificador:
            return usuario 
    return False   

excel_registro = r'/home/pi/FlaskAppv2/registro almuerzos/registro.xlsx'

def escritura_excel(almuerzos,usuario,direccion):
    
    fecha = datetime.now().strftime("%Y-%m-%d")
        
    try:
        df = pd.read_excel(direccion)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['fecha','cantidad/almuerzos','responsable'])
    
    if direccion == excel_registro:   
        nueva_fila = {'fecha' :fecha,'cantidad/almuerzos':almuerzos,'responsable': usuario}
        df = df.append(nueva_fila, ignore_index=True)
        
    usuarios_repetidos = df[df['fecha'] == fecha]['responsable'].value_counts()
    if usuarios_repetidos.max()>1:
        return False

    df.to_excel(direccion, sheet_name='registro de almuerzos', index=False)
    print(df)
    return df

def filtrar_registros(año,mes,dia):

    fecha = f'{int(año)}-{int(mes):02d}-{int(dia):02d}'

    try:
        df1 = pd.read_excel(excel_registro)
        df1 = df1[df1['fecha'] == fecha]
    except KeyError:
        df1 = pd.DataFrame()

    return df1

