[RA2](../tags.md#tag:ra2)
[RA3](../tags.md#tag:ra3)
[RA4](../tags.md#tag:ra4)
[SQL](../tags.md#tag:sql)
[SQL - DDL](../tags.md#tag:sql---ddl)
[SQL - DML](../tags.md#tag:sql---dml)

# El tipo de datos JSON en SQL

JSON (*JavaScript Object Notation*) es un formato de intercambio de datos ligero, legible por humanos y fácilmente procesable por máquinas. Aunque nació en el entorno JavaScript, su popularidad ha crecido exponencialmente hasta convertirse en el estándar *de facto* para el intercambio de datos en servicios web y aplicaciones modernas.

Los SGBD relacionales han incorporado soporte nativo para JSON con el objetivo de combinar las ventajas del modelo relacional (consistencia, transacciones, integridad referencial) con la flexibilidad de los documentos semiestructurados, sin necesidad de recurrir a bases de datos NoSQL.

## JSON en el estándar SQL

El soporte para JSON se incorporó al estándar ISO/IEC SQL en dos grandes hitos:

- **SQL:2016** introdujo el modelo SQL/JSON: el tipo de dato `JSON` como alias de texto con validación, el lenguaje de rutas (*path language*) que comienza con `$`, y las funciones `JSON_OBJECT()`, `JSON_ARRAY()`, `JSON_ARRAYAGG()`, `JSON_OBJECTAGG()`, `JSON_VALUE()`, `JSON_QUERY()`, `JSON_EXISTS()` y `JSON_TABLE()`.
- **SQL:2023** añadió un tipo `JSON` nativo (no basado en texto), la comparación y ordenación de valores JSON, y nuevos métodos de conversión en el lenguaje de rutas.

Estándar vs. extensiones

A lo largo del documento identificaremos cada función con una de estas etiquetas:

- **Estándar SQL** — definida en SQL:2016 o SQL:2023.
- **MariaDB** — propia de MariaDB/MySQL, no recogida en el estándar.
- **PostgreSQL** — propia de PostgreSQL, no recogida en el estándar.

Versiones de referencia

| Motor | Versión | Novedades JSON |
| --- | --- | --- |
| MariaDB | 10.2 | Soporte básico: tipo `JSON`, funciones `JSON_*` |
| MariaDB | 10.6 | `JSON_TABLE()`, `JSON_VALUE()` con `RETURNING` |
| PostgreSQL | 9.2 | Tipo `JSON` nativo |
| PostgreSQL | 9.4 | Tipo `JSONB` (binario, indexable) |
| PostgreSQL | 16 | `JSON_OBJECT()`, `JSON_ARRAY()`, `JSON_VALUE()`, `JSON_QUERY()` estándar |
| PostgreSQL | 17 | `JSON_TABLE()`, `JSON_EXISTS()` estándar |

## El tipo `JSON`

### En MariaDB

En MariaDB, `JSON` es internamente un alias de `LONGTEXT`, pero con **validación automática del formato**: si se intenta insertar un valor que no sea JSON válido, el servidor lanza un error, garantizando la integridad del documento almacenado.

### En PostgreSQL

PostgreSQL ofrece **dos tipos distintos**:

| Tipo | Almacenamiento | Indexable (GIN) | Velocidad escritura | Velocidad lectura |
| --- | --- | --- | --- | --- |
| `JSON` | Texto, conserva formato original | No | Más rápida | Más lenta |
| `JSONB` | Binario descompuesto | **Sí** | Más lenta | **Más rápida** |

En la práctica, **`JSONB` es el tipo recomendado** en PostgreSQL para la mayoría de casos, ya que permite crear índices GIN altamente eficientes directamente sobre el documento, sin necesidad de columnas generadas.

```
-- PostgreSQL: tabla equivalente con JSONB
CREATE TABLE producto (
    id        SERIAL PRIMARY KEY,
    nombre    VARCHAR(100)  NOT NULL,
    categoria VARCHAR(50)   NOT NULL,
    precio    NUMERIC(10,2),
    specs     JSONB                    -- tipo binario, indexable
);

-- Índice GIN sobre todo el documento (búsquedas de contenido)
CREATE INDEX idx_producto_specs ON producto USING GIN (specs);
```

---

## Tabla de ejemplo

Usaremos la siguiente tabla a lo largo del documento. Los ejemplos en MariaDB y PostgreSQL comparten el mismo esquema:

```
-- MariaDB
CREATE TABLE producto (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    nombre    VARCHAR(100)  NOT NULL,
    categoria VARCHAR(50)   NOT NULL,
    precio    DECIMAL(10,2),
    specs     JSON
);

INSERT INTO producto (nombre, categoria, precio, specs) VALUES
    ('Portátil UltraBook 15', 'informatica', 899.99,
     '{"marca": "Acer", "pantalla": 15.6, "ram_gb": 16,
       "almacenamiento": {"tipo": "SSD", "gb": 512},
       "colores": ["plata", "negro"]}'),
    ('Smartphone Galaxy S23', 'telefonia', 749.99,
     '{"marca": "Samsung", "pantalla": 6.1, "ram_gb": 8,
       "almacenamiento": {"tipo": "UFS", "gb": 128},
       "colores": ["negro", "crema", "verde"]}'),
    ('Auriculares BT Pro', 'audio', 129.99,
     '{"marca": "Sony", "tipo": "over-ear", "autonomia_h": 30,
       "activo": true, "colores": ["negro"]}'),
    ('Teclado Mecánico RGB', 'perifericos', 79.99,
     '{"marca": "Corsair", "switch": "Cherry MX Red",
       "retroiluminado": true, "conexion": ["USB", "Bluetooth"]}'),
    ('Monitor 4K 27"', 'monitores', 349.99,
     '{"marca": "LG", "pantalla": 27, "resolucion": "3840x2160",
       "frecuencia_hz": 60, "puertos": ["HDMI", "DisplayPort", "USB-C"]}');
```

---

## Funciones de creación

### `JSON_OBJECT()` Estándar SQL:2016

Construye un objeto JSON a partir de pares clave/valor.

MariaDBPostgreSQL

```
SELECT JSON_OBJECT(
    'nombre', 'Ratón Inalámbrico',
    'marca',  'Logitech',
    'dpi',    1600
) AS especificaciones;
-- {"dpi": 1600, "marca": "Logitech", "nombre": "Ratón Inalámbrico"}
```

```
-- Sintaxis estándar (PostgreSQL ≥ 16)
SELECT JSON_OBJECT('nombre' VALUE 'Ratón Inalámbrico',
                   'marca'  VALUE 'Logitech',
                   'dpi'    VALUE 1600) AS especificaciones;

-- Alternativa propietaria (todas las versiones)
SELECT json_build_object('nombre', 'Ratón Inalámbrico',
                         'marca',  'Logitech',
                         'dpi',    1600) AS especificaciones;
```

Diferencias

La sintaxis del estándar SQL usa la palabra clave `VALUE` como separador (`'clave' VALUE valor`), mientras que MariaDB acepta la coma (`,`) al estilo MySQL. PostgreSQL 16+ admite ambas formas.

### `JSON_ARRAY()` Estándar SQL:2016

Construye un array JSON a partir de una lista de valores.

MariaDBPostgreSQL

```
SELECT JSON_ARRAY('HDMI', 'DisplayPort', 'USB-C') AS puertos;
-- ["HDMI", "DisplayPort", "USB-C"]
```

```
-- Sintaxis estándar (PostgreSQL ≥ 16)
SELECT JSON_ARRAY('HDMI', 'DisplayPort', 'USB-C') AS puertos;

-- Alternativa propietaria
SELECT json_build_array('HDMI', 'DisplayPort', 'USB-C') AS puertos;
```

---

## Extracción de datos

### `JSON_EXTRACT()` y los operadores `->` y `->>` MariaDB

La función `JSON_EXTRACT(json, ruta)` extrae un valor de un documento JSON según la ruta indicada. La ruta siempre comienza con `$`, que representa la raíz del documento:

| Expresión de ruta | Significado |
| --- | --- |
| `$` | El documento completo |
| `$.marca` | El campo `marca` del objeto raíz |
| `$.almacenamiento.tipo` | El campo `tipo` dentro del objeto `almacenamiento` |
| `$.colores[0]` | El primer elemento del array `colores` |
| `$.colores[*]` | Todos los elementos del array `colores` |
| `$**.marca` | Cualquier campo `marca` en cualquier nivel de profundidad |

El operador `->` es un atajo de `JSON_EXTRACT()`. El resultado incluye las comillas del valor JSON. Para eliminarlas se usa `JSON_UNQUOTE()` o el operador `->>`：

MariaDBPostgreSQL

```
-- Con comillas (JSON_EXTRACT / ->)
SELECT nombre, specs->'$.marca' AS marca FROM producto;

-- Sin comillas (JSON_UNQUOTE + JSON_EXTRACT / ->>)
SELECT nombre, specs->>'$.marca' AS marca FROM producto;
-- +-----------------------+---------+
-- | nombre                | marca   |
-- +-----------------------+---------+
-- | Portátil UltraBook 15 | Acer    |
-- | Smartphone Galaxy S23 | Samsung |
-- | Auriculares BT Pro    | Sony    |
-- | Teclado Mecánico RGB  | Corsair |
-- | Monitor 4K 27"        | LG      |
-- +-----------------------+---------+
```

```
-- Operador -> devuelve JSONB (con comillas si es string)
SELECT nombre, specs->'marca' AS marca FROM producto;

-- Operador ->> devuelve TEXT (sin comillas)
SELECT nombre, specs->>'marca' AS marca FROM producto;

-- Para rutas anidadas: #> (JSONB) y #>> (TEXT)
SELECT nombre, specs#>>'{almacenamiento,tipo}' AS tipo_storage
FROM producto;
```

Sintaxis de ruta diferente

MariaDB usa el lenguaje de rutas SQL/JSON estándar (`$.campo`, `$.array[0]`).
PostgreSQL usa operadores propietarios: `->` acepta la clave directamente como texto o índice entero, y `#>` acepta un array de texto con la ruta (`'{a,b,c}'`).
PostgreSQL 16+ también soporta `JSON_VALUE()` con rutas SQL/JSON estándar.

### `JSON_VALUE()` Estándar SQL:2016

Extrae un valor escalar con conversión de tipo mediante la cláusula `RETURNING`.

MariaDB (≥ 10.6)PostgreSQL (≥ 16)

```
SELECT nombre,
       JSON_VALUE(specs, '$.ram_gb' RETURNING UNSIGNED) AS ram_gb
FROM producto
WHERE categoria = 'informatica';
-- +-----------------------+--------+
-- | nombre                | ram_gb |
-- +-----------------------+--------+
-- | Portátil UltraBook 15 |     16 |
-- +-----------------------+--------+
```

```
SELECT nombre,
       JSON_VALUE(specs, '$.ram_gb' RETURNING INTEGER) AS ram_gb
FROM producto
WHERE categoria = 'informatica';
```

### `JSON_QUERY()` Estándar SQL:2016

Extrae objetos o arrays (no escalares) de un documento JSON.

MariaDBPostgreSQL (≥ 16)

```
-- MariaDB no implementa JSON_QUERY(); se usa JSON_EXTRACT() para arrays y objetos
SELECT nombre, JSON_EXTRACT(specs, '$.almacenamiento') AS storage
FROM producto
WHERE categoria = 'informatica';
-- +-----------------------+--------------------------+
-- | nombre                | storage                  |
-- +-----------------------+--------------------------+
-- | Portátil UltraBook 15 | {"gb": 512, "tipo": "SSD"} |
-- +-----------------------+--------------------------+
```

```
SELECT nombre,
       JSON_QUERY(specs, '$.almacenamiento') AS storage
FROM producto
WHERE categoria = 'informatica';
```

`JSON_VALUE()` devuelve **escalares** (strings, números, booleanos). `JSON_QUERY()` devuelve **objetos y arrays**. MariaDB cubre ambos casos con `JSON_EXTRACT()`, que funciona para cualquier tipo de valor.

---

## Funciones de información

### `JSON_EXISTS()` Estándar SQL:2016

Comprueba si una ruta existe en el documento JSON.

MariaDBPostgreSQL (≥ 17)

```
-- MariaDB no implementa JSON_EXISTS(); se usa JSON_CONTAINS_PATH()
SELECT nombre
FROM producto
WHERE JSON_CONTAINS_PATH(specs, 'one', '$.ram_gb') = 1;
```

```
-- Sintaxis estándar
SELECT nombre
FROM producto
WHERE JSON_EXISTS(specs, '$.ram_gb');

-- Alternativa propietaria con el operador ?
SELECT nombre FROM producto WHERE specs ? 'ram_gb';
```

### `JSON_TYPE()` MariaDB / `json_typeof()` PostgreSQL

Devuelve el tipo JSON de un valor: `OBJECT`, `ARRAY`, `STRING`, `INTEGER`, `DOUBLE`, `BOOLEAN` o `NULL`:

MariaDBPostgreSQL

```
SELECT JSON_TYPE(specs)             AS tipo_raiz,
       JSON_TYPE(specs->'$.colores') AS tipo_colores,
       JSON_TYPE(specs->'$.activo')  AS tipo_activo
FROM producto
WHERE nombre = 'Auriculares BT Pro';
-- +-----------+--------------+-------------+
-- | tipo_raiz | tipo_colores | tipo_activo |
-- +-----------+--------------+-------------+
-- | OBJECT    | ARRAY        | BOOLEAN     |
-- +-----------+--------------+-------------+
```

```
SELECT json_typeof(specs)               AS tipo_raiz,
       json_typeof(specs->'colores')     AS tipo_colores,
       json_typeof(specs->'activo')      AS tipo_activo
FROM producto
WHERE nombre = 'Auriculares BT Pro';
-- +-----------+--------------+-------------+
-- | tipo_raiz | tipo_colores | tipo_activo |
-- +-----------+--------------+-------------+
-- | object    | array        | boolean     |
-- +-----------+--------------+-------------+
```

### `JSON_VALID()` MariaDB

Comprueba si una cadena es JSON válido. Devuelve `1` o `0`. PostgreSQL no necesita esta función porque **lanza un error en el propio `INSERT`** si el valor no es válido — la validación se hace en el tipo, no en la función.

```
-- MariaDB
SELECT JSON_VALID('{"clave": "valor"}') AS valido;  -- 1
SELECT JSON_VALID('{mal formado}')       AS valido;  -- 0

-- Detectar filas con JSON no válido (útil al migrar datos de columnas TEXT)
SELECT id, nombre FROM producto WHERE JSON_VALID(specs) = 0;
```

### `JSON_LENGTH()` MariaDB / `jsonb_array_length()` PostgreSQL

MariaDBPostgreSQL

```
-- Número de campos en el objeto raíz de cada producto
SELECT nombre, JSON_LENGTH(specs) AS num_campos
FROM producto;
-- +-----------------------+------------+
-- | nombre                | num_campos |
-- +-----------------------+------------+
-- | Portátil UltraBook 15 |          5 |
-- | Smartphone Galaxy S23 |          5 |
-- | Auriculares BT Pro    |          5 |
-- | Teclado Mecánico RGB  |          4 |
-- | Monitor 4K 27"        |          5 |
-- +-----------------------+------------+

-- Número de colores
SELECT nombre, JSON_LENGTH(specs, '$.colores') AS num_colores
FROM producto
WHERE JSON_CONTAINS_PATH(specs, 'one', '$.colores') = 1;
```

```
-- Para arrays: jsonb_array_length()
SELECT nombre, jsonb_array_length(specs->'colores') AS num_colores
FROM producto
WHERE specs ? 'colores';

-- Para contar claves de un objeto: json_object_keys() + COUNT
SELECT nombre, COUNT(*) AS num_campos
FROM producto, json_object_keys(specs::json) AS k
GROUP BY nombre;
```

### `JSON_DEPTH()` MariaDB

Devuelve la profundidad máxima de un documento JSON. No tiene equivalente directo en PostgreSQL.

```
SELECT nombre, JSON_DEPTH(specs) AS profundidad
FROM producto;
-- +-----------------------+-------------+
-- | nombre                | profundidad |
-- +-----------------------+-------------+
-- | Portátil UltraBook 15 |           3 |
-- | Auriculares BT Pro    |           2 |
-- +-----------------------+-------------+
```

### `JSON_KEYS()` MariaDB / `json_object_keys()` PostgreSQL

MariaDBPostgreSQL

```
SELECT nombre, JSON_KEYS(specs) AS claves
FROM producto
WHERE nombre = 'Portátil UltraBook 15';
-- +-------------------------------------------------------------------+
-- | claves                                                            |
-- +-------------------------------------------------------------------+
-- | ["marca", "pantalla", "ram_gb", "almacenamiento", "colores"]     |
-- +-------------------------------------------------------------------+
```

```
-- Devuelve una fila por clave (expansión en filas, no array)
SELECT json_object_keys(specs::json) AS clave
FROM producto
WHERE nombre = 'Portátil UltraBook 15';
-- +----------------+
-- | clave          |
-- +----------------+
-- | marca          |
-- | pantalla       |
-- | ram_gb         |
-- | almacenamiento |
-- | colores        |
-- +----------------+
```

---

## Funciones de búsqueda

### `JSON_CONTAINS()` MariaDB / operador `@>` PostgreSQL

MariaDBPostgreSQL

```
-- Productos disponibles en color negro
SELECT nombre
FROM producto
WHERE JSON_CONTAINS(specs->'$.colores', '"negro"');

-- Productos cuyo almacenamiento sea SSD
SELECT nombre
FROM producto
WHERE JSON_CONTAINS(specs->'$.almacenamiento', '{"tipo": "SSD"}');
```

```
-- El operador @> comprueba si el lado izquierdo contiene al derecho
-- Productos en color negro
SELECT nombre
FROM producto
WHERE specs->'colores' @> '"negro"';

-- Productos con almacenamiento SSD
SELECT nombre
FROM producto
WHERE specs->'almacenamiento' @> '{"tipo": "SSD"}';

-- El operador inverso <@ (el derecho contiene al izquierdo)
SELECT nombre
FROM producto
WHERE '{"tipo": "SSD"}' <@ (specs->'almacenamiento');
```

Ventaja de PostgreSQL con JSONB

El operador `@>` sobre columnas `JSONB` puede aprovechar un **índice GIN**, lo que hace las búsquedas de contenido extremadamente rápidas sin necesidad de columnas generadas.

### `JSON_CONTAINS_PATH()` MariaDB / operador `?` PostgreSQL

MariaDBPostgreSQL

```
-- Productos que tienen el campo 'ram_gb'
SELECT nombre
FROM producto
WHERE JSON_CONTAINS_PATH(specs, 'one', '$.ram_gb') = 1;

-- Productos con 'ram_gb' Y 'almacenamiento'
SELECT nombre
FROM producto
WHERE JSON_CONTAINS_PATH(specs, 'all', '$.ram_gb', '$.almacenamiento') = 1;
```

```
-- Clave existe: operador ?
SELECT nombre FROM producto WHERE specs ? 'ram_gb';

-- Cualquiera de varias claves existe: operador ?|
SELECT nombre FROM producto WHERE specs ?| ARRAY['ram_gb', 'autonomia_h'];

-- Todas las claves existen: operador ?&
SELECT nombre FROM producto WHERE specs ?& ARRAY['ram_gb', 'almacenamiento'];
```

### `JSON_SEARCH()` MariaDB

Busca una cadena dentro del documento y devuelve la ruta. PostgreSQL usa el operador `@@` con el tipo `jsonpath` para búsquedas más expresivas, pero no tiene un equivalente directo de `JSON_SEARCH()`.

MariaDBPostgreSQL

```
-- ¿En qué ruta se encuentra el color 'negro'?
SELECT nombre, JSON_SEARCH(specs, 'one', 'negro') AS ruta
FROM producto
WHERE JSON_SEARCH(specs, 'one', 'negro') IS NOT NULL;
-- +-----------------------+----------------+
-- | nombre                | ruta           |
-- +-----------------------+----------------+
-- | Portátil UltraBook 15 | "$.colores[1]" |
-- | Smartphone Galaxy S23 | "$.colores[0]" |
-- +-----------------------+----------------+

-- Búsqueda con comodín (% como en LIKE)
SELECT nombre FROM producto
WHERE JSON_SEARCH(specs, 'one', 'USB%') IS NOT NULL;
```

```
-- Usando el operador @@ con jsonpath (búsqueda más potente)
-- Productos cuyo array 'colores' contenga el string 'negro'
SELECT nombre
FROM producto
WHERE specs @@ '$.colores[*] == "negro"';

-- Productos con algún puerto que empiece por 'USB'
SELECT nombre
FROM producto
WHERE specs @@ '$.puertos[*] starts with "USB"';
```

---

## Funciones de modificación

Las funciones de modificación **devuelven una copia** del documento con los cambios aplicados. Para persistirlos hay que usarlas con `UPDATE`.

### `JSON_SET()` MariaDB / `jsonb_set()` PostgreSQL

Establece el valor de una o más claves. Si la clave **no existe, la crea**; si **existe, la actualiza**:

MariaDBPostgreSQL

```
UPDATE producto
SET specs = JSON_SET(specs,
    '$.garantia_anos', 2,
    '$.stock', 45)
WHERE nombre = 'Portátil UltraBook 15';
```

```
-- jsonb_set(target, path, new_value, create_missing := true)
UPDATE producto
SET specs = jsonb_set(
    jsonb_set(specs, '{garantia_anos}', '2'),
    '{stock}', '45'
)
WHERE nombre = 'Portátil UltraBook 15';
```

En PostgreSQL, `jsonb_set()` solo modifica un campo por llamada; para varios campos hay que anidar las llamadas o usar `||` (operador de concatenación/merge).

### `JSON_INSERT()` MariaDB

Solo inserta valores nuevos: si la clave ya existe, no la modifica. PostgreSQL usa `jsonb_insert()` o el operador `||` con lógica condicional.

MariaDBPostgreSQL

```
UPDATE producto
SET specs = JSON_INSERT(specs, '$.stock', 100)
WHERE categoria = 'telefonia';
```

```
-- jsonb_insert(target, path, new_value, insert_after := false)
-- Inserta en un array o añade una clave nueva (si no existe, create_missing)
UPDATE producto
SET specs = specs || '{"stock": 100}'::jsonb
WHERE categoria = 'telefonia'
  AND NOT (specs ? 'stock');   -- solo si no existe
```

### `JSON_REPLACE()` MariaDB

Solo actualiza valores existentes: si la clave no existe, no hace nada.

MariaDBPostgreSQL

```
UPDATE producto
SET specs = JSON_REPLACE(specs, '$.ram_gb', 32)
WHERE nombre = 'Portátil UltraBook 15';
```

```
-- jsonb_set con create_missing = false solo actualiza si existe
UPDATE producto
SET specs = jsonb_set(specs, '{ram_gb}', '32', false)
WHERE nombre = 'Portátil UltraBook 15';
```

Regla mnemotécnica

- `JSON_SET()` = inserta **o** actualiza (comportamiento más habitual).
- `JSON_INSERT()` = solo inserta si **no existe**.
- `JSON_REPLACE()` = solo actualiza si **ya existe**.

### `JSON_REMOVE()` MariaDB / operador `-` PostgreSQL

MariaDBPostgreSQL

```
-- Eliminar el campo 'stock'
UPDATE producto SET specs = JSON_REMOVE(specs, '$.stock');

-- Eliminar el primer elemento del array de colores
UPDATE producto
SET specs = JSON_REMOVE(specs, '$.colores[0]')
WHERE nombre = 'Smartphone Galaxy S23';
```

```
-- Eliminar una clave con el operador -
UPDATE producto SET specs = specs - 'stock';

-- Eliminar por ruta anidada con el operador #-
UPDATE producto
SET specs = specs #- '{colores, 0}'
WHERE nombre = 'Smartphone Galaxy S23';
```

### `JSON_ARRAY_APPEND()` MariaDB / `jsonb_insert()` PostgreSQL

Añade valores al final de un array en la ruta indicada.

MariaDBPostgreSQL

```
UPDATE producto
SET specs = JSON_ARRAY_APPEND(specs, '$.puertos', 'Thunderbolt')
WHERE nombre = 'Monitor 4K 27"';
```

```
-- jsonb_insert(target, path, new_value, insert_after := true)
-- El índice -1 apunta al final del array
UPDATE producto
SET specs = jsonb_insert(specs, '{puertos, -1}', '"Thunderbolt"', true)
WHERE nombre = 'Monitor 4K 27"';
```

### `JSON_MERGE_PATCH()` y `JSON_MERGE_PRESERVE()` MariaDB / operador `||` PostgreSQL

MariaDBPostgreSQL

```
-- JSON_MERGE_PATCH: las claves duplicadas del segundo sobrescriben al primero
SELECT JSON_MERGE_PATCH('{"a": 1, "b": 2}', '{"b": 99, "c": 3}');
-- {"a": 1, "b": 99, "c": 3}

-- JSON_MERGE_PRESERVE: las claves duplicadas se combinan en un array
SELECT JSON_MERGE_PRESERVE('{"a": 1, "b": 2}', '{"b": 99, "c": 3}');
-- {"a": 1, "b": [2, 99], "c": 3}
```

```
-- El operador || fusiona objetos JSONB (equivale a JSON_MERGE_PATCH)
SELECT '{"a": 1, "b": 2}'::jsonb || '{"b": 99, "c": 3}'::jsonb;
-- {"a": 1, "b": 99, "c": 3}
```

---

## Funciones de agregación

### `JSON_ARRAYAGG()` Estándar SQL:2016 / `json_agg()` PostgreSQL

MariaDBPostgreSQL

```
SELECT categoria, JSON_ARRAYAGG(nombre) AS productos
FROM producto
GROUP BY categoria;
-- +-------------+---------------------------------------------------+
-- | categoria   | productos                                         |
-- +-------------+---------------------------------------------------+
-- | audio       | ["Auriculares BT Pro"]                            |
-- | informatica | ["Portátil UltraBook 15"]                         |
-- | monitores   | ["Monitor 4K 27\""]                               |
-- | perifericos | ["Teclado Mecánico RGB"]                          |
-- | telefonia   | ["Smartphone Galaxy S23"]                         |
-- +-------------+---------------------------------------------------+
```

```
-- Función propietaria (todas las versiones)
SELECT categoria, json_agg(nombre) AS productos
FROM producto
GROUP BY categoria;

-- Sintaxis estándar (PostgreSQL ≥ 16)
SELECT categoria, JSON_ARRAYAGG(nombre) AS productos
FROM producto
GROUP BY categoria;
```

### `JSON_OBJECTAGG()` Estándar SQL:2016 / `json_object_agg()` PostgreSQL

MariaDBPostgreSQL

```
SELECT categoria, JSON_OBJECTAGG(nombre, precio) AS precios
FROM producto
GROUP BY categoria;
```

```
-- Función propietaria (todas las versiones)
SELECT categoria, json_object_agg(nombre, precio) AS precios
FROM producto
GROUP BY categoria;

-- Sintaxis estándar (PostgreSQL ≥ 16)
SELECT categoria, JSON_OBJECTAGG(nombre VALUE precio) AS precios
FROM producto
GROUP BY categoria;
```

---

## `JSON_TABLE()` Estándar SQL:2016

Transforma datos JSON en filas y columnas relacionales. Es la función más potente para combinar JSON con el modelo relacional.

MariaDB (≥ 10.6)PostgreSQL (≥ 17)

```
-- Extraer cada puerto del monitor como una fila independiente
SELECT p.nombre, jt.puerto
FROM producto p,
     JSON_TABLE(
         specs,
         '$.puertos[*]'
         COLUMNS (
             puerto VARCHAR(30) PATH '$'
         )
     ) AS jt
WHERE p.nombre = 'Monitor 4K 27"';
-- +-----------------+-------------+
-- | nombre          | puerto      |
-- +-----------------+-------------+
-- | Monitor 4K 27"  | HDMI        |
-- | Monitor 4K 27"  | DisplayPort |
-- | Monitor 4K 27"  | USB-C       |
-- +-----------------+-------------+
```

```
-- Sintaxis estándar disponible desde PostgreSQL 17
SELECT p.nombre, jt.puerto
FROM producto p,
     JSON_TABLE(
         specs,
         '$.puertos[*]'
         COLUMNS (
             puerto text PATH '$'
         )
     ) AS jt
WHERE p.nombre = 'Monitor 4K 27"';

-- Alternativa propietaria con jsonb_array_elements() (todas las versiones)
SELECT p.nombre, puerto
FROM producto p,
     jsonb_array_elements_text(p.specs->'puertos') AS puerto
WHERE p.nombre = 'Monitor 4K 27"';
```

---

## Columnas generadas e índices

El mayor inconveniente de las columnas JSON en MariaDB es que **no se pueden indexar directamente**. La solución es crear **columnas generadas** que extraigan un valor concreto del JSON.

En PostgreSQL, gracias al tipo `JSONB`, se pueden crear índices GIN sobre el documento completo sin columnas intermedias.

MariaDB — columnas generadasPostgreSQL — índice GIN directo

```
-- Columna virtual (no ocupa espacio en disco)
ALTER TABLE producto
    ADD COLUMN marca VARCHAR(50)
        GENERATED ALWAYS AS (specs->>'$.marca') VIRTUAL;

-- Columna almacenada (se persiste, admite índice B-tree)
ALTER TABLE producto
    ADD COLUMN ram_gb INT UNSIGNED
        GENERATED ALWAYS AS (
            JSON_VALUE(specs, '$.ram_gb' RETURNING UNSIGNED)
        ) STORED;

CREATE INDEX idx_producto_marca  ON producto (marca);
CREATE INDEX idx_producto_ram_gb ON producto (ram_gb);
```

```
-- Índice GIN sobre todo el documento JSONB
CREATE INDEX idx_producto_specs ON producto USING GIN (specs);

-- Estas consultas aprovechan automáticamente el índice GIN:
SELECT nombre FROM producto WHERE specs @> '{"marca": "Samsung"}';
SELECT nombre FROM producto WHERE specs ? 'ram_gb';
SELECT nombre FROM producto WHERE specs->'colores' @> '"negro"';

-- También se puede crear un índice B-tree sobre una expresión JSON
CREATE INDEX idx_producto_marca
    ON producto ((specs->>'marca'));
```

¿Cuándo usar `VIRTUAL` vs `STORED` en MariaDB?

- Usa `VIRTUAL` cuando la columna se consulte con poca frecuencia o el documento JSON cambie a menudo.
- Usa `STORED` cuando necesites crear un índice sobre el campo o la expresión sea costosa de calcular.

---

## `JSON_PRETTY()` MariaDB / `jsonb_pretty()` PostgreSQL

Formatea un documento JSON con sangría para facilitar su lectura.

MariaDBPostgreSQL

```
SELECT JSON_PRETTY(specs) AS especificaciones
FROM producto WHERE nombre = 'Portátil UltraBook 15'\G
-- {
--   "marca": "Acer",
--   "pantalla": 15.6,
--   "ram_gb": 16,
--   "almacenamiento": {
--     "gb": 512,
--     "tipo": "SSD"
--   },
--   "colores": ["plata", "negro"]
-- }
```

```
SELECT jsonb_pretty(specs) AS especificaciones
FROM producto WHERE nombre = 'Portátil UltraBook 15';
```

---

## Tabla comparativa completa

| Función / Operación | Estándar SQL | MariaDB | PostgreSQL |
| --- | --- | --- | --- |
| Tipo JSON | SQL:2023 (T801) | `JSON` (alias de LONGTEXT) | `JSON` / `JSONB` |
| Crear objeto | SQL:2016 | `JSON_OBJECT(k, v)` | `JSON_OBJECT('k' VALUE v)` / `json_build_object()` |
| Crear array | SQL:2016 | `JSON_ARRAY(v, ...)` | `JSON_ARRAY(v, ...)` / `json_build_array()` |
| Extraer valor (escalar) | SQL:2016 `JSON_VALUE` | `JSON_EXTRACT()` / `->>` | `JSON_VALUE()` / `->>` |
| Extraer objeto/array | SQL:2016 `JSON_QUERY` | `JSON_EXTRACT()` / `->` | `JSON_QUERY()` / `->` / `#>` |
| Comprobar si ruta existe | SQL:2016 `JSON_EXISTS` | `JSON_CONTAINS_PATH()` | `JSON_EXISTS()` / `?` |
| Buscar texto | — | `JSON_SEARCH()` | Operador `@@` con `jsonpath` |
| Tipo del valor | — | `JSON_TYPE()` | `json_typeof()` |
| Validar JSON | — | `JSON_VALID()` | (validación en INSERT) |
| Nº de elementos | — | `JSON_LENGTH()` | `jsonb_array_length()` |
| Profundidad | — | `JSON_DEPTH()` | Sin equivalente directo |
| Claves del objeto | — | `JSON_KEYS()` | `json_object_keys()` |
| Comprobar contenido | — | `JSON_CONTAINS()` | Operador `@>` |
| Insertar o actualizar | — | `JSON_SET()` | `jsonb_set()` |
| Solo insertar | — | `JSON_INSERT()` | `\|\|` + condición / `jsonb_insert()` |
| Solo actualizar | — | `JSON_REPLACE()` | `jsonb_set(..., false)` |
| Eliminar campo | — | `JSON_REMOVE()` | Operador `-` / `#-` |
| Añadir a array | — | `JSON_ARRAY_APPEND()` | `jsonb_insert()` |
| Fusionar (patch) | — | `JSON_MERGE_PATCH()` | Operador `\|\|` |
| Agregar en array JSON | SQL:2016 | `JSON_ARRAYAGG()` | `JSON_ARRAYAGG()` / `json_agg()` |
| Agregar en objeto JSON | SQL:2016 | `JSON_OBJECTAGG()` | `JSON_OBJECTAGG()` / `json_object_agg()` |
| JSON → tabla relacional | SQL:2016 | `JSON_TABLE()` (≥ 10.6) | `JSON_TABLE()` (≥ 17) / `jsonb_array_elements()` |
| Formato legible | — | `JSON_PRETTY()` | `jsonb_pretty()` |
| Índice sobre JSON | — | Columnas generadas + B-tree | GIN sobre `JSONB` |

---

## Referencias

- [Modern SQL](https://modern-sql.com/)

## Actividades

- **ACJSON01**. (RABD.2 // CE2a, CE2b, CE2c // 3p) Crea la base de datos `biblioteca_json` con la siguiente tabla:

  ```
  CREATE TABLE libro (
      id      INT AUTO_INCREMENT PRIMARY KEY,  -- o SERIAL en PostgreSQL
      titulo  VARCHAR(200) NOT NULL,
      metadata JSON                             -- o JSONB en PostgreSQL
  );
  ```

  El campo `metadata` debe contener, al menos: `autor` (string), `anyo_publicacion` (número entero), `editorial` (string), `generos` (array de strings) y `edicion` (objeto con los campos `numero` e `idioma`).

  1. Inserta al menos 5 libros con datos realistas.
  2. Muestra todos los libros con su título, autor (extraído del JSON, sin comillas) y año de publicación, ordenados por año de forma descendente.
  3. Filtra los libros publicados después de 2000 usando `JSON_EXTRACT()` (MariaDB) o el operador `->>` (PostgreSQL) en el `WHERE`.
  4. Muestra el título y el número de géneros de cada libro usando `JSON_LENGTH()` (MariaDB) o `jsonb_array_length()` (PostgreSQL).
  5. Lista los libros que pertenecen al género `'Ciencia ficción'` usando `JSON_CONTAINS()` (MariaDB) o el operador `@>` (PostgreSQL).

- **ACJSON02**. (RABD.3 // CE3b // 3p) Usando la tabla `producto` de los apuntes:

  1. Lista el nombre y el tamaño de pantalla (en pulgadas) de todos los productos que tengan el campo `pantalla` en sus especificaciones.
  2. Muestra los productos disponibles en más de un color.
  3. Busca todos los productos de la marca `Sony` o `LG`.
  4. Lista los productos que admitan conexión `Bluetooth`.
  5. Para cada producto, muestra su nombre, precio y el tipo de almacenamiento (si lo tienen). Los que no tengan ese campo deben aparecer con `NULL`.

- **ACJSON03**. (RABD.4 // CE4b // 3p) Usando la tabla `producto`, realiza las siguientes modificaciones y comprueba el resultado con una consulta `SELECT` tras cada operación:

  1. Añade el campo `garantia_anos` con valor `2` a todos los productos de la categoría `informatica` con `JSON_SET()` (MariaDB) o `jsonb_set()` (PostgreSQL).
  2. Cambia el valor del campo `marca` de `Corsair` a `Corsair Gaming`.
  3. Elimina el campo `activo` del producto `Auriculares BT Pro`.
  4. Añade el puerto `'Thunderbolt'` al array `puertos` del monitor.
  5. Usa `JSON_INSERT()` (MariaDB) o el operador `||` con condición (PostgreSQL) para intentar añadir el campo `marca` con el valor `'Desconocida'` a todos los productos. Explica por qué algunos no se ven afectados.

- **ARJSON01**. (RABD.2 // CE2a // 2p) Investiga y responde, con al menos dos líneas para cada cuestión:

  1. ¿Qué diferencia hay entre `JSON_SET()`, `JSON_INSERT()` y `JSON_REPLACE()`? ¿En qué situación usarías cada una?
  2. ¿Por qué MariaDB no puede indexar directamente una columna `JSON`? ¿Cómo lo soluciona? ¿Por qué PostgreSQL sí puede indexar `JSONB`?
  3. ¿Qué diferencia hay entre `JSON` y `JSONB` en PostgreSQL? ¿Cuándo conviene usar cada uno?
  4. ¿Qué funciones de la tabla comparativa son parte del estándar SQL:2016? ¿Cuáles son extensiones de MariaDB o PostgreSQL?
  5. ¿Cuándo tiene sentido utilizar JSON en una base de datos relacional en lugar de añadir nuevas columnas a la tabla? ¿Y cuándo sería un error de diseño?

- **ARJSON02**. (RABD.3 // CE3b // 3p) Crea una tabla `pedido` con las columnas `id` (PK), `cliente` (VARCHAR) y `lineas` (JSON / JSONB). El campo `lineas` debe almacenar un array de objetos, donde cada objeto represente una línea de pedido con los campos `producto_id`, `cantidad` y `precio_unitario`.

  1. Inserta 3 pedidos de ejemplo, con al menos 2 líneas cada uno.
  2. Recupera el primer producto (`producto_id`) de cada pedido.
  3. Muestra cuántas líneas tiene cada pedido.
  4. Calcula el importe total de cada pedido sumando `cantidad × precio_unitario` para cada línea. (Pista: usa `JSON_TABLE()` en MariaDB o `jsonb_array_elements()` en PostgreSQL para expandir el array en filas y luego agregar.)

- **APJSON01**. (RABD.2, RABD.3 // CE2b, CE2c, CE3b // 4p) Diseña e implementa una base de datos `tienda_json` con las tablas `categoria` y `producto` (con columna `atributos` de tipo JSON / JSONB). Los atributos deben variar según la categoría:

  - *Smartphones*: `marca`, `pantalla_pulgadas`, `bateria_mah`, `camara_mp`, `conectividad` (array).
  - *Portátiles*: `marca`, `procesador`, `ram_gb`, `almacenamiento` (objeto con `tipo` y `gb`), `peso_kg`.
  - *Televisores*: `marca`, `pulgadas`, `resolucion`, `smart_tv` (booleano), `tecnologia`.

  A continuación:

  1. Inserta al menos 3 productos de cada categoría con datos realistas.
  2. En MariaDB, crea columnas generadas e índices B-tree; en PostgreSQL, crea un índice GIN sobre `atributos`. Explica la diferencia de enfoque.
  3. Escribe 5 consultas que crucen la tabla `categoria` con los `atributos` JSON, usando `JOIN` y filtros.
  4. Genera un informe por categoría con `JSON_ARRAYAGG()` y `JSON_OBJECTAGG()`.

- **APJSON02**. (RABD.3 // CE3b // 4p) Investiga la función `JSON_TABLE()` (MariaDB ≥ 10.6, PostgreSQL ≥ 17) y su alternativa propietaria `jsonb_array_elements()` en PostgreSQL.

  A partir de la tabla `producto`:

  1. Usa `JSON_TABLE()` para extraer cada color como una fila independiente, mostrando nombre del producto y color.
  2. Agrupa los resultados anteriores para obtener, por color, cuántos productos lo incluyen.
  3. Implementa la misma consulta en PostgreSQL usando `jsonb_array_elements_text()`.
  4. Compara ambas aproximaciones en cuanto a legibilidad, portabilidad y rendimiento. ¿Cuál es más cercana al estándar SQL?

[![Invítame a un café en ko-fi.com](https://storage.ko-fi.com/cdn/kofi2.png?v=3)](https://ko-fi.com/T6T8GWT9N "Invítame a un café en ko-fi.com")

Gracias por tu tiempo. Si quieres me puedes [invitar a un café en ko-fi](https://ko-fi.com/T6T8GWT9N).

¡Gracias por tu colaboración! Ayúdame a mejorar los apuntes enviándome un mail a [a.medrano@edu.gva.es](mailto:a.medrano@edu.gva.es) con tus comentarios.
