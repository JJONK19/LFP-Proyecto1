'''
ANALIZADOR SINTACTICO
    REQUISITOS:
    - La gramatica del proyecto
    - El analizador lexico funcional
    - Conocimiento sobre pilas y sus metodos (especialmente pop)
    - Recursividad

    CONCEPTOS:
        * Terminal: Un terminal es cualquiera de los tokens generados por el analizador. Se les llama asi porque no pueden derivar
        en expresiones mas pequeñas. Se escriben en minuscula y son como las hojas en un arbol. 
        Ej: cadena, numero, signos (parentesis, llaves, dos puntos, etc).

        * No Terminal: Un No Terminal es un "token" compuesto formado por terminales o no terminales. Son una abstraccion de una 
        combinacion de terminales. Un ejemplo pueden ser las formulas matematicas. Podemos ver la formula del rectangulo (A = bh). Si
        suponemos un caso donde vamos b = 5 y h = 2, y queremos hacer una suma al area de ese rectangulo, se puede ver de dos formas:

        - Podemos expresar en terminos de sus variables (5 + (5*2)) o podemos expresarlo usando la forma abstacta (5 + A) 

        Los no terminales se escriben en mayusculas por convencion.
        Ej: EXPRESION, NOMBRE, etc.

        * Gramatica: Indica el orden en el que deben de venir los tokens. Se conforman de 2 lados: izquierdo y derecho. El izquierdo 
        contiene un No Terminal que general la expresion. El lado derecho contiene uno o mas Terminales o No Terminales que forman. 
        la equivalencia. Estas se separan por el simbolo :=
        Ej:

        EXPRESION := numero + numero
        NOMBRE := nombre apellido 

    DESCRIPCION:
    Lo primero que hace el programa es generar la lista de tokens. Para ello, se llama al analizador lexico mandando
    la cadena a revisar. Una vez tengamos los tokens, vamos a manejarlo como una pila global a la que se puede acceder
    desde cualquiera de los metodos.

    El siguiente paso es escribir un metodo por cada una de las producciones de la gramatica. Se valida por ifs que
    vayan viniendo los tokens que la gramatica indica, y se llama a otros metodos cuando en la gramatica vengan No Terminales.
    Se tienen que ir guardando cada uno de los tokens que vayamos a necesitar de la lectura, y estos se van a ejecutar cuando 
    se termine de leer la expresion.

    Para saber cuando se debe o no extraer un token (usar pop), debemos de ver nuestra gramatica. Si la gramatica puede tomar
    rumbos distintos en funcion de que venga, solo asignamos el valor a una variable y con un if decidimos hacia donde se va. 
    Si no se va a ningun lado o el token que estamos analizando es fijo siempre, sí usamos pop. 
    Ej:
    - START := { OPERACIONES , CONFIGURACIONES }
    En esta gramatica podemos usar pop al inicio cuando venga la llave porque sabemos que siempre esta ahi. 

    -S1 ::= DATOS | INSTRUCCION
    DATOS ::= Claves = [ CLAVES ] | Registros = [ REGISTROS ]
    En esta debemos tomar una decision, asi que solo leemos el siguiente token y comparamos con el token inicial de las dos 
    para ver a cual se va. Para este caso, si el siguiente token es la cadena "Claves" sabemos que se va a la produccion de DATOS.
    Lo de leer nada mas el token se hace porque al movernos de S1 a DATOS, el metodo tiene que hacer un pop para verificar que lo
    primero que venga sea "Claves", pero como hicimos un pop antes, entonces va a tirar error porque no la va a encontrar en nuestra
    pila.

    ENTRADAS:
    - Cadena: Cadena a analizar

    SALIDAS:
    - Un array Resultado:
        * En la posicion 0: Resultado (depende de lo que se vaya a retornar)
        * En la posicion 1: Lista de Errores
     
     NOTAS:
    - Un ejemplo de la gramatica se encuentra en la documentacion
    - Estructura del token: Pos 0 = Valor, Pos 1 = Tipo, Pos 2 = Fila, Pos 3 = Columna 
    - Se utilizan clause guards para hacer legible el codigo:  https://artansoft.com/2017/01/guard-clauses-definicion-beneficios/
    - Recordar que en el lexico se quitaron las comillas a las cadenas. Solo se debe validar que venga la palabra:
        * "operaciones" : Solo se valida que la cadena sea operaciones, no "operaciones"

'''
from Lexico import automata

