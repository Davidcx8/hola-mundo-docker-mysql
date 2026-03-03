CREATE DATABASE IF NOT EXISTS hola_db;
USE hola_db;

CREATE TABLE IF NOT EXISTS visitas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  mensaje VARCHAR(255) NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserción inicial (opcional)
INSERT INTO visitas (mensaje) VALUES ('Pedro'),('David'),('Cristian');