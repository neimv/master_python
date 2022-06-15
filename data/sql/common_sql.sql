CREATE DATABASE transporte;

CREATE TABLE pasajero (
	id SERIAL,
	nombre VARCHAR(100),
	direccion_residencia VARCHAR,
	fecha_nacimiento DATE,
	
	CONSTRAINT pasajero_pkey PRIMARY KEY (id)
);


CREATE TABLE bitacora_viaje (
	id SERIAL,
	id_viaje INTEGER,
	fecha DATE,
	
	CONSTRAINT bit_viaje_pkey PRIMARY KEY (id)
) PARTITION BY RANGE (fecha); -- hasta aqui se crea la tabla pero no se pueden insertar, por falta de la particion


CREATE TABLE bitacora_viaje201001 PARTITION bitacora_viaje
FOR VALUES RANGE FROM ('2010-01-01') TO ('2010-01-31');

CREATE ROLE usuario_consulta;

-- \dg -- usuario y atributos de los usuarios
-- member of para que un role pertenezca a otro role

ALTER ROLE usuario_consulta WITH LOGIN;
ALTER ROLE usuario_consulta WITH SUPERUSER;
ALTER ROLE usuario_consulta WITH PASSWORD '12345678';

CREATE ROLE {name} WITH {permissions};

GRANT INSERT, SELECT, UPDATE ON {schema}.{table} TO {user};

ALTER TABLE {schema}.{table}
	ADD CONSTRAINT {nombre_llave} FOREIGN KEY ({llave})
	REFERENCES {schema}.{tabla_destino} ({field}) MATCH SIMPLE
	ON UPDATE CASCADE
	ON DELETE CASCADE
	NOT VALID;


CREATE OR REPLACE VIEW {schema}.{view} AS {query}

CREATE MATERIALIZED VIEW {schema}.{view} AS {query} WITH NO DATA (para que se cree sin datos);

REFRESH MATERIALIZED VIEW {vista}

[ <<label>> ]
[ DECLARE declarations ]
BEGIN
	statements
END [ label ];

-- ejemplo 
BEGIN
	FOR rec IN SELECT * FROM {table} LOOP
		RAISE NOTICE '%', rec.{field};
	END LOOP;
END

CREATE OR REPLACE FUNCTION {name}()
	RETURNS {void|type}
AS $$ { codigo RETURN {value}} $$
LANGUAJE PLPGSQL; -- se pueden usar otros lenguajes

CREATE OR REPLACE FUNCTION {name}()
	RETURNS TRIGGER
AS $$ { codigo RETURN {OLD|NEW} } $$
LANGUAJE PLPGSQL;

CREATE TRIGGER {nombre}
AFTER {action} ON {table}
FOR EACH ROW
EXECUTE PROCEDURE {procedure}();


-- data science
SELECT MAX(ultima_actualizacion) AS fecha_ultima_actualizacion,
    clasificacion,
    COUNT(*) AS cantidad_peliculas
FROM peliculas
WHERE duracion_renta > 3
GROUP BY clasificacion, ultima_actualizacion
ORDER BY fecha_ultima_actualizacion


CREATE OR REPLACE PROCEDURE test_drpcreate_procedure()
LANGUAGE SQL
AS $$
    DROP TABLE IF EXISTS aaa;
    CREATE TABLE aaa (bbb CHAR(5) CONSTRAINT firstkey PRIMARY KEY);
$$;

CALL test_drpcreate_procedure();


CREATE OR REPLACE FUNCTION test_dropcreate_function()
RETURNS VOID
LANGUAGE plpgsql
AS $$
    BEGIN
        DROP TABLE IF EXISTS aaa;
        CREATE TABLE aaa (bbb CHAR(5) CONSTRAINT firstkey PRIMARY KEY, ccc CHAR(5));
        DROP TABLE IF EXISTS aaab;
        CREATE TABLE aaab (bbba CHAR(5) CONSTRAINT firstkey_b PRIMARY KEY, ccca CHAR(5));
    END
$$

SELECT test_dropcreate_function();


CREATE OR REPLACE FUNCTION count_total_movies()
RETURNS int
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN COUNT(*) FROM peliculas;
END
$$

SELECT count_total_movies();


CREATE OR REPLACE FUNCTION duplicate_records()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
   INSERT INTO aaab(bbba, ccca)
   VALUES (NEW.bbb, NEW.ccc);
   
   RETURN NEW;
END
$$

CREATE TRIGGER aaa_changes
    BEFORE INSERT
    ON aaa
    FOR EACH ROW
    EXECUTE PROCEDURE duplicate_records();
    
    
INSERT INTO aaa
VALUES ('abcde', 'efghi');

SELECT * FROM aaa;
SELECT * FROM aaab;

CREATE OR REPLACE FUNCTION movies_stats()
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    total_rated_r REAL := 0.0;
    total_larger_than_100 REAL := 0.0;
    total_published_2006 REAL := 0.0;
    average_duration REAL := 0.0;
    average_rental_price REAL := 0.0;
BEGIN
    total_rated_r := COUNT(*) FROM peliculas WHERE clasificacion = 'R';
    total_larger_than_100 := COUNT(*) FROM peliculas WHERE duracion > 100;
    total_published_2006 := COUNT(*) FROM peliculas WHERE anio_publicacion = 2006;

    average_duration := AVG(duracion) FROM peliculas;
    average_rental_price := AVG(precio_renta) FROM peliculas;

    TRUNCATE TABLE peliculas_estadisticas;
    
    INSERT INTO peliculas_estadisticas (tipo_estadistica, total)
    VALUES
        ('Peliculas con clasificacion R', total_rated_r),
        ('Peliculas de mas de 100 min', total_larger_than_100),
        ('Peliculas publicadas en 2006', total_published_2006),
        ('Promedio de duracion en minutos', average_duration),
        ('Precio promedio de renta', average_rental_price);
