from cryptos_changes import app
from flask import flash, render_template, request, redirect, url_for
import sqlite3
from cryptos_changes.models import ValueCrypto, ConectData, APIError, errorApi
from cryptos_changes.forms import  PurchaseForm
from datetime import datetime



data_manager = ConectData()
api_manager = ValueCrypto()

@app.route("/")
def inicio():

    try:
        datos = data_manager.recuperar_datos()
        if isinstance(datos,dict):
            lista =[]
            lista.append(datos)
            return render_template("index.html",movimientos = lista)
        else:
            
            return render_template("index.html",movimientos = datos)
    except sqlite3.Error as e:
        flash("Se ha producido un error en la BBDD. Inténtelo más tarde")
        return render_template("index.html",movimientos = [])

@app.route("/purchase", methods= ['GET', 'POST'])
def purchase():
    form = PurchaseForm()
    
    
    if request.method == 'GET':
        return render_template("purchase.html", formulario = form)

    else:
        
        #validación de datos
        if form.validate():
        #recuperar datos de forms y calcular la tasa
            moneda_origen = form.moneda_from.data
            moneda_destino = form.moneda_to.data
            cantidad_origen = form.cantidad_from.data
            
            if moneda_destino == moneda_origen:
                flash("La moneda destino debe ser diferente a la moneda origen")
                return render_template("purchase.html", formulario = form)
           
            #Presionando el icono checkOk

            if  form.aceptar.data and form.cantidad_to.data:
                #Comprobar que tienes la moneda origen y suficientes fondos
                hay_fondos=True

                if (moneda_origen != form.from_hidden.data) or(moneda_destino != form.to_hidden.data) or (str(cantidad_origen) != form.cant_hidden.data):
                    flash("Se ha producido un error en los datos calculados, vuelva a calcularlo")
                    form.cantidad_to.data =None
                    return render_template("purchase.html", formulario = form)

                if moneda_origen != 'EUR':
                    cantidad_disponible = data_manager.consulta_cantidad_moneda(moneda_origen)
                    hay_fondos= True if cantidad_disponible >= cantidad_origen else False

                if hay_fondos:
  
                    try:
                        tasa = api_manager.obtenerTasa(moneda_origen,moneda_destino)
                        cantidad_destino = cantidad_origen * tasa
                        fecha = datetime.today().strftime('%d-%m-%Y')
                        hora=datetime.today().strftime('%H:%M:%S')
                        #Insertar datos en la BBDD
                        data_manager.inserta_datos(params = (fecha, hora,moneda_origen, cantidad_origen, moneda_destino, cantidad_destino))
                        return redirect(url_for("inicio"))
                    except sqlite3.Error as e:
                        flash("Se ha producido un error en la BBDD.")
                        return render_template("purchase.html", formulario = form)
                else:
                    flash("No dispones de suficientes fondos")
                    return render_template("purchase.html", formulario = form)

            #Presionando el boton calcular
            elif form.calcular.data:
                hay_fondos=True
                #Comprobar que tienes la moneda origen y suficientes fondos
                if moneda_origen != 'EUR':
                    cantidad_disponible = data_manager.consulta_cantidad_moneda(moneda_origen)
                    hay_fondos= True if cantidad_disponible >= cantidad_origen else False

                if hay_fondos:
  
                    try:
                        tasa = api_manager.obtenerTasa(moneda_origen,moneda_destino)
                        cantidad_destino = cantidad_origen * tasa
                        #Pasar el formulario y la cantidad destino
                        form.campos.data = (moneda_origen,moneda_destino, cantidad_origen)
                        form.from_hidden.data = moneda_origen
                        form.to_hidden.data = moneda_destino
                        form.cant_hidden.data = cantidad_origen
                        form.cantidad_to.data = cantidad_destino
                        pu = cantidad_origen/cantidad_destino
                        return render_template("purchase.html",formulario =  form, cantidad_to = cantidad_destino, precio_unitario = pu  )
                    except APIError as e:
                        flash(f"Se ha producido un error al consultar la API: {errorApi(e)}")
                        
                        return render_template("purchase.html", formulario = form)
                else:
                    flash("No dispones de suficientes fondos")
                    return render_template("purchase.html", formulario = form)
            else:
                flash("No se han calculado los datos correctamente, inténtelo de nuevo")
                return render_template("purchase.html", formulario = form)

        else:
            flash("Datos incorrectos")
            return render_template('purchase.html',formulario = form)


@app.route("/status")
def estado():
    
    #consultar movimientos
    try:
        totales = data_manager.consulta_total_inversion()
        resultados =[]
        criptos =[]
        if totales:
            cambios = api_manager.obtener_cambio_a_euros()
            ganancias_perdidas= 0.0
            valor_compra= 0.0
            valor_actual = 0.0
            invertido = data_manager.consulta_euros_invertidos()
            recuperado = data_manager.consulta_euros_recuperados()
            valor_compra = invertido - recuperado
            for total_moneda in totales:
                moneda =total_moneda[0]
                cantidad_moneda = total_moneda[1]
                total_eur=0
                if cantidad_moneda>0:
                    if moneda!= 'EUR':
                        total_eur= cantidad_moneda * cambios[moneda]
                        criptos.append(total_moneda)
                    else:
                        total_eur = cantidad_moneda
                    valor_actual += total_eur
                
            ganancias_perdidas= valor_actual - valor_compra

            resultados.append(round(invertido,2))
            resultados.append(round(valor_actual,2))
            resultados.append(round(recuperado,2))
            resultados.append(round(valor_compra,2))
            resultados.append(round(ganancias_perdidas,2))
            resultados.append(round(ganancias_perdidas > 0))

        return render_template("status.html", contenido = resultados)

    except sqlite3.Error as e:
        flash("Se ha producido un error en la base de datos. Inténtelo de nuevo más tarde")
        return render_template("index.html",movimientos = [])