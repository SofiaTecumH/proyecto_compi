CREATE TABLE usuarios (
id INT PRIMARY KEY,
    nombre VARCHAR(50),
    edad INT,
    correo VARCHAR(100)
);

INSERT INTO usuarios (id, nombre, edad, correo) VALUES (1, 'Ana', 25, 'ana@example.com');
INSERT INTO usuarios (id, nombre, edad, correo) VALUES (2, 'Luis', 30, 'luis@example.com');
INSERT INTO usuarios (id, nombre, edad, correo) VALUES (3, 'Carlos', 22, 'carlos@example.com');

SELECT * FROM usuarios;

UPDATE usuarios SET edad = 26 WHERE id = 1;

DELETE FROM usuarios WHERE id = 3;