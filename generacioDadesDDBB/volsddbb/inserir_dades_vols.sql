-- Carrega de dades per a les taules gate, airline, flight, flight_gate i ticket

-- Substitueix '/ruta/completa/' per la ruta real dels fitxers al teu sistema

LOAD DATA LOCAL INFILE '/ruta/completa/gate.csv'
INTO TABLE gate
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, terminal, boarding_zone);

LOAD DATA LOCAL INFILE '/ruta/completa/taula_airline.csv'
INTO TABLE airline
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, name, image);

LOAD DATA LOCAL INFILE '/ruta/completa/taula_flight.csv'
INTO TABLE flight
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, code, origin, destination, date, time, airline_id);

LOAD DATA LOCAL INFILE '/ruta/completa/taula_flight_gate.csv'
INTO TABLE flight_gate
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(flight_id, gate_id);

LOAD DATA LOCAL INFILE '/ruta/completa/taula_ticket.csv'
INTO TABLE ticket
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(id, seat, user_id, flight_id);
