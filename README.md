# GLang
### Compilador para la clase de Enero-Mayo 2019 "Diseño de Compiladores"
*Un lenguaje de programación y graficador al mismo tiempo*

hola, esta es una prueba que prometo borrar
Con GLang puedes crear las siguientes gráficas:
- (Graph) gráficas de funciones constantes, lineales, cuadráticas y cúbicas.
- (PieChart) gráficas de pastel.
- (BarChart) gráficas de barras.
- (HorBarChart) gráficas de barras horizontales
- (DonutGraph) gráficas de dona.
- (Network) grafos no dirigidos
- (Venn) diagramas de Venn.
- (Radar) gráficas de radar.
- Realizar operaciones relacionales, operacionales y de lógica
- Utilizar funciones (módulos)
- Declarar variables enteras, booleanas, caracteres y flotantes así como vectores y matrices
- Además puedes usar los estatutos de control de flujo if-else, while and for

## Requisitos del sistema para utilizar GLang
- Tener Python3 instalado
- Haber instalado previamente ply, matplotlib, matplotlibvenn , networkx

## Mi primera corrida
Primeramente, se deberá correr el siguiente comando para clonar el proyecto en tu equipo de cómputo
```
git clone https://github.com/luisapineda/GLang.git
```
Te dejamos este archivo *prueba.txt* de demo
```
program miPrimeraCorrida{
    vars {
        int i;
    }
    main {
        print("Hello World!");
        i = 1;
        while(i<=10){
            print("El valor de i es " & i);
            i = i + 1;
        }
    }
}
```
Para compilar algún archivo .txt (Tomaremos como ejemplo el archivo *prueba.txt*) en GLang realizamos el siguiente comando
*Se tiene que realizar encontrandose dentro del folder de GLang*
```
python3 ./prueba.txt
```
Al compilarlo, se generará el siguiente output
```
Running..
Hello World!
El valor de i es 1
El valor de i es 2
El valor de i es 3
El valor de i es 4
El valor de i es 5
El valor de i es 6
El valor de i es 7
El valor de i es 8
El valor de i es 9
El valor de i es 10
Execution completed in 4.884403944015503 seconds.
```
## ¿Cómo programar en GLang?
# Estructura básica de un programa
Esta es la estructura básica para un programa
```
program miPrimeraCorrida{
    vars {
        
    }
    
    main {
        
        }
    }
}
```

# Declarar variables
GLang cuenta con 4 tipos de variables
- Variables booleanas: **bool**
- Variables enteras: **int**
- Variables flotantes: **float**
- Caracteres: **char**
- Nuestras gráficas (Explicadas en la parte superior del documento)
Además, se pueden declarar vectores o matrices de nuestros tipos ingresando entre corchetes el límite superior del arreglo
Se declaran de la siguiente manera
```
bool flag, isSunny;
float c,x;
int i,cont,n,a[2][2],b[5];
```
En el código, el vector b irá de 1..5 y la matriz a cuenta con 2 renglones (de 1..2) y dos columnas (de 1..2)

