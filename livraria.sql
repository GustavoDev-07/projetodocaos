CREATE USER 'bibliotecarios'@'%' IDENTIFIED BY '937651';
GRANT SELECT, INSERT, ALTER, DELETE, CREATE ON livraria.* TO 'bibliotecarios'@'%';