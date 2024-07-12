CREATE DATABASE IF NOT EXISTS ecommerce;

USE ecommerce;

CREATE TABLE IF NOT EXISTS categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10, 2) NOT NULL,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'administrador') NOT NULL
);

INSERT INTO categorias (nombre, descripcion) VALUES ('Electrónica', 'Artículos de electrónica');
INSERT INTO productos (nombre, descripcion, precio, categoria_id) VALUES ('Laptop', 'Una laptop nueva', 1000.00, 1);
INSERT INTO usuarios (nombre, email, contrasena, rol) VALUES ('Admin', 'admin@example.com', 'scrypt:32768:8:1$W7Ot0YhiZ7S6gS5d$2212e4f5373098a4f6d94f60e9410af5dc2085dc9bc854256fa71197bd46825d7fa9dfe34898cd33a16100ac25cee95a59047ab6170b57305391bc8a54fc19c1', 'administrador');
