'''
    ANALIZADOR LEXICO
    REQUISITOS:
    - Necesitamos tener el AFD ya generado con el método del arbol

    CONCEPTOS:
        * token: Coincidencia que encuentra nuestro analizador de acuerdo las reglas lexicas de nuestro AFD. Almacena la coincidencia, 
        el tipo de token, la fila y la columna. Estructura de ejemplo: [coincidencia, tipo, fila, columna]
        Ej:

        Regla: String = "[A-z][0-9]" - Reconoce cualquier combinacion de letras y numeros encerrados en comillas
        Token Ejemplo: ["hola mundo", "String", 55, 66]

        Regla: Reservada = "[A-z][0-9]" - Reconoce cualquier combinacion de letras y numeros encerrados en comillas. Comparte
        la definicion de un string pero internamente sabemos que esta en un array de palabras reservadas (explicacion detallada
        mas adelante)
        Token Ejemplo: ["suma", "Reservada", 77, 2]

        * buffer: Variable que almacena los caracteres que se van reconociendo. Al usar un string, por ejemplo, la computadora
        va almacenando las letras hasta que encuentre el fin del cadena. Para nuestro caso, al reconocer "hola", va guardando
        todas las letras desde que encuentra la primera comilla y deja de guardar hasta que encuentre otra (el fin de cadena
        aca es esa otra comilla).


    DESCRIPCION:
    Recibe una cadena de texto y va leyendo caracter por caracter hasta generar los tokens o coincidencias que vengan en nuestro lenguaje
    de entrada (cadenas, numeros, decimales, etc.). El analizador consiste en un ciclo que recorre caracter por caracter hasta terminar
    de la cadena. 
    
    Dentro hay una especie de switch(o if-else anidados por que no existe en python) donde se ejecuta el movimiento entre estados
    de acuerdo al caracater que venga. Para eso esta la variable "estado", que cambia de acuerdo al estado del AFD en el que estemos.
    Por ejemplo, si en nuestro AFD pasamos del estado 0 (e = 0) al estado 1 (e = 1) cuando venga un numero. 

    Cuando se llega al estado de aceptacion, se crea un token, el cual es un array con la informacion relevante de esa palabra. Por 
    ejemplo, si concuerda una palabra reservada, el token almacena que se trata de una palabra reservada, almacenana la palabra
    como tal asi como la fila y la columna. Eso lo guarda en el array de tokens. Si el usuario lo prefiere, puede cambiar este enfoque
    usando clases, diccionarios o cualquier otra forma con la que se sienta comodo. Lo importante es almacenar esta informacion ya que
    nos servira cuando analicemos que las palabras vengan en el orden correcto (sintaxis).

    Para los errores, el comportamiento es similar. Al igual que los tokens, se crea un vector que almacena: el caracter inesperado, 
    la fila y la columna. Esto se almacena en la lista de errores. Recordemos que un error lexico es aquel caracter que en nuestro
    AFD no tenemos definido. Por ejemplo, si en un estado tenemos una transicion que va de E0 a E1 con un ";" y vemos que viene una letra,
    se considera esa letra como un error.

    El metodo tambien tiene algo conocido como recuperacion de errores: Para evitar que nuestro programa falle, cada que encuentra un 
    error, este va a regresar de nuevo al estado 0 (el inicial) y desde ahi va a continuar con el analisis. Si siguen encontrandose 
    errores, va a omitir y añadirños a la lista hasta que encuentre una combinacion valida.

    Como nota final, la funcion maneja un sistema de posiciones para filas y columnas. De esa forma, podemos localizar
    errores en nuestro archivo de entrada y verificar en que linea (y posicion en la misma) se encuentra el error.

    ENTRADAS:
    - Cadena: Cadena a analizar

    SALIDAS:
    - Un array Resultado:
        * En la posicion 0: Lista de Tokens
        * En la posicion 1: Lista de Errores

'''
def automata (cadena):
    #----- Declaracion de Variables
    tokens = []             #Almacena los tokens encontrados en el analisis
    errores = []            #Almacena los errores lexicos
    fila = 1                #Indica en que fila del archivo estamos
    columna = 1             #Indica en que posicion de la fila estamos
    i = 0                   #Se usa en el while que recorre la cadena
    temp = ""               #Variable temporal usada para guardar los caracteres de un string o un número 
    estado = 0              #Numero de estado que se esta ejecutando actualmente

    #----- Lista con las palabras reservadas validas en el lenguaje
    '''
    MANEJO DE RESERVADAS:
    Como nuestro lenguaje maneja distintos tipos de palabras reservadas, podemos crear diferentes listas para las 
    reservadas y añadir al tipo de token que son de un tipo especifico para facilitar el analisis de sintaxis. Por ejemplo,
    podemos crear un token con un tipo Operacion cuando se reconozca "suma", "resta" o "potencia". Asi cuando analicemos 
    la sintaxis de esta linea:
                                        "operacion": "suma",

    validamos que "suma" es una palabra que se puede esperar. Si viniera esto:

                                        "operacion": "XD",

    sabriamos que es un error porque "XD" no es un token de tipo Operacion (sabemos que operacion solo puede ser "suma", "resta"
    o "potencia"). 

    Ej:
    operaciones = ["suma", "resta", "potencia"]
    configuraciones = ["texto", "fondo", "fuente", "forma"]

    Cualquier palabra que no se encuentre en esas listas, es un simple string.

    NOTA:
    - Preguntarle a su auxiliar la lista de fondos, fuentes y formas disponibles para tenerlo en cuenta en sus reservadas.

    '''
    reservadas = ["operaciones", "operacion", "configuraciones", "texto", "fondo", "fuente",
                  "forma"]
    
    operador = ["suma", "resta", "multiplicacion", "division", "potencia", "raiz", "inverso", "seno", "coseno",
                  "tangente", "mod"]
    
    valor = ["valor1", "valor2", "valor3", "valor4", "valor5", "valor6", "valor7", "valor8", "valor9", "valor10",
             "valor11", "valor12", "valor13", "valor14", "valor15", "valor16", "valor17", "valor18", "valor19", "valor20"]
    


    #----- Automata
    # Recorre caracter por caracter usando el indice como si fuese un array. Pueden cambiarlo usando "for caracter in cadena"
    # sustituyendo "cadena[i]" por "caracter".
    while i < len(cadena):

        #Estado 0
        '''
            NOTA: Para ahorrar codigo, podemos ver en el AFD que si viene corchetes, coma, llaves o dos puntos nos vamos a S1
            que es el estado de aceptacion. Podemos aceptar la cadena de una vez y crear el token en lugar de: 1. Guardar en 
            temp (el buffer) el caracter, 2. Movernos de S0 a S3 (acepatcion), 3. Crear el token, reiniciar temp y regresar a S0.
        '''
        #========================================================================================================================
        if estado == 0:
            if cadena[i] == ",":
                tokens.append([cadena[i], "Coma", fila, columna])
                temp = ""
                columna += 1

            elif cadena[i] == "{":
                tokens.append([cadena[i], "Llave Abrir", fila, columna])
                temp = ""
                columna += 1

            elif cadena[i] == "}":
                tokens.append([cadena[i], "Llave Cierre", fila, columna])
                temp = ""
                columna += 1

            elif cadena[i] == "[":
                tokens.append([cadena[i], "Corchete Abrir", fila, columna])
                temp = ""
                columna += 1

            elif cadena[i] == "]":
                tokens.append([cadena[i], "Corchete Cierre", fila, columna])
                temp = ""
                columna += 1

            elif cadena[i] == ":":
                tokens.append([cadena[i], "Dos Puntos", fila, columna])
                temp = ""
                columna += 1

            #Si vienen comillas nos movemos a S2 segun el AFD
            #Las cadenas se guardan sin comillas por facilidad, por eso no las concatenamos a temp.
            elif cadena[i] == '"':
                estado = 2
                columna += 1

            #Si vienen un caracter que sea un digito, nos movemos a S1 segun el AFD
            #Añadimos el digito al buffer para no perderlo.
            elif cadena[i].isdigit():
                temp += cadena[i]
                estado = 1
                columna += 1

            #Los siguientes caracteres no estan, pero es para manejar saltos de linea y espacios que vengan en el archivo de entrada
            elif cadena[i] == "\r":
                pass

            elif cadena[i] == "\n":
                columna = 1
                fila += 1
        
            elif cadena[i] == " ":
                columna += 1

            elif cadena[i] == "\t":
                columna += 1
        
            else:
                errores.append([cadena[i], fila, columna])
                temp = ""
                columna += 1