#-- Declaracion de variables globales
tokens = []                 #Almacena los tokens del analizador lexico
errores = []                 #Almacena los errores del analizador sintactico

def parser (cadena):
    #Definifimos que tokens se refiere a la global para modificarla
    global tokens
    
    #Genera los tokens
    respuesta = automata(cadena)
    tokens = respuesta[0]               #Recordemos que la lista de tokens esta en la pos 0 de la respuesta del automata

    #Invertir los tokens para manejarlo como una pila
    #Recordar que ahora leemos el vector del final hacia el inicio.
    tokens.reverse()

    #Llamamos a la derivacion inicial de la gramatica
    start()

#----- No terminal START ===================================================================================================
def start():
    '''
        START := { OPERACIONES , CONFIGURACIONES } 
    '''
    try:
        #Extraemos un token. Deberia de venir una llave {. Error si no.
        temp = tokens.pop()                     
        if temp[1] != "Llave Abrir":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Llamamos al No Terminal OPERACiONES
        operaciones()

        #Extraemos un token. Deberia de venir una coma. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Coma":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Llamamos al No Terminal CONFIGURACIONES
        configuraciones()

        #Extraemos un token. Deberia de venir una llave }. Error si no.
        temp = tokens.pop()                    
        if temp[1] != "Llave Cierre":         
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        # ACA ACABA EL ANALISIS
        print("Analisis Finalizado")
        
    except Exception as e:
        print("Error: " + str(e))

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



                                                    #OPERACIONES



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#----- No terminal OPERACIONES ===================================================================================================
def operaciones():
    '''
       OPERACIONES := “ operaciones “ : [ OPERACIÓN ]
       
    '''
    try:
        #Extraemos un token. Deberia de venir operaciones. Usamos temp[0] para acceder al valor del token. 
        temp = tokens.pop()                     
        if temp[0] != "operaciones":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir dos puntos. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Dos Puntos":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir un corchete [. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Corchete Abrir":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Llamamos al No Terminal OPERACION
        operacion()

        #Extraemos un token. Deberia de venir una coma. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Corchete Cierre":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
    except Exception as e:
        print("Error: " + str(e))

#----- No terminal OPERACION ===================================================================================================
def operacion():
    '''
       OPERACIÓN := EXPRESION
                    | EXPRESION, OPERACIÓN
    '''
    try:
        #Llamamos al No Terminal EXRPESION
        expresion()

        #Leemos el siguiente token. Si viene una coma, sabemos que se va por la produccion EXPRESION, OPERACIÓN
        #Si no viene coma, entonces ahi acaba. Usamos -1 para obtener el ultimo valor del vector de tokens.
        temp = tokens[-1]
        if temp[1] != "Coma":
            return
        
        #Sacamos la coma que revisamos antes de la pila ahora que estamos seguros que nos vamos a la segunda produccion
        tokens.pop()        

        #Llamamos al No Terminal OPERACION
        operacion()

    except Exception as e:
        print("Error: " + str(e))

