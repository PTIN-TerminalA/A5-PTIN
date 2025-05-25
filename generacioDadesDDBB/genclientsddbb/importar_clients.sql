-- Canvia la ruta per la que tinguis
LOAD DATA LOCAL INFILE '/ruta/completa/taula_user.csv'
INTO TABLE user
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name, dni, email, password, usertype);

-- Canvia la ruta per la que tinguis
LOAD DATA LOCAL INFILE '/ruta/completa/taula_regular.csv'
INTO TABLE regular
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, birth_date, phone_num, identity);

-- Canvia la ruta per la que tinguis
LOAD DATA LOCAL INFILE '/ruta/completa/taula_gender.csv'
INTO TABLE gender
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(identity);