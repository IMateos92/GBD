[RA3](../tags.md#tag:ra3)
[SQL](../tags.md#tag:sql)

# Consultas jerárquicas

## Consultas jerárquicas

Las consultas jerárquicas permiten trabajar con datos que tienen una estructura de árbol o relaciones padre-hijo dentro de una misma tabla. En nuestro caso, la tabla `departamento` presenta una estructura jerárquica donde un departamento puede depender de otro a través de la columna `CodDepDep` que hace referencia a `CodDep`.

Por ejemplo, para recuperar los departamentos que están en la parte más alta del árbol, podríamos obtenerlos a partir de aquellos donde la clave ajena reflexiva está vacía:

```
select d1.CodDep as depNivel1, d1.NomDep as nomNivel1
from departamento d1
where d1.CodDepDep is null;
-- +-----------+----------------------------+
-- | depNivel1 | nomNivel1                  |
-- +-----------+----------------------------+
-- | ADMZS     | Administración Zona Sur    |
-- | DIRGE     | Dirección General          |
-- | JEFZS     | Jefatura Fábrica Zona Sur  |
-- +-----------+----------------------------+
-- 3 rows in set (0.006 sec)
```

Si, en cambio, queremos además recuperar tanto los del primer nivel como sus descendientes directos, necesitamos hacer un *join* con otra instancia de la tabla, de manera que nombramos `d1` a los departamentos del primer nivel y `d2` a los del segundo:

```
select 
    d1.CodDep as depNivel1, d1.NomDep as nomNivel1,
    d2.CodDep as depNivel2, d2.NomDep as nomNivel2
from departamento d1
    left join departamento d2 on d2.CodDepDep = d1.CodDep
where d1.CodDepDep is null;
-- +-----------+----------------------------+-----------+--------------------------+
-- | depNivel1 | nomNivel1                  | depNivel2 | nomNivel2                |
-- +-----------+----------------------------+-----------+--------------------------+
-- | ADMZS     | Administración Zona Sur    | VENZS     | Ventas Zona Sur          |
-- | DIRGE     | Dirección General          | IN&DI     | Investigación y Diseño   |
-- | JEFZS     | Jefatura Fábrica Zona Sur  | PROZS     | Producción Zona Sur      |
-- +-----------+----------------------------+-----------+--------------------------+
-- 3 rows in set (0.001 sec)
```

De forma similar, para recuperar los departamentos "hoja", los que no tienen dependientes, y por lo tanto, aquellos departamentos que no tienen otros departamentos dependiendo de ellos, volvemos a realizar el *join* pero este caso un *antijoin*:

```
select d1.CodDep as CodDepHoja, d1.NomDep as NomDepHoja
from departamento d1
    left join departamento d2 on d1.CodDep = d2.CodDepDep
where d2.CodDep is null;
-- +------------+--------------------------+
-- | CodDepHoja | NomDepHoja               |
-- +------------+--------------------------+
-- | IN&DI      | Investigación y Diseño   |
-- | PROZS      | Producción Zona Sur      |
-- | VENZS      | Ventas Zona Sur          |
-- +------------+--------------------------+
-- 3 rows in set (0.000 sec)
```

Si en vez de dos niveles, necesitamos añadir el tercer nivel, tenemos que unir con una tercera instancia de la tabla:

```
select 
    d1.CodDep as depNivel1, d1.NomDep as nomNivel1,
    d2.CodDep as depNivel2, d2.NomDep as nomNivel2,
    d3.CodDep as depNivel3, d3.NomDep as nomNivel3
from departamento d1
    left join departamento d2 on d2.CodDepDep = d1.CodDep
    left join departamento d3 on d3.CodDepDep = d2.CodDep
where d1.CodDepDep is null;
-- +-----------+----------------------------+-----------+--------------------------+-----------+-----------+
-- | depNivel1 | nomNivel1                  | depNivel2 | nomNivel2                | depNivel3 | nomNivel3 |
-- +-----------+----------------------------+-----------+--------------------------+-----------+-----------+
-- | ADMZS     | Administración Zona Sur    | VENZS     | Ventas Zona Sur          | NULL      | NULL      |
-- | DIRGE     | Dirección General          | IN&DI     | Investigación y Diseño   | NULL      | NULL      |
-- | JEFZS     | Jefatura Fábrica Zona Sur  | PROZS     | Producción Zona Sur      | NULL      | NULL      |
-- +-----------+----------------------------+-----------+--------------------------+-----------+-----------+
-- 3 rows in set (0.001 sec)
```

Con los datos que tenemos cargados, como no tenemos departamentos de nivel 3, tenemos los datos en blanco.

Preparando nuevos datos

En la base de datos `empresa-plus`, que puedes crear a partir del script [06bd-empresa-plus.sql](../resources/06bd-empresa-plus.sql), hemos insertado nuevos departamentos para estudiar toda la casuística de las relaciones jerárquicas.

```
INSERT INTO departamento (CodDep, CodEmpDir, CodDepDep, CodCen, NomDep, PreAnu, TiDir) VALUES
-- Nivel 2: Dependientes de Dirección General
('FINZS', 10, 'DIRGE', 'DIGE', 'Finanzas Corporativas', 18500000, 'P'),
('RHZZS', 11, 'DIRGE', 'DIGE', 'Recursos Humanos', 9500000, 'P'),
('MKYCO', 12, 'DIRGE', 'DIGE', 'Marketing Corporativo', 15200000, 'F'),

-- Nivel 3: Dependientes de Investigación y Diseño
('INVSW', 13, 'IN&DI', 'DIGE', 'Investigación Software', 12800000, 'P'),
('INVHW', 14, 'IN&DI', 'DIGE', 'Investigación Hardware', 14300000, 'F'),
('DISPR', 15, 'IN&DI', 'DIGE', 'Diseño de Producto', 10900000, 'P'),

-- Nivel 4: Dependientes de departamentos de nivel 2
('SWMOV', 16, 'INVSW', 'DIGE', 'Software Móvil', 7600000, 'P'),
('SWWEB', 17, 'INVSW', 'DIGE', 'Software Web', 6200000, 'F'),
('HWSEN', 18, 'INVHW', 'DIGE', 'Hardware Sensores', 8300000, 'P'),
('DISER', 19, 'DISPR', 'DIGE', 'Diseño de Servicios', 5400000, 'F'),

-- Nivel 5: Dependientes de departamentos de nivel 3
('MOVUI', 20, 'SWMOV', 'DIGE', 'UI Móvil', 3800000, 'P'),
('MOVBA', 21, 'SWMOV', 'DIGE', 'Backend Móvil', 4200000, 'F'),
('WEBUI', 22, 'SWWEB', 'DIGE', 'UI Web', 3100000, 'P'),
('SENIO', 23, 'HWSEN', 'DIGE', 'Sensores IoT', 4700000, 'F'),

-- Nivel 6: Dependientes de departamentos de nivel 4
('UIDSG', 24, 'MOVUI', 'DIGE', 'Diseño UI', 1900000, 'P'),
('UIFNC', 25, 'MOVUI', 'DIGE', 'Funcionalidad UI', 2100000, 'F'),

-- Estructura paralela: Dependientes de Producción Zona Sur
('MANUF', 26, 'PROZS', 'FAZS', 'Manufactura', 65000000, 'P'),
('CALDE', 27, 'PROZS', 'FAZS', 'Control de Calidad', 15800000, 'F'),
('LOGUN', 28, 'PROZS', 'FAZS', 'Logística Unitaria', 27200000, 'P'),

-- Nivel adicional bajo Manufactura
('ASMZS', 29, 'MANUF', 'FAZS', 'Ensamblaje', 42000000, 'P'),
('COMPZ', 30, 'MANUF', 'FAZS', 'Componentes', 23000000, 'F'),

-- Nivel adicional bajo Ensamblaje
('ELELC', 31, 'ASMZS', 'FAZS', 'Ensamblaje Electrónico', 28000000, 'P'),
('MECAS', 32, 'ASMZS', 'FAZS', 'Ensamblaje Mecánico', 14000000, 'F');
```

Así pues, ahora disponemos de una jerarquía principal que suma 5 niveles de profundidad bajo la `Dirección General` y otra bajo `Producción Zona Sur`:

```
graph TD
ADMZS
DIRGE --> IN&DI
DIRGE --> FINZS
DIRGE --> RHZZS
DIRGE --> MKYCO
IN&DI --> INVSW
IN&DI --> INVHW
IN&DI --> DISPR
INVSW --> SWMOV
INVSW --> SWWEB
INVHW --> HWSEN
DISPR --> DISER
SWMOV --> MOVUI
SWMOV --> MOVBA
SWWEB --> WEBUI
HWSEN --> SENIO
MOVUI --> UIDSG
MOVUI --> UIFNC
JEFZS --> PROZS
PROZS --> MANUF
PROZS --> CALDE
PROZS --> LOGUN
MANUF --> ASMZS
MANUF --> COMPZ
ASMZS --> ELELC
ASMZS --> MECAS
```

Si ahora repetimos la consulta, además de obtener datos de nivel 3, obtendremos más registros, ya que ahora tenemos varios departamentos que comparten padre:

```
select 
    d1.CodDep as depNivel1, d1.NomDep as nomNivel1,
    d2.CodDep as depNivel2, d2.NomDep as nomNivel2,
    d3.CodDep as depNivel3, d3.NomDep as nomNivel3
from departamento d1
    left join departamento d2 on d2.CodDepDep = d1.CodDep
    left join departamento d3 on d3.CodDepDep = d2.CodDep
where d1.CodDepDep is null;
-- +-----------+----------------------------+-----------+--------------------------+-----------+-------------------------+
-- | depNivel1 | nomNivel1                  | depNivel2 | nomNivel2                | depNivel3 | nomNivel3               |
-- +-----------+----------------------------+-----------+--------------------------+-----------+-------------------------+
-- | ADMZS     | Administración Zona Sur    | VENZS     | Ventas Zona Sur          | NULL      | NULL                    |
-- | DIRGE     | Dirección General          | FINZS     | Finanzas Corporativas    | NULL      | NULL                    |
-- | DIRGE     | Dirección General          | IN&DI     | Investigación y Diseño   | DISPR     | Diseño de Producto      |
-- | DIRGE     | Dirección General          | IN&DI     | Investigación y Diseño   | INVHW     | Investigación Hardware  |
-- | DIRGE     | Dirección General          | IN&DI     | Investigación y Diseño   | INVSW     | Investigación Software  |
-- | DIRGE     | Dirección General          | MKYCO     | Marketing Corporativo    | NULL      | NULL                    |
-- | DIRGE     | Dirección General          | RHZZS     | Recursos Humanos         | NULL      | NULL                    |
-- | JEFZS     | Jefatura Fábrica Zona Sur  | PROZS     | Producción Zona Sur      | CALDE     | Control de Calidad      |
-- | JEFZS     | Jefatura Fábrica Zona Sur  | PROZS     | Producción Zona Sur      | LOGUN     | Logística Unitaria      |
-- | JEFZS     | Jefatura Fábrica Zona Sur  | PROZS     | Producción Zona Sur      | MANUF     | Manufactura             |
-- +-----------+----------------------------+-----------+--------------------------+-----------+-------------------------+
-- 10 rows in set (0.001 sec)
```

De esta manera, cada nivel supone añadir nuevos atributos y unir con otra tabla, debiendo hacer una consulta específica. Pero, ¿y si de antemano no sabemos cuantos niveles tenemos de dependencia, o nos interesa saber cuantos son?

Hasta la llegada de los CTE, la única solución factible era crear un procedimiento almacenado haciendo uso de bucles y cursores. Un tipo de CTE que nos va a permitir navegar por las reflexiones reflexivas son los CTE cíclicos, o también conocidos como CTE recursivo.

### CTE recursivo

Para utilizar un [CTE recursivo](https://mariadb.com/kb/en/recursive-common-table-expressions-overview/), definiremos un CTE con el prefijo `RECURSIVE`, donde definiremos una consulta base (que definirá el punto de partida) y una consulta recursiva (que definirá cómo avanzar en la jerarquía), de la misma manera que hemos estudiado la recursividad en el módulo profesional de *Programación*. Ambas consultas las debemos unir mediante `UNION ALL` para añadir todos los registros obtenidos. Así pues, la sintaxis de un CTE recursivo es similar a:

```
WITH RECURSIVE nombreCTE AS (
    -- Consulta base
    SELECT columnas FROM tabla WHERE condicion

    UNION ALL

    -- Consulta recursiva
    SELECT t.columnas 
    FROM tabla t
    JOIN nombreCTE cte ON t.columna_hijo = cte.columna_padre
)
SELECT * FROM nombreCTE;
```

Si creamos una consulta para obtener todos los descendiente con su nivel de profundidad del departamento `JEFZS` haríamos:

```
WITH RECURSIVE jerarquiaDepartamento as (
    select CodDep, NomDep, CodDepDep, 1 as NivDep
    from departamento
    where CodDep = 'JEFZS'

    UNION ALL

    select d.CodDep, d.NomDep, d.CodDepDep, jd.NivDep + 1 as NivDep
    from departamento d join jerarquiaDepartamento jd ON d.CodDepDep = jd.CodDep
)

select * from jerarquiaDepartamento;
-- +--------+----------------------------+-----------+--------+
-- | CodDep | NomDep                     | CodDepDep | NivDep |
-- +--------+----------------------------+-----------+--------+
-- | JEFZS  | Jefatura Fábrica Zona Sur  | NULL      |      1 |
-- | PROZS  | Producción Zona Sur        | JEFZS     |      2 |
-- | CALDE  | Control de Calidad         | PROZS     |      3 |
-- | LOGUN  | Logística Unitaria         | PROZS     |      3 |
-- | MANUF  | Manufactura                | PROZS     |      3 |
-- | ASMZS  | Ensamblaje                 | MANUF     |      4 |
-- | COMPZ  | Componentes                | MANUF     |      4 |
-- | ELELC  | Ensamblaje Electrónico     | ASMZS     |      5 |
-- | MECAS  | Ensamblaje Mecánico        | ASMZS     |      5 |
-- +--------+----------------------------+-----------+--------+
-- 9 rows in set (0.000 sec)
```

Con el mismo planteamiento, si queremos partir de todos los departamentos principales, y recuperar todo el árbol de dependencias, haríamos:

```
WITH RECURSIVE jerarquiaDepartamento as (
    select CodDep, NomDep, CodDepDep, 1 as NivDep
    from departamento
    where CodDepDep is null

    UNION ALL

    select d.CodDep, d.NomDep, d.CodDepDep, jd.NivDep + 1 as NivDep
    from departamento d join jerarquiaDepartamento jd ON d.CodDepDep = jd.CodDep
)

select * from jerarquiaDepartamento;
-- +--------+----------------------------+-----------+--------+
-- | CodDep | NomDep                     | CodDepDep | NivDep |
-- +--------+----------------------------+-----------+--------+
-- | ADMZS  | Administración Zona Sur    | NULL      |      1 |
-- | DIRGE  | Dirección General          | NULL      |      1 |
-- | JEFZS  | Jefatura Fábrica Zona Sur  | NULL      |      1 |
-- | VENZS  | Ventas Zona Sur            | ADMZS     |      2 |
-- | FINZS  | Finanzas Corporativas      | DIRGE     |      2 |
-- | IN&DI  | Investigación y Diseño     | DIRGE     |      2 |
-- | MKYCO  | Marketing Corporativo      | DIRGE     |      2 |
-- | RHZZS  | Recursos Humanos           | DIRGE     |      2 |
-- | PROZS  | Producción Zona Sur        | JEFZS     |      2 |
-- | DISPR  | Diseño de Producto         | IN&DI     |      3 |
-- | INVHW  | Investigación Hardware     | IN&DI     |      3 |
-- | INVSW  | Investigación Software     | IN&DI     |      3 |
-- ...
-- | UIDSG  | Diseño UI                  | MOVUI     |      6 |
-- | UIFNC  | Funcionalidad UI           | MOVUI     |      6 |
-- +--------+----------------------------+-----------+--------+
-- 29 rows in set (0.001 sec)
```

Si queremos recuperar la ruta del árbol, lo cual suele ser una operación necesaria, en el caso base nos quedamos con el nombre del departamento, y en el recursivo, le concatenamos al contenido el nombre de sus descendientes. Cabe destacar un patrón de uso en este tipo de consultas donde queremos obtener la ruta, donde en el caso base hacemos un `CAST` por si el tipo no fuera de tipo texto, y en el recursivo, mediante `CONCAT` le añadimos, además de un separador (en nuestro caso `>`), el código del nuevo elemento:

```
WITH RECURSIVE jerarquiaDepartamento as (
    select CodDep, NomDep, CodDepDep, 1 as NivDep,
        CAST(NomDep AS CHAR(255)) AS ruta
    from departamento
    where CodDep = 'JEFZS'

    UNION ALL

    select d.CodDep, d.NomDep, d.CodDepDep, jd.NivDep + 1 as NivDep,
        CONCAT(jd.ruta, ' > ', CAST(d.NomDep AS CHAR(255))) AS ruta
    from departamento d join jerarquiaDepartamento jd ON d.CodDepDep = jd.CodDep
)

select * from jerarquiaDepartamento;
-- +--------+----------------------------+-----------+--------+--------------------------------------------------------------------------------------------------------+
-- | CodDep | NomDep                     | CodDepDep | NivDep | ruta                                                                                                   |
-- +--------+----------------------------+-----------+--------+--------------------------------------------------------------------------------------------------------+
-- | JEFZS  | Jefatura Fábrica Zona Sur  | NULL      |      1 | Jefatura Fábrica Zona Sur                                                                              |
-- | PROZS  | Producción Zona Sur        | JEFZS     |      2 | Jefatura Fábrica Zona Sur > Producción Zona Sur                                                        |
-- | CALDE  | Control de Calidad         | PROZS     |      3 | Jefatura Fábrica Zona Sur > Producción Zona Sur > Control de Calidad                                   |
-- | LOGUN  | Logística Unitaria         | PROZS     |      3 | Jefatura Fábrica Zona Sur > Producción Zona Sur > Logística Unitaria                                   |
-- | MANUF  | Manufactura                | PROZS     |      3 | Jefatura Fábrica Zona Sur > Producción Zona Sur > Manufactura                                          |
-- | ASMZS  | Ensamblaje                 | MANUF     |      4 | Jefatura Fábrica Zona Sur > Producción Zona Sur > Manufactura > Ensamblaje                             |
-- | COMPZ  | Componentes                | MANUF     |      4 | Jefatura Fábrica Zona Sur > Producción Zona Sur > Manufactura > Componentes                            |
-- | ELELC  | Ensamblaje Electrónico     | ASMZS     |      5 | Jefatura Fábrica Zona Sur > Producción Zona Sur > Manufactura > Ensamblaje > Ensamblaje Electrónico    |
-- | MECAS  | Ensamblaje Mecánico        | ASMZS     |      5 | Jefatura Fábrica Zona Sur > Producción Zona Sur > Manufactura > Ensamblaje > Ensamblaje Mecánico       |
-- +--------+----------------------------+-----------+--------+--------------------------------------------------------------------------------------------------------+
```

Si en vez de los nombres, queremos crear la ruta con los códigos, haríamos:

```
WITH RECURSIVE jerarquiaDepartamento as (
    select CodDep, NomDep, CodDepDep, 1 as NivDep,
        CAST(CodDep AS CHAR(255)) AS ruta
    from departamento
    where CodDep = 'JEFZS'

    UNION ALL

    select d.CodDep, d.NomDep, d.CodDepDep, jd.NivDep + 1 as NivDep,
        CONCAT(jd.ruta, ' > ', CAST(d.CodDep AS CHAR(255))) AS ruta
    from departamento d join jerarquiaDepartamento jd ON d.CodDepDep = jd.CodDep
)

select * from jerarquiaDepartamento;
-- +--------+----------------------------+-----------+--------+---------------------------------------+
-- | CodDep | NomDep                     | CodDepDep | NivDep | ruta                                  |
-- +--------+----------------------------+-----------+--------+---------------------------------------+
-- | JEFZS  | Jefatura Fábrica Zona Sur  | NULL      |      1 | JEFZS                                 |
-- | PROZS  | Producción Zona Sur        | JEFZS     |      2 | JEFZS > PROZS                         |
-- | CALDE  | Control de Calidad         | PROZS     |      3 | JEFZS > PROZS > CALDE                 |
-- | LOGUN  | Logística Unitaria         | PROZS     |      3 | JEFZS > PROZS > LOGUN                 |
-- | MANUF  | Manufactura                | PROZS     |      3 | JEFZS > PROZS > MANUF                 |
-- | ASMZS  | Ensamblaje                 | MANUF     |      4 | JEFZS > PROZS > MANUF > ASMZS         |
-- | COMPZ  | Componentes                | MANUF     |      4 | JEFZS > PROZS > MANUF > COMPZ         |
-- | ELELC  | Ensamblaje Electrónico     | ASMZS     |      5 | JEFZS > PROZS > MANUF > ASMZS > ELELC |
-- | MECAS  | Ensamblaje Mecánico        | ASMZS     |      5 | JEFZS > PROZS > MANUF > ASMZS > MECAS |
-- +--------+----------------------------+-----------+--------+---------------------------------------+
-- 9 rows in set (0.001 sec)
```

### Operaciones jerárquicas

Aunque en los ejemplos anteriores ya hemos realizado algunas, como recuperar los hijos directos de un nodo o toda la ruta de un determinado elemento, otras operaciones que se suelen realizar con las relaciones jerárquicas son:

- Calcular la profundidad máxima del árbol jerárquico: una vez realizado el CTE recursivo, podemos determinar cuántos niveles de profundidad tiene la jerarquía de departamentos.

  ```
  SELECT MAX(NivDep) AS profundidadMaxima
  FROM jerarquiaDepartamento;
  -- +-------------------+
  -- | profundidadMaxima |
  -- +-------------------+
  -- |                 4 |
  -- +-------------------+
  -- 1 row in set (0.001 sec)
  ```
- Calcular el presupuesto total y subtotales por rama jerárquica: Al CTE, le añadimos una columna que obtenga el presupuesto de cada departamento, y posteriormente, agrupamos para realizar el cálculo agregado:

  ```
  WITH RECURSIVE jerarquiaDepartamento as (
      select CodDep, NomDep, CodDepDep, 1 as NivDep, CAST(NomDep AS CHAR(255)) AS ruta,
          PreAnu AS PrePropio
      from departamento
      where CodDep = 'JEFZS'

      UNION ALL

      select d.CodDep, d.NomDep, d.CodDepDep, jd.NivDep + 1 as NivDep, CONCAT(jd.ruta, ' > ', d.NomDep) AS ruta,
          d.PreAnu AS PrePropio
      from departamento d join jerarquiaDepartamento jd ON d.CodDepDep = jd.CodDep
  )

  SELECT 
      j1.CodDep,
      j1.NomDep,
      j1.NivDep,
      j1.PrePropio,
      SUM(j2.PrePropio) AS PreRama
  FROM jerarquiaDepartamento j1 JOIN jerarquiaDepartamento j2
      ON j2.ruta LIKE CONCAT(j1.ruta, '%')
  GROUP BY j1.CodDep, j1.NomDep, j1.NivDep, j1.PrePropio, j1.ruta
  ORDER BY j1.ruta;
  -- +--------+----------------------------+--------+--------------+--------------+
  -- | CodDep | NomDep                     | NivDep | PrePropio    | PreRama      |
  -- +--------+----------------------------+--------+--------------+--------------+
  -- | JEFZS  | Jefatura Fábrica Zona Sur  |      1 |   6200000.00 | 329200000.00 |
  -- | PROZS  | Producción Zona Sur        |      2 | 108000000.00 | 323000000.00 |
  -- | CALDE  | Control de Calidad         |      3 |  15800000.00 |  15800000.00 |
  -- | LOGUN  | Logística Unitaria         |      3 |  27200000.00 |  27200000.00 |
  -- | MANUF  | Manufactura                |      3 |  65000000.00 | 172000000.00 |
  -- | COMPZ  | Componentes                |      4 |  23000000.00 |  23000000.00 |
  -- | ASMZS  | Ensamblaje                 |      4 |  42000000.00 |  84000000.00 |
  -- | ELELC  | Ensamblaje Electrónico     |      5 |  28000000.00 |  28000000.00 |
  -- | MECAS  | Ensamblaje Mecánico        |      5 |  14000000.00 |  14000000.00 |
  -- +--------+----------------------------+--------+--------------+--------------+
  -- 9 rows in set (0.002 sec)
  ```

[![Invítame a un café en ko-fi.com](https://storage.ko-fi.com/cdn/kofi2.png?v=3)](https://ko-fi.com/T6T8GWT9N "Invítame a un café en ko-fi.com")

Gracias por tu tiempo. Si quieres me puedes [invitar a un café en ko-fi](https://ko-fi.com/T6T8GWT9N).

¡Gracias por tu colaboración! Ayúdame a mejorar los apuntes enviándome un mail a [a.medrano@edu.gva.es](mailto:a.medrano@edu.gva.es) con tus comentarios.