#----- No terminal EXPRESION ===================================================================================================
def expresion():
    '''
       EXPRESION := { “operación” : “ operador”, LISTAVALORES }
    '''
    #Declaracion de variables para la ejecucion
    operador = ""                               #Almacena si es una suma, resta, multiplicavion, etc.
    valores = []                                #Almacena los valores que se van a manejar. Son numeros.
    resultado = 0                               #ALmacena el resultado de la expresion

    try:
        #Extraemos un token. Deberia de venir una llave {. Error si no.
        temp = tokens.pop()                     
        if temp[1] != "Llave Abrir":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 0
        
        #Extraemos un token. Deberia de venir operacion. Usamos temp[0] para acceder al valor del token. 
        temp = tokens.pop()                     
        if temp[0] != "operacion":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 0
        
        #Extraemos un token. Deberia de venir dos puntos. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Dos Puntos":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir una reservada de tipo "Operador". Error si no.
        #Guardamos ese operador en la avriable operador.
        temp = tokens.pop()                     
        operador = temp[0]
        if temp[1] != "Operador":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 0
        
        #Extraemos un token. Deberia de venir una coma. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Coma":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 0
        
        #Llamamos al metodo LISTAVALORES. Le mandamos el array valores para que almacene ahi nuestros numeros.
        listavalores(valores)

        #Extraemos un token. Deberia de venir una llave }. Error si no.
        temp = tokens.pop()                    
        if temp[1] != "Llave Cierre":         
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 0

        #Verificar que valores no venga vacio. Retornamos 0 para evitar errores.
        if len(valores) == 0:
            print("Error: No se añadieron valores a la operacion.")
            return 0

        #Operamos la lista de valores segun el operador. Si surge un error, retornamos 0 siempre.
        #De no ser asi, retornamos el resultado. Aun si no se usa en operacion() debemos de mandarlo ya 
        #que expresion se puede manejar de manera recursiva.
        #TODO: Añadir el resto de operaciones.
        if operador == "suma":
            for numero in valores:
                resultado += numero

        elif operador == "resta":
            resultado = valores[0]
            for numero in valores[1:]:
                resultado -= numero
        
        elif operador == "multiplicacion":
            resultado = valores[0]
            for numero in valores[1:]:
                resultado *= numero
        
        elif operador == "division":
            try:
                if len(valores) > 2:
                    print("Error: La division solo admite dos valores.")
                else:
                    resultado = valores[0] / valores[1]
            except:
                resultado = 0
        
        #Regresamos el resultado de la expresion
        print("El resultado de la operacion ", operador, " es: ", resultado)
        return resultado
            
    except Exception as e:
        print("Error: " + str(e))
        return 0

#----- No terminal LISTAVALORES ===================================================================================================
def listavalores(valores):
    '''
       LISTAVALORES := VALOR
                    | VALOR, LISTAVALORES
    '''
    try:
        #Llamamos al No Terminal VALOR
        #VALOR va a regresar el numero que venga en la seccion "valor1" : #NUMERO
        numero = valor()
        valores.append(numero)

        #Leemos el siguiente token. Si viene una coma, sabemos que se va por la produccion VALOR, LISTAVALORES
        #Si no viene coma, entonces ahi acaba. Usamos -1 para obtener el ultimo valor del vector de tokens.
        temp = tokens[-1]
        if temp[1] != "Coma":
            return
        
        #Sacamos la coma que revisamos antes de la pila ahora que estamos seguros que nos vamos a la segunda produccion
        tokens.pop()        

        #Llamamos al No Terminal OPERACION
        listavalores(valores)

    except Exception as e:
        print("Error: " + str(e))

#----- No terminal VALOR ===================================================================================================
def valor():
    '''
        VALOR := “valor“ : NUMERO
    '''
    try:
        #Extraemos un token. Deberia de venir una reservada de tipo "Valor". Error si no.
        #Quemamos estos tokens en el lexico para no preocuparnos por reconocer valor + un numero: "valor88"
        temp = tokens.pop()                    
        if temp[1] != "Valor":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return float(0)
        
        #Extraemos un token. Deberia de venir dos puntos. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Dos Puntos":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return float(0)
        
        #Llamamos al No Terminal NUMERO
        resultado = numero()
        return resultado

    except Exception as e:
        print("Error: " + str(e))
        return float(0)