#========================================================================================================================
#Manejo de numeros y decimales. El estado 4 y 5 no estan en el AFD pero son un ejemplo para manejar decimales.
        #Estado 1 - Numeros enteros
        elif estado == 1:
            if cadena[i].isdigit():
                temp += cadena[i]   #Añade los numeros que se vayan encontrando
                columna += 1

            elif cadena[i] == ".":
                temp += cadena[i]   #Añade el punto al buffer. Implementacion de decimales.
                estado = 4
                columna += 1

            else:
                tokens.append([temp, "Numero", fila, columna])
                temp = ""       #Vaciar el buffer
                columna += 1
                i -= 1          #Retroceso en el caracter analizado
                estado = 0

        #Estado 4 - Punto Decimal - Esta de paso para verificar que despues del punto vengan numeros
        elif estado == 4:
            if cadena[i].isdigit():
                temp += cadena[i]
                estado = 5
                columna += 1
            
            else:
                errores.append([temp, fila, columna])
                temp = ""
                columna += 1
                estado = 0

        #Estado 5 - Numeros despues del punto
        elif estado == 5:
            if cadena[i].isdigit():
                temp += cadena[i]
                columna += 1
        
            else:
                tokens.append([temp, "Numero", fila, columna])
                temp = ""
                columna += 1
                i -= 1
                estado = 0

