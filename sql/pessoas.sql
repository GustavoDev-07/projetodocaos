-- Active: 1770747795365@@172.16.116.96@3306@livraria
USE livraria;
SHOW TABLES;
 
CREATE TABLE pessoas(
    id INT PRIMARY KEY AUTO_INCREMENT,
    Nome VARCHAR (50) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Idade  DATE NOT NULL,
    Senha VARCHAR (50)
); 
SELECT
    id,
    nome,
    email,
    idade,
    senha 
FROM
    pessoas 