CREATE TABLE notifications(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    date DATETIME NOT NULL,
    uuid varchar(50) NOT NULL,
    eventtype varchar(20) NOT NULL,
    eventdata varchar(500) NOT NULL
);