#========================================================================================================================
#Manejo de cadenas y palabras reservadas.

        #Estado 2
        elif estado == 2:
            if cadena[i] == '/' or cadena[i] == '\\' :
                columna += 1
                
            elif cadena[i] == '"':
                #Ya que las cadenas y reservadas se parecen, debemos revisar si una cadena no es reservada. Solo hay que ver
                #si la palabra no esta en nuestra/s lista/s de reservadas
                #Nota: Hay que tener cuidado con mayusculas y minusculas en el enunciado. En algunos casos, se tiene que 
                #reconocer "suma", "SUMA" ó "Suma" como la misma reservada. Para este caso, vamos a asumir que todo viene en
                #minusculas y que no hay errores de ese tipo.
                if temp in reservadas:
                    tokens.append([temp, "Reservada", fila, columna])
                elif temp in operador:
                    tokens.append([temp, "Operador", fila, columna])
                elif temp in valor:
                    tokens.append([temp, "Valor", fila, columna])
                else:
                    tokens.append([temp, "Cadena", fila, columna])
                temp = ""
                columna += 1
                estado = 0

            elif cadena[i] == "\n": 
                errores.append([temp, fila, columna]) #Es error porque una cadena no puede iniciar en una linea y terminar en otra
                temp = ""
                columna = 1
                fila += 1
                estado = 0

            else:
                temp += cadena[i]   #Si viene cualquier otra cosa que no sean comillas, lo añade al buffer (temp)
                columna += 1        

        #Aumentar iteración por ser un while. Si no, no se va a mover al siguiente caracter
        i += 1

#========================================================================================================================
#FIN DEL ANALZADOR

    #Regresar informacion 
    resultado = [tokens, errores]
    return resultado

'''
#Prueba
def main():
    entrada = ' ''
                {
                    "operaciones": [
                                        {
                                            "operacion":"suma",
                                            "valor1": 4.5,
                                            "valor2":5.32
                                        }
                                    ], @
                    "configuraciones": [
                                            {
                                                "texto": "Operaciones",
                                                "fondo": "azul"
                                            }
                                        ]
                }' ''
    salida = automata(entrada)
    print("TOKENS")
    for token in salida[0]:
        print(token)
    
    print("ERRORES")
    for errores in salida[1]:
        print(errores)

if __name__ == "__main__":
    main()

'''