#----- No terminal VALOR ===================================================================================================
def numero():
    '''
        NUMERO := numero
                | [ EXPRESION ]
    '''
    # --- Declaracion de variables
    resultado = 0                  #Variable que contiene al numero del token 
    try:
        #Leemos el siguiente token. Si viene un numero, lo pasamos de string a numero y lo asignamos en resultado
        #Si no, tenemos que revisar si es u corchete [ para mandar a llamar a expresion().
        temp = tokens[-1]
        if temp[1] == "Numero":
            try:
                tokens.pop()            #Sacamos el numero de la pila
                resultado = float(temp[0])
            
            except:
                resultado = float(0)
        
        else:
            #Extraemos un token. Deberia de venir un corchete [. Error si no.
            temp = tokens.pop()                   
            if temp[1] != "Corchete Abrir":           
                errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
                return 
            
            #Llamamos al no terminal EXPRESION y le asignamos el resultado
            resultado = float(expresion())

            #Extraemos un token. Deberia de venir una coma. Error si no.
            temp = tokens.pop()                   
            if temp[1] != "Corchete Cierre":           
                errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
                return 
        
        return resultado

    except Exception as e:
        print("Error: " + str(e))
        return 0

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++



                                                    #CONFIGURACIONES



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#----- No terminal CONFIGURACIONES  ===================================================================================================
def configuraciones():
    '''
       CONFIGURACIONES := “ configuraciones “ : [ { AJUSTES } ]
       
    '''
    try:
        #Extraemos un token. Deberia de venir operaciones. Usamos temp[0] para acceder al valor del token. 
        temp = tokens.pop()                     
        if temp[0] != "configuraciones":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir dos puntos. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Dos Puntos":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir un corchete [. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Corchete Abrir":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir una llave {. Error si no.
        temp = tokens.pop()                     
        if temp[1] != "Llave Abrir":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 0
        
        #Llamamos al No Terminal AJUSTES
        ajustes() 

        #Extraemos un token. Deberia de venir una llave }. Error si no.
        temp = tokens.pop()                    
        if temp[1] != "Llave Cierre":         
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 0

        #Extraemos un token. Deberia de venir una coma. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Corchete Cierre":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
    except Exception as e:
        print("Error: " + str(e))

#----- No terminal AJUSTES  ===================================================================================================
def ajustes():
    '''
       AJUSTES :=  “ajuste“ =  “cadena“
                | “ajuste“ =  “cadena“ , AJUSTES

       
    '''
    #TODO: Añadir el codigo de las configuraciones (Depende de como manejen graphviz)
    try:
        #Extraemos un token. Deberia de venir un token de tipo reservada. Es el nombre del ajuste (texto, fondo, etc) 
        temp = tokens.pop()                     
        if temp[1] != "Reservada":            
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir dos puntos. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Dos Puntos":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Extraemos un token. Deberia de venir una cadena. Error si no.
        temp = tokens.pop()                   
        if temp[1] != "Cadena":           
            errores.append([temp[0], "Se esperaba " + temp[1], temp[2], temp[4]])
            return 
        
        #Leemos el siguiente token. Si viene una coma, sabemos que se va por la produccion “ajuste“ =  “cadena“ , AJUSTES
        #Si no viene coma, entonces ahi acaba. Usamos -1 para obtener el ultimo valor del vector de tokens.
        temp = tokens[-1]
        if temp[1] != "Coma":
            return
        
        #Sacamos la coma que revisamos antes de la pila ahora que estamos seguros que nos vamos a la segunda produccion
        tokens.pop()        

        #Llamamos al No Terminal OPERACION
        ajustes()

    except Exception as e:
        print("Error: " + str(e))


#========================================================================================================================
#FIN DEL ANALZADOR


#Prueba
def main():
    entrada = '''
                {
                    "operaciones": [
                                        {
                                            "operacion":"suma",
                                            "valor1": 10,
                                            "valor2": [
                                                {
                                                    "operacion":"suma",
                                                    "valor1": 5,
                                                    "valor2": 5
                                                }
                                            ]
                                        }, 
                                        {
                                            "operacion":"resta",
                                            "valor1": 10,
                                            "valor2": 5
                                        }
                                    ], "configuraciones": [
                                            {
                                                "texto": "Operaciones",
                                                "fondo": "azul"
                                            }
                                    ]
                }'''
    parser(entrada)
    print(errores)

if __name__ == "__main__":
    main()
