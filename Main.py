import uuid
import webbrowser
from PyQt5 import QtWidgets, uic, QtCore
import sys
import os.path
import os
from PyQt5.QtGui import QPixmap
from graphviz import Digraph
from Lexico import automata

class ventana (QtWidgets.QMainWindow):

    #Constructor
    def __init__(self):
        super(ventana, self).__init__()
        uic.loadUi('Principal.ui', self)
        global direccion
        global nombre
        direccion = ''
        nombre = ''
        self.a = Digraph('Arbol',format='png') #Arbol de Ejecución
        self.t = [] #Lista de Tokens
        self.e = [] #Lista de Errores
        self.eg = [] #Lista de Errores Gramaticales
        self.resultado = [] #Almacena el reusltado del analisis lexico
        self.cargar.clicked.connect(self.carga)
        self.analizar.clicked.connect(self.analisis)
        self.error.clicked.connect(self.errores)
        self.arbol.clicked.connect(self.arboles)
        self.token.clicked.connect(self.tokens)
        self.n0 =""
        self.n1 =""
        self.n01 =""
        self.claves = []
        self.registros = []
        self.valban = "" #Sirven para mover lo leido  por el metodo val
        self.valnodos = [] #Sirven para mover lo leido  por el metodo val
        self.regban = "" #Sirven para mover lo leido  por el metodo reg
        self.valrban = "" #Sirven para mover lo leido  por el metodo reg
        self.regnodos = [] #Sirven para mover lo leido  por el metodo reg
        self.regnodost = []
        self.temp = [] #Guarda los valores de registro temporal
        self.show()

    #Metodo de carga de archivos
    def carga(self): 
        global direccion
        direccion = ''
        direccion = QtWidgets.QFileDialog.getOpenFileName(self, "Abrir Archivo", "C:\\", "Archivos .lfp (*.lfp)")
        if direccion[0] != "":
            try:
                archivo = open(direccion[0], 'r')
                cadena = archivo.read()
                archivo.close()
                self.texto.setText(cadena)
                exito = QtWidgets.QMessageBox()
                exito.setText("Archivo cargado con exito.")
                exito.setIcon(QtWidgets.QMessageBox.Information)
                exito.setWindowTitle("Mensaje")
                exito.exec_()

            except:
                error = QtWidgets.QMessageBox()
                error.setText("Ocurrió un error. Verifique su archivo o intente de nuevo.")
                error.setIcon(QtWidgets.QMessageBox.Warning)
                error.setWindowTitle("Error")
                error.exec_()

    
    #Método que interpreta el código ingresado en la caja de texto
    def analisis(self):
        self.a = Digraph('Arbol',format='png') #Arbol de Ejecución
        self.claves = []
        self.registros = []
        self.eg = []
        self.consola.setText("")
        cadena = self.texto.toPlainText()
        if cadena == '':
            pass
        else:
            #Codigo del automata
            self.resultado = automata(cadena)
            self.t = self.resultado[0]
           

    #Método que genera un html con el arbol gramatical de la ultima ejecución del codigo
    def arboles(self):
        try:
            self.a.view()
        except:
            pass

    #Método que genera un html con los errores encontrados en la ultima ejecución del codigo
    def errores(self):
         webbrowser.open_new_tab('Errores.html')

    #Método que genera un html con los tokens de la ultima ejecución del codigo
    def tokens(self):
        webbrowser.open_new_tab('Tokens.html')

    #Analiador Lexico que ejecuta instrucciones y crea el arbol. Regresa una lista con los errores.
    def parser (self):
        #Preparar Listas
        self.valban = "" 
        self.valnodos = []
        self.valban = 0
        self.regnodos = []
        self.regban = 0
        self.valrban = 0
        #---Preparar los tokens como una pila
        self.t.reverse()
        
        #---Nodo Inicial
        I = self.nuevo("Inicio")
        self.n0 = self.nuevo("S0")
        self.add(I, self.n0)
        
        #---Analizador
        self.S1()

    #Estados del Analizador
    #---Diferencia si vienen Datos o Instrucciones
    def S1(self):
        try:
            temp = self.t[-1]
            t = temp[0].lower()
            if temp[1] == "Reservada":

                #---Agrega los nodos axioma al arbol
                self.n1 = self.nuevo("S1")
                self.add(self.n0, self.n1)
                self.n01 = self.nuevo("S0'")
                self.add(self.n0, self.n01)
                self.n0 = self.n01

                if t == "claves" or t == "registros":
                    self.datos()
                    self.S1()

                elif t == "imprimir" or t == "imprimirln" or t == "conteo" or  t == "promedio" or t == "contarsi" or t =="datos" or t == "sumar" or t == "max" or t == "min" or t == "exportarreporte":
                    self.ins()
                    self.S1()

            else: 
                self.eg.append([temp[1], "Palabra Reservada", temp[2], temp[3]])
                self.t.pop()
                self.S1()
        except:
            vacio = self.nuevo("ε")
            self.add(self.n0, vacio)
        
    #---Analizador de Instrucciones
    def ins(self):
        temp = self.t[-1]
        t = temp[0].lower() 
        n1 = self.nuevo('Instruccion')

        #---Analisis de Imprimir
        if t == "imprimir":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'imprimir':
                n2 = self.nuevo('Imprimir')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Parentesis Cierre":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Punto y Coma":
                                n2 = self.nuevo(t[0])
                                self.add(n1, n2)
                                self.add(self.n1, n1)
                                cadena = self.consola.toPlainText()
                                cadena = cadena + cad
                                self.consola.setText(cadena)
                            else:
                                self.eg.append([t[1], "Punto y Coma", t[2], t[3]])
                        else:
                            self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])

        #---Analisis de ImprimirLn
        elif t == "imprimirln":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'imprimirln':
                n2 = self.nuevo('ImprimirLn')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Parentesis Cierre":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Punto y Coma":
                                n2 = self.nuevo(t[0])
                                self.add(n1, n2)
                                self.add(self.n1, n1)
                                cadena = self.consola.toPlainText()
                                cadena = cadena + "\n" + cad
                                self.consola.setText(cadena)
                            else:
                                self.eg.append([t[1], "Punto y Coma", t[2], t[3]])                   
                        else:
                            self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])

        #---Analisis de Conteo
        elif t == "conteo":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'conteo':
                n2 = self.nuevo('Conteo')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Parentesis Cierre":
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Punto y Coma":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            self.add(self.n1, n1)
                            cad = str(len(self.registros))
                            cadena = self.consola.toPlainText()
                            cadena = cadena + "\n" + cad
                            self.consola.setText(cadena)
                        else:
                            self.eg.append([t[1], "Punto y Coma", t[2], t[3]])    
                    else:
                        self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])

        #---Analisis de Promedio
        elif t == "promedio":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'promedio':
                n2 = self.nuevo('Promedio')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Parentesis Cierre":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Punto y Coma":
                                n2 = self.nuevo(t[0])
                                self.add(n1, n2)
                                self.add(self.n1, n1)
                                #Ejecución de la Instrucción
                                if len(self.registros) == 0 or len(self.claves) == 0:
                                    resu = "ERROR: No hay información cargada para los arreglos o claves." 
                                else:
                                    t = len(self.claves) 
                                    b0 = 0
                                    for a in self.registros:
                                        if t != len(a):
                                            b0 = 1
                                    if b0 == 1:
                                        resu = "ERROR: El numero de claves y el numero de valores de uno o más registros no concuerdan." 
                                    else:
                                        if cad in self.claves:
                                            res = self.claves.index(cad)
                                        else:
                                            res = -1
                                        b = 0
                                        if res == -1:
                                            resu = "ERROR: No existe dicha clave en el listado de arreglos."
                                        else:
                                            resu = 0
                                            for a in self.registros:
                                                if a[res].isnumeric():
                                                    resu = resu + float(a[res])
                                                    b = 1
                                                
                                                elif self.isfloat(a[res]):
                                                    d = float(a[res])
                                                    resu += d
                                                    b = 1
                                                else:
                                                    resu = "ERROR: La clave seleccionada maneja texto." 
                                                    b = 0
                                                        
                                            if b == 1:
                                                resu = resu / len(self.registros)
                                                resu = str(resu)
                                cadena = self.consola.toPlainText()
                                cadena = cadena + "\n" + resu
                                self.consola.setText(cadena)
                            else:
                                self.eg.append([t[1], "Punto y Coma", t[2], t[3]])             
                        else:
                            self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])


        #---Analisis de ContarSI
        elif t == "contarsi":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'contarsi':
                n2 = self.nuevo('ContarSi')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Coma":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Cadena" or t[1] == "Numero":
                                valor = t[0]
                                nt = self.nuevo("Tipo")
                                self.add(n1, nt)
                                n2 = self.nuevo(t[0])
                                self.add(nt, n2)
                                t = self.t.pop()
                                if t[1] == "Parentesis Cierre":
                                    n2 = self.nuevo(t[0])
                                    self.add(n1, n2)
                                    t = self.t.pop()
                                    if t[1] == "Punto y Coma":
                                        n2 = self.nuevo(t[0])
                                        self.add(n1, n2)
                                        self.add(self.n1, n1)
                                        #Ejecución de la Instrucción
                                        if len(self.registros) == 0 or len(self.claves) == 0:
                                            resu = "ERROR: No hay información cargada para los arreglos o claves." 
                                        else:
                                            t = len(self.claves) 
                                            b0 = 0
                                            for a in self.registros:
                                                if t != len(a):
                                                    b0 = 1
                                            if b0 == 1:
                                                resu = "ERROR: El numero de claves y el numero de valores de uno o más registros no concuerdan." 
                                            else:
                                                if cad in self.claves:
                                                    res = self.claves.index(cad)
                                                else:
                                                    res = -1
                                                b = 0
                                                if res == -1:
                                                    resu = "ERROR: No existe dicha clave en el listado de arreglos."
                                                else:
                                                    resu = 0
                                                    for a in self.registros:
                                                        if a[res] == valor:
                                                            resu += 1
                                                    resu = str(resu)
                                        cadena = self.consola.toPlainText()
                                        cadena = cadena + "\n" + resu
                                        self.consola.setText(cadena) 
                                    else:
                                        self.eg.append([t[1], "Punto y Coma", t[2], t[3]])
                                else:
                                    self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                            else:
                                self.eg.append([t[1], "Numero o Cadena", t[2], t[3]])
                        else:
                            self.eg.append([t[1], "Coma", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])


        #---Analisis de Datos
        elif t == "datos":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'datos':
                n2 = self.nuevo('Datos')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Parentesis Cierre":
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Punto y Coma":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            self.add(self.n1, n1)
                            #Ejecución de la Instrucción
                            resu = ""
                            if len(self.registros) == 0 or len(self.claves) == 0:
                                resu = "ERROR: No hay información cargada para los arreglos o claves." 
                            else:
                                t = len(self.claves) 
                                ba = 0
                                for a in self.registros:
                                    if t != len(a):
                                        ba = 1   
                                if ba == 1:
                                    resu = "ERROR: El numero de claves y el numero de valores de uno o más registros no concuerdan." 
                                else:
                                    cadena = self.consola.toPlainText() 
                                    cadena += "\n" + "Claves:"
                                    for a in self.claves:
                                        cadena += " " + a
                                    cadena += "\n" + "Registros:" + "\n"
                                    for b in self.registros:
                                        for c in b:
                                            cadena += " " + c
                                        cadena += " ; " + "\n"
                                    self.consola.setText(cadena)   

                            cadena = self.consola.toPlainText()
                            cadena = cadena + "\n" + resu
                            self.consola.setText(cadena)
                        else:
                            self.eg.append([t[1], "Punto y Coma", t[2], t[3]]) 
                    else:
                        self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])

        #---Analisis de Sumar
        elif t == "sumar":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'sumar':
                n2 = self.nuevo('Sumar')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Parentesis Cierre":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Punto y Coma":
                                n2 = self.nuevo(t[0])
                                self.add(n1, n2)
                                self.add(self.n1, n1)
                                #Ejecución de la Instrucción
                                if len(self.registros) == 0 or len(self.claves) == 0:
                                    resu = "ERROR: No hay información cargada para los arreglos o claves." 
                                else:
                                    t = len(self.claves) 
                                    b0 = 0
                                    for a in self.registros:
                                        if t != len(a):
                                            b0 = 1
                                    if b0 == 1:
                                        resu = "ERROR: El numero de claves y el numero de valores de uno o más registros no concuerdan." 
                                    else:
                                        if cad in self.claves:
                                            res = self.claves.index(cad)
                                        else:
                                            res = -1
                                        b = 0
                                        if res == -1:
                                            resu = "ERROR: No existe dicha clave en el listado de arreglos."
                                        else:
                                            resu = 0
                                            for a in self.registros:
                                                if a[res].isnumeric():
                                                    resu = resu + float(a[res])
                                                    b = 1
                                                elif self.isfloat(a[res]):
                                                    d = float(a[res])
                                                    resu += d
                                                    b = 1
                                                else:
                                                    resu = "ERROR: La clave seleccionada maneja texto." 
                                                    b = 0
        
                                            if b == 1:
                                                resu = str(resu)
                                cadena = self.consola.toPlainText()
                                cadena = cadena + "\n" + resu
                                self.consola.setText(cadena)
                            else:
                                self.eg.append([t[1], "Punto y Coma", t[2], t[3]]) 
                        else:
                            self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])


        #---Analisis de Max
        elif t == "max":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'max':
                n2 = self.nuevo('Max')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Parentesis Cierre":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Punto y Coma":
                                n2 = self.nuevo(t[0])
                                self.add(n1, n2)
                                self.add(self.n1, n1)
                                #Ejecución de la Instrucción
                                if len(self.registros) == 0 or len(self.claves) == 0:
                                    resu = "ERROR: No hay información cargada para los arreglos o claves." 
                                else:
                                    t = len(self.claves) 
                                    b0 = 0
                                    for a in self.registros:
                                        if t != len(a):
                                            b0 = 1
                                    if b0 == 1:
                                        resu = "ERROR: El numero de claves y el numero de valores de uno o más registros no concuerdan." 
                                    else:
                                        if cad in self.claves:
                                            res = self.claves.index(cad)
                                        else:
                                            res = -1
                                        b = 0
                                        if res == -1:
                                            resu = "ERROR: No existe dicha clave en el listado de arreglos."
                                        else:
                                            temo = []
                                            for a in self.registros:
                                                if a[res].isnumeric():
                                                    temo.append(float(a[res]))
                                                
                                                elif self.isfloat(a[res]):
                                                    temo.append(float(a[res]))
                                                else:
                                                    temo.append(a[res])
                                            resu = max(temo)
                                cadena = self.consola.toPlainText()
                                cadena = cadena + "\n" + str(resu)
                                self.consola.setText(cadena)
                            else:
                                self.eg.append([t[1], "Punto y Coma", t[2], t[3]])
                        else:
                            self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])


        #---Analisis de Min
        elif t == "min":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'min':
                n2 = self.nuevo('Min')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Parentesis Cierre":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Punto y Coma":
                                n2 = self.nuevo(t[0])
                                self.add(n1, n2)
                                self.add(self.n1, n1)
                                #Ejecución de la Instrucción
                                if len(self.registros) == 0 or len(self.claves) == 0:
                                    resu = "ERROR: No hay información cargada para los arreglos o claves." 
                                else:
                                    t = len(self.claves) 
                                    b0 = 0
                                    for a in self.registros:
                                        if t != len(a):
                                            b0 = 1
                                    if b0 == 1:
                                        resu = "ERROR: El numero de claves y el numero de valores de uno o más registros no concuerdan." 
                                    else:
                                        if cad in self.claves:
                                            res = self.claves.index(cad)
                                        else:
                                            res = -1
                                        b = 0
                                        if res == -1:
                                            resu = "ERROR: No existe dicha clave en el listado de arreglos."
                                        else:
                                            temo = []
                                            for a in self.registros:
                                                if a[res].isnumeric():
                                                    temo.append(float(a[res]))
                                                
                                                elif self.isfloat(a[res]):
                                                    temo.append(float(a[res]))
                                                else:
                                                    temo.append(a[res])
                                            resu = min(temo)
                                cadena = self.consola.toPlainText()
                                cadena = cadena + "\n" + str(resu)
                                self.consola.setText(cadena)
                            else:
                                self.eg.append([t[1], "Punto y Coma", t[2], t[3]]) 
                        else:
                            self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])


        #---Analisis de Exportar
        elif t == "exportarreporte":
            t = self.t.pop()
            t = t[0].lower()
            if t == 'exportarreporte':
                n2 = self.nuevo('ExportarReporte')
                self.add(n1, n2)
                t = self.t.pop()
                if t[1] == "Parentesis Abrir":
                    n2 = self.nuevo(t[0])
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Cadena":
                        cad = t[0]
                        n2 = self.nuevo(t[0])
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Parentesis Cierre":
                            n2 = self.nuevo(t[0])
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Punto y Coma":
                                n2 = self.nuevo(t[0])
                                self.add(n1, n2)
                                self.add(self.n1, n1)
                                #Ejecución de la Instrucción
                                if len(self.registros) == 0 or len(self.claves) == 0:
                                    resu = "ERROR: No hay información cargada para los arreglos o claves." 
                                else:
                                    t = len(self.claves) 
                                    ba = 0
                                    for a in self.registros:
                                        if t != len(a):
                                            ba = 1
                                    if ba == 1:
                                        resu = "ERROR: El numero de claves y el numero de valores de uno o más registros no concuerdan." 
                                    else:
                                        resu = "Mensaje: Reporte Creado con Exito"
                                        html = open('Reporte.html', 'w')
                                        html.write('<!DOCTYPE html>')
                                        html.write('<html>')
                                        html.write('    <head>')
                                        html.write('        <title'+cad+'</title>')
                                        html.write('        <style>')
                                        html.write('            *{')
                                        html.write('                background-color: #eff7e1;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('              }')
                                        html.write('            h1{')
                                        html.write('                color: #222831;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('              }')
                                        html.write('            h2{')
                                        html.write('                color: #30475e;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('              }')
                                        html.write('            h3{')
                                        html.write('                color: #f05454;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('              }')
                                        html.write('            aside{')
                                        html.write('                background-color: #214151;')
                                        html.write('                color: #663F3F;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('              }')
                                        html.write('            header{')
                                        html.write('                background-color: #a2d0c1;')
                                        html.write('                color: #663F3F;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('              }')
                                        html.write('            footer{')
                                        html.write('                background-color: #f8dc81;')
                                        html.write('                color: #663F3F;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('              }')
                                        html.write('            table{')
                                        html.write('                width: 100%')
                                        html.write('                border-collapse: collapse;')
                                        html.write('                font-family: "Arial Narrow";')
                                        html.write('            td, th{')
                                        html.write('                border: 1px solid #dddddd')
                                        html.write('                text-align: center;')
                                        html.write('                padding: 8px;')
                                        html.write('            tr:nth-child(even){')
                                        html.write('                background-color: #dddddd')
                                        html.write('              }')
                                        html.write('        </style>')
                                        html.write('    </head>')
                                        html.write('    <body>')
                                        html.write('        <header>')
                                        html.write('            <br></br>')
                                        html.write('            <br></br>')
                                        html.write('        </header>')
                                        html.write('        <aside>')
                                        html.write('            <br></br>')
                                        html.write('            <br></br>')
                                        html.write('        </aside>')
                                        html.write('        <center>')
                                        html.write('            <h1><b><u>'+cad+'</u></b></h1>')
                                        html.write('            <br></br>')
                                        html.write('            <table>')
                                        html.write('                <tr>')
                                        for a in self.claves:
                                            html.write('                    <th><span style="color: #009DFF">'+a+'</span></th>')
                                        html.write('                </tr>')
                                        html.write('                <tr>')
                                        html.write('                </tr>')
                                        lexemas = self.resultado[0]
                                        for b in self.registros:
                                            html.write('                <tr>')
                                            for c in b:
                                                html.write('                    <th>'+c+'</th>')
                                            html.write('                </tr>')
                                        html.write('            </table>')
                                        html.write('            <br></br>')
                                        html.write('        </center>')
                                        html.write('        <aside>')
                                        html.write('            <br></br>')
                                        html.write('            <br></br>')
                                        html.write('        </aside>')
                                        html.write('        <footer>')
                                        html.write('            <br></br>')
                                        html.write('            <br></br>')
                                        html.write('        </footer>')
                                        html.write('    </body>')
                                        html.write('</html>')
                                        html.close()
                                        webbrowser.open_new_tab('Reporte.html')
    
                                cadena = self.consola.toPlainText()
                                cadena = cadena + "\n" + resu
                                self.consola.setText(cadena)
                                
                            else:
                                self.eg.append([t[1], "Punto y Coma", t[2], t[3]]) 
                        else:
                            self.eg.append([t[1], "Parentsis Cierre", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Cadena", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Parentsis Abrir", t[2], t[3]])
            else:
                self.eg.append([t[1], "Palabra Reservada", t[2], t[3]])

    #---Analizador de Datos
    def datos(self):

            temp = self.t[-1]
            t = temp[0].lower()

            #---Analisis de Claves
            if t == 'claves':
                n1 = self.nuevo('Datos')
                t = self.t.pop()
                t = t[0].lower()
                if t == 'claves':
                    n2 = self.nuevo('Claves')
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Igual":
                        n2 = self.nuevo('=')
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Corchete Abrir":
                            n2 = self.nuevo('[')
                            self.add(n1, n2)
                            t = self.t.pop()
                            if t[1] == "Cadena":
                                n2 = self.nuevo("Claves")
                                self.add(n1, n2)
                                n3 = n2
                                n2 = self.nuevo(t[0])
                                self.add(n3, n2)
                                self.claves.append(t[0])
                                self.val()
                                if self.valban == 1:
                                    #Añadir Nodos del metodo val
                                    tam = len(self.valnodos) // 2
                                    if len(self.valnodos) != 0:
                                        for a in range(tam):
                                            n2 = self.nuevo("Clave")
                                            self.add(n3, n2)
                                            n3 = n2
                                            n2 = self.nuevo(self.valnodos[a])
                                            self.add(n3, n2)
                                            n2 = self.nuevo(self.valnodos[a+1])
                                            self.add(n3, n2)
                                        n2 = self.nuevo("Clave")
                                        self.add(n3, n2)
                                        vacio = self.nuevo("ε")
                                        self.add(n2, vacio)
                                                
                                    else:
                                        n2 = self.nuevo("Clave")
                                        self.add(n3, n2)
                                        vacio = self.nuevo("ε")
                                        self.add(n2, vacio)

                                    #Añadir Corchete
                                    n2 = self.nuevo("]")
                                    self.add(n1, n2)
                                    self.t.pop()
                                    self.add(self.n1, n1)
                                    
                                else:
                                    pass
                            else:
                                self.eg.append([t[1], "Cadena", t[2], t[3]])
                        else:
                            self.eg.append([t[1], "Corchete Abrir", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Igual", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Palabra Reservada - Claves", t[2], t[3]])

            #Analisis de Registros
            elif t == 'registros':
                n1 = self.nuevo('Registros')
                t = self.t.pop()
                t = t[0].lower()
                if t == 'registros':
                    n2 = self.nuevo('Registros')
                    self.add(n1, n2)
                    t = self.t.pop()
                    if t[1] == "Igual":
                        n2 = self.nuevo('=')
                        self.add(n1, n2)
                        t = self.t.pop()
                        if t[1] == "Corchete Abrir":
                            n2 = self.nuevo('[')
                            self.add(n1, n2)
                            self.regi()
                            if self.regban == 1:
                                
                                #Añadir Nodos del metodo reg
                                n2 = self.nuevo("Registros")
                                self.add(n1, n2)
                                n3 = n2
                                lt = self.regnodos[0]
                                lt.pop(0)
                                lt.pop(len(lt)-1)
                                n2 = self.nuevo("{")
                                self.add(n3, n2)
                                n2 = self.nuevo("Valores")
                                self.add(n3, n2)
                                n4 = n2
                                nt = self.nuevo("Tipo")
                                self.add(n4, nt)
                                n2 = self.nuevo(lt[0])
                                self.add(nt, n2)
                                
                                for x in range(len(lt)-1):
                                    n2 = self.nuevo("Valor")
                                    self.add(n4, n2)
                                    n4 = n2
                                    if lt[x+1] ==",":
                                        n2 = self.nuevo(lt[x+1])
                                        self.add(n4, n2)
                                    else:
                                        nt = self.nuevo("Tipo")
                                        self.add(n4, nt)
                                        n2 = self.nuevo(lt[x+1])
                                        self.add(nt, n2)
                                n2 = self.nuevo("Valor")
                                self.add(n4, n2)
                                n4 = n2
                                vacio = self.nuevo("ε")
                                self.add(n4, vacio)
                                n2 = self.nuevo("}")
                                self.add(n3, n2)
                                
                                for a in range(len(self.regnodos)-1):
                                    n2 = self.nuevo("Registros")
                                    self.add(n3, n2)
                                    n3 = n2
                                    lt = self.regnodos[a+1]
                                    lt.pop(0)
                                    lt.pop(len(lt)-1)
                                    n2 = self.nuevo("{")
                                    self.add(n3, n2)
                                    n2 = self.nuevo("Valores")
                                    self.add(n3, n2)
                                    n4 = n2
                                    nt = self.nuevo("Tipo")
                                    self.add(n4, nt)
                                    n2 = self.nuevo(lt[0])
                                    self.add(nt, n2)
                                    for x in range(len(lt)-1):
                                        n2 = self.nuevo("Valor")
                                        self.add(n4, n2)
                                        n4 = n2
                                        nt = self.nuevo("Tipo")
                                        self.add(n4, nt)
                                        n2 = self.nuevo(lt[x+1])
                                        self.add(nt, n2)
                                    n2 = self.nuevo("Valor")
                                    self.add(n4, n2)
                                    n4 = n2
                                    vacio = self.nuevo("ε")
                                    self.add(n4, vacio)
                                    n2 = self.nuevo("}")
                                    self.add(n3, n2)


                                n2 = self.nuevo("Registro")
                                self.add(n3, n2)
                                vacio = self.nuevo("ε")
                                self.add(n2, vacio)

                                #Añadir Corchete
                                n2 = self.nuevo("]")
                                self.add(n1, n2)
                                self.t.pop()
                                self.add(self.n1, n1)
                                
                                
                                    
                            else:
                                pass
                        else:
                            self.eg.append([t[1], "Corchete Abrir", t[2], t[3]])
                    else:
                        self.eg.append([t[1], "Igual", t[2], t[3]])
                else:
                    self.eg.append([t[1], "Palabra Reservada - Claves", t[2], t[3]])           
        
    #---Analizador de Valores
    def val(self):
        temp = self.t[-1]
        if temp[1] == "Corchete Cierre":
            self.valban = 1
        else:
            t = self.t.pop()
            if t[1] == "Coma":
                self.valnodos.append(t[0])
                t = self.t.pop()
                if t[1] == "Cadena":
                    self.valnodos.append(t[0])
                    self.claves.append(t[0])
                    self.val()
                else:
                    self.eg.append([t[1], "Cadena", t[2], t[3]])
                    self.valban = 0
                    self.claves = []
            else:
                self.eg.append([t[1], "Coma ó Corchete", t[2], t[3]])
                self.valban = 0
                self.claves = []

    #---Analizador de Registros
    def regi(self):
        self.regnodost = []
        self.temp = []
        temp = self.t[-1]
        if temp[1] == "Corchete Cierre":
            self.regban = 1
        else:
            t = self.t.pop()
            if t[1] == "Llave Abrir":
                self.regnodost.append(t[0])
                t = self.t.pop()
                if t[1] == "Cadena" or t[1] == "Numero":
                    self.regnodost.append(t[0])
                    self.temp.append(t[0])
                    self.valr()
                    if self.valrban == 1:
                        t = self.t.pop()
                        self.regnodost.append(t[0])
                        self.regnodos.append(self.regnodost)
                        self.registros.append(self.temp)
                        self.regi()
                    else:
                        self.regban = 0      
                else:
                    self.eg.append([t[1], "Cadena o Numero", t[2], t[3]])
                    self.regban = 0
            else:
                self.eg.append([t[1], "Corchete de Cierre o Llave de Apertura", t[2], t[3]])
                self.regban = 0
    
    #---Analizador de Valores para Registros
    def valr(self):
        temp = self.t[-1]
        if temp[1] == "Llave Cierre":
            self.valrban = 1
        else:
            t = self.t.pop()
            if t[1] == "Coma":
                self.regnodost.append(t[0])
                t = self.t.pop()
                if t[1] == "Cadena" or t[1] == "Numero":
                    self.regnodost.append(t[0])
                    self.temp.append(t[0])
                    self.valr()
                else:
                    self.eg.append([t[1], "Cadena o Numero", t[2], t[3]])
                    self.valrban = 0
            else:
                self.eg.append([t[1], "Coma ó Llave de Cierre", t[2], t[3]])
                self.valrban = 0
    
    
    #Metodos para manejar nodos
    #--- Crea un nuevo nodo
    def nuevo(self, nombre):
        no = str(uuid.uuid1())
        self.a.node(no,nombre)
        return no

    #---Añadir un nodo a otro. Padre e Hijo son los identificadores correspondientes a cada nodo.
    def add(self, padre,hijo):
        self.a.edge(padre, hijo)

    def isfloat(self, numero):
        try:
            float(numero)
            return True
        except ValueError:
            return False


app = QtWidgets.QApplication(sys.argv)
main = ventana()
sys.exit(app.exec_())

