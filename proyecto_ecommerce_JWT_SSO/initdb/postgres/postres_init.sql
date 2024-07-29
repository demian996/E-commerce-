-- Connect to the default 'postgres' database to perform database operations
\c postgres;

-- Drop the database if it exists
DROP DATABASE IF EXISTS ecommerce;

-- Create the database
CREATE DATABASE ecommerce;

-- Connect to the new database
\c ecommerce;

-- Create the logs_transacciones table
CREATE TABLE logs_transacciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL,
    accion TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into logs_transacciones
INSERT INTO logs_transacciones (usuario_id, accion) VALUES
(1, 'Usuario 1: Creó una nueva categoría'),
(2, 'Usuario 2: Editó el producto X'),
(3, 'Usuario 3: Eliminó el usuario Y');
