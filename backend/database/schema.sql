-- Crear base de datos
CREATE DATABASE IF NOT EXISTS opticstream;
USE opticstream;

-- Tabla de sesiones/streams de detección
CREATE TABLE IF NOT EXISTS streams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    fuente VARCHAR(255) NOT NULL,
    inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    fin DATETIME NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de detecciones (cada frame con cambios)
CREATE TABLE IF NOT EXISTS detecciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    stream_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_objetos INT DEFAULT 0,
    FOREIGN KEY (stream_id) REFERENCES streams(id) ON DELETE CASCADE
);

-- Tabla de objetos detectados
CREATE TABLE IF NOT EXISTS objetos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    deteccion_id INT NOT NULL,
    track_id INT NULL,
    class_id INT NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    FOREIGN KEY (deteccion_id) REFERENCES detecciones(id) ON DELETE CASCADE
);

-- Índices para mejorar consultas
CREATE INDEX idx_detecciones_stream ON detecciones(stream_id);
CREATE INDEX idx_detecciones_timestamp ON detecciones(timestamp);
CREATE INDEX idx_objetos_deteccion ON objetos(deteccion_id);
CREATE INDEX idx_objetos_class ON objetos(class_name);