END
$$

SELECT movies_stats();
SELECT * FROM peliculas_estadisticas;


CREATE TYPE humor AS ENUM ('triste', 'normal', 'feliz');

CREATE TABLE persona_prueba_2 (
    nombre TEXT,
    humor_actual humor
);

INSERT INTO persona_prueba_2 VALUES ('kiubos', 'triste');


SELECT titulo, MAX(precio_renta)
FROM peliculas
GROUP BY titulo;

SELECT SUM(precio_renta)
FROM peliculas;

SELECT clasificacion, COUNT(*) AS total_clasificacion
FROM peliculas
GROUP BY clasificacion;

SELECT AVG(precio_renta)
FROM peliculas;

SELECT clasificacion, AVG(precio_renta) AS precio_promedio
FROM peliculas
GROUP BY clasificacion
ORDER BY precio_promedio DESC;

SELECT clasificacion, AVG(duracion) AS duracion_promedio
FROM peliculas
GROUP BY clasificacion
ORDER BY duracion_promedio DESC;

SELECT clasificacion, AVG(duracion_renta) AS duracion_renta_promedio
FROM peliculas
GROUP BY clasificacion
ORDER BY duracion_renta_promedio DESC;


CREATE TABLE ordenes (
    id SERIAL NOT NULL PRIMARY KEY,
    info JSON NOT NULL
);

INSERT INTO ordenes (info)
VALUES
    (
        '{"cliente": "neimv zatara", "items": {"producto": "biberon", "cantidad": "24"}}'
    ),
    (
        '{"cliente": "neyik dumah", "items": {"producto": "carro de juguete", "cantidad": "1"}}'
    ),
    (
        '{"cliente": "yo", "items": {"producto": "tren de juguete", "cantidad": "2"}}'
    );

SELECT *
FROM ordenes;

SELECT info ->> 'cliente' AS cliente
FROM ordenes;

SELECT info ->> 'cliente' AS cliente
FROM ordenes
WHERE info -> 'items' ->> 'producto' = 'biberon'


SELECT
    MIN(
        CAST(
            info -> 'items' ->> 'cantidad' AS INTEGER
        )
    ),
    MAX(
        CAST(
            info -> 'items' ->> 'cantidad' AS INTEGER
        )
    ),
    SUM(
        CAST(
            info -> 'items' ->> 'cantidad' AS INTEGER
        )
    ),
    AVG(
        CAST(
            info -> 'items' ->> 'cantidad' AS INTEGER
        )
    )
FROM ordenes;


WITH RECURSIVE tabla_recursiva(n) AS (
    VALUES(1)
    UNION ALL
    SELECT n + 1 FROM tabla_recursiva WHERE n < 100
) SELECT SUM(n) FROM tabla_recursiva;


SELECT peliculas.pelicula_id AS id
    , peliculas.titulo
    , COUNT(*) AS numero_rentas
    , ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS lugar
FROM rentas
INNER JOIN inventarios
    ON rentas.inventario_id = inventarios.inventario_id
INNER JOIN peliculas
    ON inventarios.pelicula_id = peliculas.pelicula_id
GROUP BY peliculas.pelicula_id
ORDER BY numero_rentas DESC
LIMIT 10;


SELECT peliculas.pelicula_id
    , tipos_cambio.tipo_cambio_id
    , tipos_cambio.cambio_usd * peliculas.precio_renta AS precio_mxn
FROM peliculas, tipos_cambio
WHERE tipos_cambio.codigo = 'MXN';


CREATE TRIGGER trigger_update_tipos_cambio
    AFTER INSERT OR UPDATE
    ON public.peliculas
    FOR EACH ROW
    EXECUTE PROCEDURE public.precio_peliculas_tipo_cambio();


SELECT peliculas.pelicula_id AS id
    , peliculas.titulo
    , COUNT(*) AS numero_rentas
    , DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS lugar
    , PERCENT_RANK() OVER (ORDER BY COUNT(*) DESC) AS lugar_p
    , ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) AS lugar_n
FROM rentas
INNER JOIN inventarios
    ON rentas.inventario_id = inventarios.inventario_id
INNER JOIN peliculas
    ON inventarios.pelicula_id = peliculas.pelicula_id
GROUP BY peliculas.pelicula_id
ORDER BY numero_rentas DESC;


SELECT c.ciudad_id
    , c.ciudad
    , COUNT(*) AS rentas_por_ciudad
FROM ciudades AS c
INNER JOIN direcciones AS d
    ON c.ciudad_id = d.ciudad_id
INNER JOIN tiendas AS t
    ON t.direccion_id = d.direccion_id
INNER JOIN inventarios AS i
    ON i.tienda_id = t.tienda_id
INNER JOIN rentas as r
    ON i.inventario_id = r.inventario_id
GROUP BY c.ciudad_id;


SELECT DATE_PART('year', r.fecha_renta) AS anio
    , DATE_PART('month', r.fecha_renta) AS mes
    , p.titulo
    , COUNT(*) AS numero_rentas
FROM rentas AS r
INNER JOIN inventarios as i
    ON r.inventario_id = i.inventario_id
INNER JOIN peliculas AS p
    ON p.pelicula_id = i.pelicula_id
GROUP BY anio, mes, p.titulo
ORDER BY titulo;


