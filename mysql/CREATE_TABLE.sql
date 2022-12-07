USE robottests;
CREATE TABLE executiontimes (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     starttime VARCHAR(255) NOT NULL,
     elapsedTime VARCHAR(255) NOT NULL,
     longname VARCHAR(255) NOT NULL,
     status VARCHAR(255) NOT NULL,
     PRIMARY KEY (id)
);