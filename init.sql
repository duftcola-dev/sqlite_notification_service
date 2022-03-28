CREATE TABLE user(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name varchar(30) NOT NULL,
    email varchar(40) NOT NULL 
);

INSERT INTO user (name,email) VALUES ("test","test@gmail.com");
INSERT INTO user (name,email) VALUES ("test1","test1@gmail.com");
INSERT INTO user (name,email) VALUES ("test2","test3@gmail.com");
INSERT INTO user (name,email) VALUES ("test3","test3@gmail.com");