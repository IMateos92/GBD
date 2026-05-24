# Entorno

En esta páginas vamos a agrupar las herramientas que vamos a utilizar en el curso, con las instrucciones o comandos necesarios para su puesta en marcha.

## Herramientas

Las herramientas que vamos a utilizar a lo largo del curso son:

- [MariaDB](https://mariadb.org/): SGBD relacional basado en *MySQL*.
  - [PhpMyAdmin](https://www.phpmyadmin.net/): herramienta gráfica de gestión de *MariaDB* / *MySQL*
- [PostgreSQL](https://www.postgresql.org/): SGBD relacional.
  - [PgAdmin](https://www.pgadmin.org/): herramienta gráfica de gestión de *PostgreSQL*.
- [Redis](https://redis.io/): Base de datos NoSQL de tipo clave-valor.
- [MongoDB](https://www.mongodb.com/): Base de datos NoSQL de tipo documental.
- [Grafana](https://grafana.com/): herramienta de observabilidad y visualización de datos.
- [Visual Studio Code](https://code.visualstudio.com/): editor de texto/código.

Docker

En este módulo vamos a utilizar [Docker](https://www.docker.com/) como herramienta para probar las bases de datos. En pocas palabras, *Docker* permite lanzar contenedores que contienen los servicios que necesitemos. En este módulo no vamos a aprender a crear contenedores, sólo a lanzar contenedores ya existentes.

Para ello, el primer paso es instalar [Docker Desktop](https://www.docker.com/products/docker-desktop/) en tu ordenador.

## MariaDB

*MariaDB* es un SGBD relacional basado en *MySQL*, ampliamente utilizado en el desarrollo de aplicaciones web y multiplataforma.

*MariaDB* dispone de un interfaz basada en páginas web llamada *PhpMyAdmin*, que a través de un servidor web, por ejemplo *Apache*, permite administrar las bases de datos de un servidor desde cualquier equipo de la red.

Este *software* dispone de opciones para realizar prácticamente cualquier operación que se pueda realizar vía SQL. Permite gestionar las bases de datos de un servidor, crear, borrar y modificar tablas, lanzar comandos SQL, exportar e importar información, recopilar estadísticas, hacer copias de seguridad, etc. Además dispone de un pequeño diseñador que permite gestionar las relaciones de las tablas.

Para lanzar tanto *MariaDB* com *PhpMyAdmin* mediante *Docker*, el primer paso es crear la definición de los dos contenedores en un archivo *Docker Compose*, el cual hemos llamado [`docker-compose-mariadb.yml`](resources/docker-compose-mariadb.yml), donde además de la definición de ambos contenedores, configuraremos el usuario para acceder al SBGD, así como el volumen para los datos:

docker-compose-mariadb.yml

```
services:
  mariadb:
    image: mariadb:latest
    container_name: mdb
    ports:
      - 3306:3306
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=pruebas
      - MYSQL_USER=s8a
      - MYSQL_PASSWORD=s8a
    volumes:
      - mariabd_data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin
    container_name: phpma
    ports:
      - 8080:80
    environment:
      - PMA_HOST=mariadb
    depends_on:
      - mariadb

volumes:
  mariabd_data:
```

Para lanzar los contenedores, utilizaremos el siguiente comando:

```
docker compose -p mariadb-s8a -f docker-compose-mariadb.yml up -d
```

### Cliente `mariadb`

Recuerda arrancar el contenedor

No te olvides que debes arrancar el contenedor cada vez que quieras usarlo, ya sea mediante el botón *play* en *Docker Desktop*, o mediante `docker start <nombreContenedor>`:

```
docker start mdb
```

Primero nos conectamos al contenedor (el cual en el archivo *docker-compose* hemos llamado `mdb`):

```
docker exec -it mdb bash
```

Copiando archivos en el contenedor

Si queremos introducir un archivo dentro del contenedor, por ejemplo, para importar sus datos, previamente lo hemos de copiar dentro (un buen destino es `/tmp`, ya que existe en todos los contenedores):

```
docker cp datos.sql mdb:/tmp
```

A continuación, con el cliente del SGBD, nos conectamos al servidor (al ser `localhost` no hace falta que lo indiquemos) pasándole el usuario (`-u nomusuario`) y la contraseña (`-pcontraseña`)`:

```
mariadb -u s8a -ps8a pruebas
```

Y obtendremos información como que nos hemos conectado correctamente, y en la última línea muestra que ha conectado con la bd `pruebas`:

```
root@e6dbf61ca4db:/# mariadb -u s8a -ps8a pruebas
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 5
Server version: 11.4.2-MariaDB-ubu2404 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [pruebas]>
```

Si quieres más información sobre como conectar con *MariaDB* y todos los parámetros disponibles, consulta la [documentación oficial](https://mariadb.com/kb/en/connecting-to-mariadb/).

s8a superusuario

Si queremos evitar usar el usuario `root` para crear bases de datos e importar esquemas, es muy cómodo configurar el usuario que hemos creado para que pueda acceder a todos los recursos. Para ello, una vez hemos entrado con root:

```
mariadb -u root -proot
```

Le damos todos permisos a todos los recursos al usuario `s8a`:

```
GRANT ALL PRIVILEGES ON *.* TO 's8a'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;
```

La gestión de permisos la estudiaremos en la unidad *9.- Lenguaje SQL: Control de Datos DCL y Transacciones TCL*.

![](images/00phpmyadmin-login.png "Login en PhpMyAdmin")

Login en PhpMyAdmin

### PhpMyAdmin

Para acceder a la interfaz gráfica de *PhpMyAdmin*, desde nuestro navegador web, nos conectamos a <http://localhost:8080>, donde veremos el interfaz de *login*, y entramos con el usuario `s8a` y la contraseña `s8a` que habíamos configurado previamente en la definición del contenedor.

Una vez dentro, en el menú lateral veremos las bases de datos a las cuales tenemos acceso, así como, una vez seleccionada una en concreto, las tablas con sus columnas e índices, y en la parte derecha, las diferentes opciones mediante el menú superior (desde herramientas para insertar o buscar registros, como importar o exportar los datos u obtener una representación gráfica del modelo físico):

![](images/00phpmyadmin-estructura.png)

Estructura de una tabla en PhpMyAdmin

Aprendiendo *PhpMyAdmin*

Aunque en la red existen multitud de recursos con artículos y tutoriales sobre *PhpMyAdmin*, a lo largo del curso iremos utilizando la herramienta y viendo las posibilidades que ofrece conforme las vayamos necesitando.

### Grafana

[Grafana](https://grafana.com/) es una plataforma de código abierto para la observabilidad y el análisis de datos en tiempo real. Permite visualizar métricas provenientes de diversas fuentes, como bases de datos SQL y NoSQL, sistemas de monitoreo como Prometheus o InfluxDB, y plataformas en la nube. Su interfaz intuitiva facilita la creación de paneles interactivos y gráficos personalizados, lo que lo convierte en una herramienta esencial para la monitorización de infraestructuras, aplicaciones y servicios. Además, Grafana soporta alertas y consultas avanzadas, permitiendo a los usuarios tomar decisiones basadas en datos de manera eficiente.

Para lanzar *Grafana* sobre los contenedores que ya tenemos, crearemos un nuevo archivo, el cual hemos llamado [`docker-compose-grafana.yml`](resources/docker-compose-grafana.yml), donde además de la definición de los contenedores previos, hemos configurado *Grafana* en el puerto 3000:

docker-compose-grafana.yml

```
services:
  mariadb:
    image: mariadb:latest
    container_name: mdb
    ports:
      - 3306:3306
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=pruebas
      - MYSQL_USER=s8a
      - MYSQL_PASSWORD=s8a
    volumes:
      - mariabd_data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin
    container_name: phpma
    ports:
      - 8080:80
    environment:
      - PMA_HOST=mariadb
    depends_on:
      - mariadb

  grafana:
    image: grafana/grafana-oss
    container_name: grafana
    ports:
      - "3000:3000"
    volumes:
      - grafana_data:/var/lib/grafana

  volumes:
    mariabd_data:
    grafana_data:
```

Una vez creado el archivo, lanzamos el contenedor mediante:

```
docker compose -p mariadb-s8a -f docker-compose-grafana.yml up -d
```

Y ya podremos acceder a la página de login (<http://localhost:3000/>) con el usuario `admin` y contraseña `admin`, donde nos pedirá cambiar la contraseña. Una vez dentro, uno de los primeros pasos es añadir una fuente de datos (*data source*) de tipo *MySQL*. Ten en cuenta que en nombre del *host* debes configurar el nombre del contenedor: `mdb:3306`:

![](images/00grafana-mysql.png)

Configurando la fuente de datos en Grafana

## PostgreSQL

*PostgreSQL* es un SGBD relacional *open-source* que sigue un modelo cliente-servidor, soportando accesos concurrentes de múltiples usuarios. Está escrito en C y tiene soporte para todos los sistemas operativos, incluyendo su uso mediante *Docker*.

Por ello, necesitamos lanzar un contenedor con el servidor al cual nos conectaremos desde el cliente por línea de comandos `psql` o desde el cliente gráfico *PgAdmin*. Por ello, en el fichero de configuración [`docker-compose-postgres.yml`](resources/docker-compose-postgres.yml) de *Docker Compose* tenemos dos servicios:

docker-compose-postgres.yml

```
services:
  db:
    image: postgres:17
    container_name: pg
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=s8a
      - POSTGRES_PASSWORD=s8a
      - POSTGRES_DB=pruebas
    volumes:
      - pg-data:/var/lib/postgresql/data
  pgadmin:
    image: dpage/pgadmin4
    container_name: pgadmin
    ports:
      - "5050:80"
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@s8a.com
      PGADMIN_DEFAULT_PASSWORD: admin
    volumes:
      - pgadmin-data:/var/lib/pgadmin

volumes:
  pg-data:
  pgadmin-data:
```

Tras crear este archivo en nuestro sistema, podemos crear los contenedores mediante:

```
docker compose -p pg-s8a -f docker-compose-postgres.yml up -d
```

### Cliente `psql`

Recuerda arrancar el contenedor

No te olvides que debes arrancar el contenedor cada vez que quieras usarlo, ya sea mediante el botón *play* en *Docker Desktop*, o mediante `docker start <nombreContenedor>`:

```
docker start pg
```

Primero nos conectamos al contenedor (el cual en el archivo *docker-compose* hemos llamado `pg`):

```
docker exec -it pg bash
```

A continuación, mediante el cliente del SGBD, nos conectamos al servidor (al ser `localhost` no hace falta que lo indiquemos) pasándole el usuario (`-U s8a`) y luego la base de datos a la que nos queremos conectar (`pruebas`):

```
psql -U s8a pruebas
```

Obteniendo información de la versión instalada y en la última línea muestra que ha conectado con la bd `pruebas`:

```
root@6475b31d89f4:/# psql -U s8a pruebas
psql (17.5 (Debian 17.5-1.pgdg120+1))
Type "help" for help.

pruebas=#
```

Además de soportar sentencias SQL estándar, `psql` también viene con varios metacomandos que le permiten obtener información sobre la conexión actual, listar objetos de base de datos existentes, copiar datos de archivos externos y mucho más. Todos estos comandos comienzan con el símbolo de la barra invertida (`\`). Por ejemplo, si queremos obtener información de la conexión usaremos el comando `\conninfo`:

```
pruebas=# \conninfo
You are connected to database "pruebas" as user "s8a" via socket in "/var/run/postgresql" at port "5432".
```

Metacomandos

Mediante el metacomando `\?` podemos obtener una lista completa de todos los metacomandos soportados por `psql`. Para cerrar la lista generada y devolver el control al indicador `psql`, pulsa la letra `q`.

### PgAdmin

Una vez arrancados los contenedores, accederemos a <http://localhost:5050/> y tras introducir los datos del usuario administrador (`admin@s8a.com` / `admin`), veremos el interfaz de inicio de la herramienta de administración *PgAdmin*.

El siguiente paso es crear la conexión con el servidor. Para ello, creamos un nuevo servidor mediante la opción *Agregar un nuevo servidor* y en los datos de configuración, indicamos los mismos datos que hemos utilizado al definir el contenedor (en el nombre del servidor podemos poner el nombre del contenedor o su identificador `pg`, así como el usuario `s8a` y la contraseña `s8a`):

![](images/00pgadmin-new-server.png)

Conectando con el servidor en PgAdmin

Error - *role does not exists*

Si al crear la conexión al servidor recibís algún tipo de error similar a "rol inexistente", es probable que los volúmenes y las versiones de los contenedores no concuerden. Si es así, elimina los contenedores y los volúmenes, y vuelve a ejecutar el script de *Docker Compose*.

Una vez dentro, tendremos un cuadro de mandos para monitorizar el SGBD, así como poder navegar por las estructuras de la base de datos:

![](images/00pgadmin-estructura.png)

Estructura de una tabla en PgAdmin

AWS RDS

Además de utilizar ambos SGBD en local, podemos hacer uso de servicios en el cloud como AWS RDS.

## DBeaver

Además de utilizar los clientes propios de cada SGBD, así como herramientas web específicas, es muy común utilizar un cliente gráfico multisolución como *DBeaver*.

El primer paso es crear la conexión al SGBD, mediante la opción del menú y tras seleccionar el SGBD, indicaremos los datos de la conexión. En este caso, como ya no lo hacemos desde dentro del contenedor, el host siempre será `localhost`, y los usuarios, los indicados anteriormente.

![](images/00dbeaver.png)

Interfaz de DBeaver para PostgreSQL

## Redis

*Redis* es una solución NoSQL basada en un modelo de datos de clave-valor en memoria que se utiliza como base de datos de respuesta rápida o caché de aplicaciones. A partir de la versión 8 (mayo de 2025), incluye en el *core* funcionalidades que antes se distribuían como módulos separados (*JSON*, *búsqueda*, *series temporales*, estructuras probabilísticas y *vector sets*), por lo que ya no es necesario instalar la antigua imagen `redis/redis-stack` para acceder a ellas.

Aunque podemos instalar *Redis* en cualquier sistema operativo, en nuestro caso, vamos a centrarnos en hacerlo mediante un contenedor *Docker*.

Adiós a redis-stack

Si has visto en otros tutoriales las imágenes `redis/redis-stack` o `redis/redis-stack-server`, ten en cuenta que están **deprecadas** desde la salida de *Redis 8*: el mantenimiento de las versiones 6.2, 7.2 y 7.4 finaliza en diciembre de 2025. Para nuevas instalaciones, la imagen oficial recomendada es `redis:8` (o simplemente `redis:latest`).

Otra diferencia importante: en `redis-stack`, *RedisInsight* venía empaquetado en el puerto `8001`. Desde *Redis 8*, *RedisInsight* es un contenedor independiente (`redis/redisinsight`) que se sirve por defecto en el puerto `5540`.

De forma similar a como hicimos con *MariaDB* y *PostgreSQL*, vamos a definir los contenedores en un archivo *Docker Compose*, al que llamaremos [`docker-compose-redis.yml`](https://aitor-medrano.github.io/bd/resources/docker-compose-redis.yml), con dos servicios: el servidor de *Redis* y la interfaz gráfica [*RedisInsight*](https://redis.io/insight/):

docker-compose-redis.yml

```
services:
  redis:
    image: redis:8
    container_name: redis
    ports:
      - 6379:6379
    volumes:
      - redis_data:/data

  redisinsight:
    image: redis/redisinsight:latest
    container_name: redisinsight
    ports:
      - 5540:5540
    volumes:
      - redisinsight_data:/data
    depends_on:
      - redis

volumes:
  redis_data:
  redisinsight_data:
```

Para lanzar los contenedores ejecutaremos el siguiente comando:

```
docker compose -p redis-s8a -f docker-compose-redis.yml up -d
```

### Cliente `redis-cli`

Para conectarnos al cliente interactivo `redis-cli`, primero accedemos al contenedor y, dentro, lanzamos el cliente:

```
docker exec -it redis redis-cli
# 127.0.0.1:6379>
```

Una vez dentro del cliente, podemos comprobar la versión de *Redis* con la que estamos trabajando ejecutando `INFO server` o, de forma más concisa, con el comando `help`, que en su primera línea muestra la versión instalada:

```
127.0.0.1:6379> help
# redis-cli 8.6.2
# To get help about Redis commands type: ...
```

### RedisInsight

Si accedemos a <http://localhost:5540/> accederemos a la página de inicio de *RedisInsight*, donde tras aceptar la licencia, deberemos añadir nuestra base de datos de *Redis*. Como ambos contenedores están en la misma red de *Docker Compose*, en el campo *Host* indicaremos `redis` (el nombre del servicio) y en el puerto `6379`. Es decir, la URL completa de conexión es `redis://default@redis:6379`:

![](images/00redis-add-database.png)

Añadiendo una base de datos en Redis

Tras añadir la base de datos, *RedisInsight* nos permite explorar las claves, ejecutar comandos en su *Workbench* integrado y visualizar los datos en forma de árbol cuando utilizamos prefijos con `:` como separador (lo veremos en la unidad de *Redis*).

![](images/00redis-insight.png)

Redis Insight

### Redis cloud

Si no queremos instalar *Redis* en nuestro ordenador, podemos emplear *Redis cloud*, el cual ofrece de manera gratuita una instancia con 30MB de datos. Para ello, en la propia página de *Redis*, tras registrarnos, podremos crear una instancia.

![](images/00redis-cloud.png)

Redis Cloud

Una vez creada, obtendremos su información de acceso, con su *endpoint* público, al cual podemos conectarnos con el cliente Redis CLI o mediante el interfaz gráfico *RedisInsight* (en su caso, deberíamos también instalarlo como cliente en nuestro dispositivo).

![](images/00redis-cloud-s8a.png)

Conexión a Redis Cloud

## MongoDB

Desde <https://www.mongodb.com/try/download/community> podemos descargar la versión *Community* acorde a nuestro sistema operativo.

En vez de instalarlo como un servicio en nuestra máquina, a día de hoy, es mucho más cómodo hacer uso de contenedores *Docker* o utilizar una solución *cloud*.

### Docker

Para lanzar el contenedor de *Docker* al que llamaremos `bd-mongo` mediante el siguiente comando:

```
docker run -p 127.0.0.1:27017:27017 --name bd-mongo -d mongo
```

MongoDB y procesadores AVX

Si tenemos un procesador sin soporte para AVX, necesitamos instalar una versión inferior a la 5.0.

Así pues, podemos indicar la versión 4.4:

```
docker run -p 127.0.0.1:27017:27017 --name bd-mongo -d mongo:4.4
```

A continuación vamos a descargar el conjunto de datos ([sampledata.archive](https://atlas-education.s3.amazonaws.com/sampledata.archive)) que ofrece *MongoDB* a modo de prueba, el cual vamos a emplear a lo largo de las diferentes sesiones.

Volvemos al terminal de nuestro sistema y copiamos los datos desde nuestro sistema a la carpeta `/tmp` del contenedor:

```
docker cp sampledata.archive bd-mongo:/tmp
```

Posteriormente abrimos un terminal dentro de nuestro contenedor (o mediante *Attach Shell* en *VSCode*):

```
docker exec -it bd-mongo bash
```

Y finalmente, restauramos los datos mediante `mongorestore`:

```
mongorestore --archive=/tmp/sampledata.archive
```

Una vez cargados, nos informará que se han restaurado 433.281 documentos.

Por último, para acceder al cliente de *MongoDB* `mongosh`, ejecutamos el siguiente comando:

```
mongosh
# Current Mongosh Log ID: 69fcdbc860416d1c5444ba88
# Connecting to:          mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.8.2
# Using MongoDB:          8.2.7
# Using Mongosh:          2.8.2

# ...

test>
```

Independientemente de nuestro sistema operativo, por defecto, el demonio se lanza sobre el puerto 27017. Una vez instalado, si accedemos a <http://localhost:27017> podremos ver que nos indica cómo estamos intentando acceder mediante HTTP a *MongoDB* mediante el puerto reservado al *driver* nativo.

![MongoDB - Acceso al puerto 27017](images/00localhost27017.png)

Acceso al puerto 27017

### Mongo Atlas

Si, en cambio, preferimos una solución *cloud*, disponemos de [Mongo Atlas](https://www.mongodb.com/es/atlas), que nos ofrece de manera gratuita un clúster compartido de servidores con 3 nodos y 512 MB para datos. Si queremos una solución *serverless* o un servidor dedicado, ya tendremos que [pasar por caja](https://www.mongodb.com/pricing).

![MongoDB - Registro en Mongo Atlas](images/00mongoatlas-register.png)

Registro en Mongo Atlas

Para comenzar a utilizar *Mongo Atlas* el primer paso es [registrarnos](https://www.mongodb.com/cloud/atlas/register) y completar un cuestionario sobre nuestro uso. Tras ello:

1. Creamos el clúster de despliegue. En nuestro caso, hemos realizado el despliegue en AWS en la región de Paris (`eu-west-3`) y dejado el nombre por defecto, `Cluster 0`.

   ![MongoDB - Elección del clúster](images/00mongoatlas-cluster.png)

   Elección del clúster
2. Creamos un usuario/contraseña para autenticar nuestra conexión. En nuestro caso, hemos creado el usuario `iabd` con la contraseña `iabdiabd` (después la podemos modificar desde el menú *Security -> Database Access*):

   ![MongoDB - Configuración del usuario](images/00mongoatlas-usuario.png)

   Configuración del usuario

   En la misma pantalla, indicamos que permitimos las conexiones desde todas las direcciones IP (esta decisión sólo la tomamos por comodidad, para poder conectarnos desde casa y el centro) mediante la IP `0.0.0.0` (después podemos modificar la configuración desde el menú *Security -> Network Access*).
3. Una vez realizados los dos pasos anteriores, comenzará la creación del clúster, la cual puede tardar de 2 a 3 minutos.

   ![MongoDB - Dashboard del clúster](images/00mongoatlas-dashboard.png)

   Dashboard del clúster
4. A continuación, cargaremos los datos de ejemplo. Para ello, en el menú con los tres puntos (`...`), elegiremos la opción *Load Sample Dataset*. Una vez haya finalizado, podremos ver los datos cargados pulsando sobre el botón *Browse Collections*:

   ![MongoDB - Colecciones con los datos de prueba](images/00mongoatlas-colecciones.png)

   Colecciones con los datos de prueba

Conexión segura

Mediante `srv` se establece una conexión segura

Finalmente, para obtener la cadena de conexión, desde el *dashboard* del clúster con la opción *Connect* o desde la pestaña *Cmd Line Tools* del propio clúster, podremos obtener la [cadena de conexión](https://www.mongodb.com/docs/manual/reference/connection-string), que tendrá un formato similar a :

```
mongodb+srv://usuario:password@host/basededatos
```

En versiones anteriores, una herramienta de terceros bastante utilizada era [*RoboMongo*](http://robomongo.org) / *Robo3T* / [*Studio3T*](https://studio3t.com/) el cual extiende el shell y ofrece un IDE más amigable. A día de hoy, *MongoDB* tiene su propio IDE conocido como [MongoDB Compass](https://www.mongodb.com/es/products/compass).

### MongoDB Compass

En el curso nos vamos a centrar en el uso del *shell*, pero no está de más conocer las herramientas visuales que facilitan el trabajo con *MongoDB* en el día a día.

Una de ellas es [*MongoDB Compass*](https://www.mongodb.com/es/products/compass), que facilita la exploración y manipulación de los datos. De una manera flexible e intuitiva, *Compass* ofrece visualizaciones detalladas de los esquemas, métricas de rendimiento en tiempo real así como herramientas para la creación de consultas.

Existen tres versiones de *Compass*, una completa con todas las características, una de sólo lectura sin posibilidad de insertar, modificar o eliminar datos (perfecta para analítica de datos) y una última versión *isolated* que solo permite la conexión a una instancia local.

Una vez descargada e instalada la versión que nos interesa, tras crear la conexión a partir de la cadena de conexión (similar a `mongodb+srv://<usuario>:<contraseña>@cluster0.4hm7u8y.mongodb.net/test`), veremos en el menú de la izquierda todas las conexiones a servidores MongoDB almacenadas y las diferentes bases de datos de las respectivas conexiones:

![MongoDB - GUI de Mongo Compass](images/00mongocompass-init.png)

GUI de Mongo Compass

Si seleccionamos una base de datos concreta, y de ella, una colección en el menú de la izquierda, en el panel central tendremos una visualización de los datos contenidos, así como opciones para analizar su esquema, realizar consultas agregadas, editar los índices, etc... Además, podremos realizar consultas sobre los datos:

![MongoDB - Opciones desde una colección en MongoDBCompass](images/00mongocompass-coleccion.png)

Opciones desde una colección

mongosh en Compass

Tanto sobre el nombre de la conexión (dejando el ratón encima aparecerá un icono), como desde la parte superior derecha, podemos conectarnos desde un *shell* similar a `mongosh`.

[![Invítame a un café en ko-fi.com](https://storage.ko-fi.com/cdn/kofi2.png?v=3)](https://ko-fi.com/T6T8GWT9N "Invítame a un café en ko-fi.com")

Gracias por tu tiempo. Si quieres me puedes [invitar a un café en ko-fi](https://ko-fi.com/T6T8GWT9N).

¡Gracias por tu colaboración! Ayúdame a mejorar los apuntes enviándome un mail a [a.medrano@edu.gva.es](mailto:a.medrano@edu.gva.es) con tus comentarios.
