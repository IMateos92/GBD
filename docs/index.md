# Gestión de Bases de Datos

En este repositorio vamos a agrupar los materiales y actividades realizadas en el módulo 0484 de ***Gestión de Bases de Datos*** del CFGS de *Administración de Sistemas Informáticos y Redes* (ASIR), cuyo curriculum viene fijado por el [Real Decreto 1629/2009](https://www.boe.es/eli/es/rd/2009/10/30/1629), impartido en el [IES Castelar](https://iescastelar.educarex.es/) de Badajoz.

La competencia que se trabaja en este curso es:

- d) Gestionar bases de datos, interpretando su diseño lógico y verificando integridad, consistencia, seguridad y accesibilidad de los datos.

Y el objetivo general correspondiente es:

- e) Interpretar el diseño lógico, verificando los parámetros establecidos para gestionar bases de datos.

Las líneas de actuación en el proceso de enseñanza-aprendizaje que permiten alcanzar los objetivos del módulo versarán sobre:

- La interpretación de diseños lógicos de bases de datos.
- La realización del diseño físico de una base de datos a partir de un diseño lógico.
- La implementación y normalización de bases de datos.
- La realización de operaciones de consulta y modificación sobre los datos almacenados.
- La programación de procedimientos almacenados.
- La utilización de bases de datos no relacionales.

## Resultados de Aprendizaje

Los diferentes resultados de aprendizaje (RA) trabajados junto con su peso aproximado, tal cual se indica en la programación didáctica, son:

| Código | Descripción | Peso (%) |
| --- | --- | --- |
| RA1 | Reconoce los elementos de las bases de datos analizando sus funciones y valorando la utilidad de los sistemas gestores. | 8 |
| RA2 | Crea bases de datos definiendo su estructura y las características de sus elementos según el modelo relacional. | 8 |
| RA3 | Consulta la información almacenada en una base de datos empleando asistentes, herramientas gráficas y el lenguaje de manipulación de datos. | 21 |
| RA4 | Modifica la información almacenada en la base de datos utilizando asistentes, herramientas gráficas y el lenguaje de manipulación de datos. | 8 |
| RA5 | Desarrolla procedimientos almacenados evaluando y utilizando las sentencias del lenguaje incorporado en el sistema gestor de bases de datos. | 18 |
| RA6 | Diseña modelos relacionales normalizados interpretando diagramas entidad/relación. | 24 |
| RA7 | Gestiona la información almacenada en bases de datos no relacionales, evaluando y utilizando las posibilidades que proporciona el sistema gestor. | 13 |

## Unidades de Trabajo

A partir de los RA, hemos definido 13 unidades de trabajo (UT).

El módulo de *Base de Datos* viene fijado con una carga lectiva de **160h**, repartidas en **5 sesiones semanales**, a lo largo de 32 semanas. Este curso se ha planificado sobre un total de 28 semanas, dejando las últimas 4 semanas para el desarrollo, por parte del alumnado, del programa formativo dual en la empresa. Estas 28 semanas hacen un total de 140h lectivas.

A continuación, en la siguiente tabla y a modo de mapa general, se muestran las diferentes UT y los RA que cubren, indicando la carga horaria empleada durante el presente curso en cada una de ellas:

| Unidades de Trabajo | RA1 | RA2 | RA3 | RA4 | RA5 | RA6 | RA7 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [1. Introducción a las bases de datos](01intro.md) | 9 |  |  |  |  |  |  |
| [2. Diseño conceptual. Modelo Entidad/Relación](02er.md) |  |  |  |  |  | 12 |  |
| [3. Diseño lógico: Modelo relacional](03mr.md) |  |  |  |  |  | 9 |  |
| [4. Diseño lógico: Transformación de modelos](04mr-eer.md) |  |  |  |  |  | 15 |  |
| [5. Modelo físico - SQL - DDL y DML](05ddl.md) |  | 7 |  | 6 |  |  |  |
| [6. SQL: Selección de datos](06sql.md) |  |  | 11 |  |  |  |  |
| [7. SQL: Agregaciones](07sql-group.md) |  | 2 | 8 |  |  |  |  |
| [8. SQL: Subconsultas. Optimización](08sql-subquerys.md) |  | 1 | 11 | 1 |  |  |  |
| [9. SQL: DCL y TCL](09dcl-tcl.md) |  | 2 |  | 5 |  |  |  |
| [10. Programación en bases de datos](10plsql.md) |  |  |  |  | 10 |  |  |
| [11. PL/SQL Avanzado](11triggers.md) |  |  |  |  | 14 |  |  |
| [12. Bases de datos NoSQL](12nosql.md) / [*Redis*](12redis.md) | 2 |  |  |  |  |  | 6 |
| [13. Bases de datos documentales. *MongoDB*](13mongodb.md) |  |  |  |  |  |  | 9 |
| **Total - 140h**   **Porcentaje** | 11 8% | 12 9% | 30 21% | 12 9% | 24 17% | 36 26% | 15 10% |