Para asignar a una variable lo hacemos de la siguiente manera
```
i = 3;
a[1][2] = 10;

```
# Realizar operaciones
En GLang puedes realizar las siguientes operaciones
- Suma: **+**
- Resta: **-**
- Multiplicacion: *
- División: **/**
- Comparaciones: **>, <, >=, <=, ==, and, or, not**
Ejemplo
```
i = 4 * (5 - 1);
cont = 4.2 * i;
a[1][2] = 10;
n = 100
b[n] = 3;
isSunny = true;
flag = false;
if (flag == isSunny) {
  i = 111;
} else {
  i = 2222;
}
```
Es importante mencionar que al querer hacer una operación básica con la resta, tiene que existir un espacio entre el símbolo **-** y el número o variable que se quiera tener como segundo operando, de lo contrario, lo contará como un número negativo y no como resta. 

# Entrada y salida de valores
Para realizar una entrada de valores usamos la palabra reservada *input* y para salida de variables *print* como en el siguiente ejemplo.
```
print("Ingresa un numero");
input>>n;
print("Ingresaste "&n);
```
con **&**, realizamos una concatenación en el print de strings con expresiones aritméticas

# Estructuras de control
GLang cuenta con if, if-else, for y while y se emplean de la siguiente manera
```
if (3>4) {
  i=1;
} 

a=5;
while(a>i) {
  i = i + 1;
}

for (i=0; i<5 ; i=i+1;)
{
    print(i- 1);
}
```
# Módulos
GLang permite la declaracion de modulos con la palabra reservada *module*, declarandolo entre la sección de *vars* y de *main*. 
Los módulos pueden ser de tipo void o de alguno de los tipos primitivos de nuestro lenguaje. Se puede incluir de la siguiente manera
program x{

```
    vars {
        int i,j,n;
    }

    module void uno(int a, int b) {
        vars {
            int i,cont;
        }

        {
            cont=0;
            i=a*b; 
            i=0; 
            if(a>i) {
                print("Valor de A (>0): " & a);
                uno(a- 1,b);
            } else {
                print(a);
            }
        }

    }

    module int dos(int b) {
        {
            b=b*i+j;
            print("B es "&b);
            return b*2;
        }
    }

    main {
        i=2;
        j=i*2- 1;
        i=5;
        uno(j,i);
        n = dos(5);
        print(i);
        print(j);
        print(n);
    }

}
```
# Nuestras gráficas
Los tipos de nuestras gráficas son los siguientes
- **Graph**: gráficas de funciones constantes, lineales, cuadráticas y cúbicas
- **PieChart**: gráficas de pastel
- **BarChart**: gráficas de barras
- **HorBarChart**: gráficas de barras horizontales
- **DonutGraph**: gráficas de dona
- **Network**: grafos no dirigidos
- **Venn**: diagramas de Venn
- **Radar**: gráficas de radar
Se declaran en el mismo formato de una variable
```
vars{ 
Graph migrafica1; 
PieChart migrafica2;
BarChart migrafica3;
HorBarChart migrafica4;
DonutGraph migrafica5;
Network mired;
Venn mivenn;
RadarChart miradar;
int iNumero, i, a, iNumero2, b, iNumero3, iNumeroTemp;
bool c,d;
}
```
Se cuentan con cuatro distintas funciones especiales en nuestras gráficas
NOTA: Las funciones no son aplicables para todos los tipos de gráfica, solo para algunas
 - **NAME("nombreDeLaGrafica")**: Asignar un nombre a la gráfica
 - **NAMEX("nombreDelEjeX")**: Asignar un nombre al eje X
 - **NAMEY("nombreDelEjeY")**: Asignar un nombre al eje y
 - **COLOR(nombreDelColor)**: Dar un color a la gráfica
 
 Además, cada tipo de gráfica cuenta con su función especial create

| Tipo de Gráfica | Nombre de la función Create | Parámetros |
| :---         |     :---:      |          ---: |
| Graph   | CREATEG     | (int x3, int x2, int x1, int c)    |
| PieChart    | CREATEPC      | int v1,..int vn; String l1,ii String ln)    |
| BarChart   | CREATEGB     | int v1,..int vn; String l1,ii String ln)    |
| HorBarChart    | CREATEGBH      | int v1,..int vn; String l1,ii String ln)      |
| DonutGraph   | CREATED     | int v1,..int vn; String l1,ii String ln)    |
| Network     | CREATEN      | list vs1, list vs2     |
| Ven  | CREATEV     | int v1,..int vn; String l1,ii String ln)    |
| Radar     | CREATER      | int v1,..int vn; String l1,ii String ln)      |

Podemos observar un ejemplo en el siguiente fragmento de código
```
main{ 
    migrafica1.name("Crecimiento economico"); 
    migrafica1.nameX("Dias"); 
    migrafica1.nameY("Dinero"); 
    migrafica1.createG(0,1,3,4);

    migrafica2.name("Animales");
    migrafica2.createPC(20,21,22,23;"Perros", "Gatos", "Osos", "Murcielagos"); 

    migrafica3.name("Animales"); 
    migrafica3.nameY("Porcentaje de animales");
    migrafica3.createGB(20,21,22,23;"Perros", "Gatos", "Osos", "Murcielagos");

    migrafica4.name("Animales");
    migrafica4.nameX("Porcentaje de animales");
    migrafica4.color(red);
    migrafica4.createGBH(25,25,25,25;"Perros", "Gatos", "Osos", "Murcielagos");

    migrafica5.name("Calificaciones");
    migrafica5.createD(25,25,25,25;"Perros", "Gatos", "Osos", "Murcielagos");

    miradar.name("Animales");
    miradar.color(red);
    miradar.createR(25,25,25,25;"Perros", "Gatos", "Osos", "Murcielagos");

    mivenn.name("Reprobados");
    mivenn.createV( 10 , 5 , 20 ;"Matematicas","Quimica");

    mired.createN(["A", "B", "C","A"];["D", "A", "E","C"]);
}
```
No todas las gráficas pueden acceder a las 4 funciones especiales previamente explicadas, así que en la siguiente tabla podemos visualizar cuales aplican a cada uno de nuestros tipos

| Tipo de Gráfica | NAME | NAMEX | NAMEY | COLOR |
| --- | --- | --- | --- | --- |
| Graph   | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  |
| PieChart    | :heavy_check_mark:  | :x:  | :x:  | :heavy_check_mark:  |
| BarChart   | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  |
| HorBarChart    | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  | :heavy_check_mark:  |
| DonutGraph   | :heavy_check_mark:  | :x:  | :x:  | :heavy_check_mark:  |
| Network     | :x:  | :x:  | :x:  | :heavy_check_mark:  |
| Ven  |:heavy_check_mark: | :heavy_check_mark:  | :x:  | :x:  | :x:  |
| Radar     | :heavy_check_mark:  | :x:  | :x:  | :heavy_check_mark:  |
El default color si no se le asigna es *naranja*


## ¡Listo!
Estás listo para usar GLang, ¡Disfrútalo!
