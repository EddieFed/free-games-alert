# MySQL Schema for this project!
#
# Guide on how to replicate:
# https://stackoverflow.com/a/10769570

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS games;

CREATE TABLE games
(
    i INT AUTO_INCREMENT PRIMARY KEY,
    game VARCHAR(255) NULL,
    date DATE NULL
);

create table users
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(255) NOT NULL,
    carrier VARCHAR(255) NOT NULL,
    confirmed TINYINT(1) DEFAULT 0 NOT NULL
);