Si nos centramos en la temporalización, hemos agrupado las unidades en diferentes bloques repartidos a lo largo del curso del siguiente modo:

```
timeline
    title Planificación temporal
    section 1ª Evaluación
        Introducción : Presentación : 1.- Intro BD 
        Diseño : 2.- Modelo ER : 3.- Modelo relacional : 4.- Transformación
        SQL Definición: 5.- DDL + DML
    section 2ª Evaluación
        SQL Consulta : 6.- DQL : 7.- Agregaciones : 8.- Subconsultas
        SQL Control : 9.- DCL + TCL
    section 3ª Evaluación
        PL-SQL : 10.- Programación SQL : 11.- PLS/SQL Avanzado
        NoSQL : 12.- Redis : 13.- MongoDB
        Dual
```

## Evaluación

Para la evaluación del módulo de *Gestión de Bases de Datos* se ponderarán los resultados de aprendizaje respecto a los porcentajes indicados en el apartado anterior.

Para la evaluación de cada RA, emplearemos diferentes Instrumentos de Evaluación (IE), como pueden ser:

- **Actividades de enseñanza/aprendizaje**, normalmente realizadas en el aula, acompañadas de una rúbrica. Distinguiremos las **actividades de clase** ( AC), las cuales se calificarán normalmente sobre una escala de 3 puntos, de las **actividades de refuerzo** ( AR), también sobre 3 puntos para consolidar uno o varios CE no conseguidos, así como **actividades de profundización** ( AP) que aportarán puntos extra al RA.
- **Prácticas** ( PR) o **trabajo de investigación** ( TI), con una carga temporal variable, entre una semana o toda una unidad didáctica. Normalmente calificados sobre 10 puntos.
- **Proyectos** ( PY), bien de desarrollo individual o en parejas, sobre un determinado RA. Normalmente calificados sobre 30 puntos.
- **Pruebas objetivas** ( PO). En algunos RA, y no de forma generalizada, se realizará una prueba objetiva (ya sea escrita o en ordenador). Normalmente calificados sobre 30 puntos.

Para calcular la calificación de cada resultado de aprendizaje, se realizará la media ponderada simple de los diferentes instrumentos de evaluación empleados en dicho RA. Para comprobar que se han cubierto todos los criterios de evaluación, puedes consultar la página de [validación](validacion.md).

Todas las calificaciones, tanto de los instrumentos de evaluación como de los propios RA, se podrá consultar en todo momento en la plataforma *Aules* del curso.

## Materiales

A lo largo del curso, iremos trabajando diferentes materiales disponibles en este espacio web.

Cada una de las UT comenzará con un resumen de la **Propuesta Didáctica** que se plantea, los elementos que va a cubrir, tanto el RA a trabajar como sus criterios de evaluación (CE) asociados, así como un cuestionario inicial para reflexionar nuestro conocimiento previo.

En la parte final de cada sesión, además de diferentes recursos de **Referencia** para ampliar conocimientos, se plantean una serie de **Actividades** que iremos trabajando en su mayor medida en el aula. Cada una de las actividades indica el RA que cubre, los CE que trabaja así como su calificación, la cual luego se verá reflejada en la rúbrica de la entrega dicha tarea en Aules. Además, las actividades están codificadas con el prefijo del tipo de instrumento de evaluación, así como la unidad que cubren (por ejemplo, la actividad AC207, será la 7ª actividad de clase de la unidad 2).

Respecto a los recursos tecnológicos, aunque inicialmente trabajaremos mucho con papel y lápiz (para modelar es más rápido crear esbozos en papel), luego pasaremos a utilizar los SGBD de [MariaDB](https://mariadb.org/) y [PostgreSQL](https://www.postgresql.org/) indistintamente, tanto mediante contenedores [Docker](https://www.docker.com) como con soluciones *cloud* en [AWS](https://aws.amazon.com). En las últimas unidades, trabajaremos con [Redis](https://redis.io) y [MongoDB](https://www.mongodb.com/).
