CREATE DATABASE hotel_db;
USE hotel_db;

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100),
    item VARCHAR(100)
);


INSERT INTO orders (customer_name, item)
VALUES
('Ajay', 'Chicken Rice'),
('Arul', 'Idly'),
('Kumar', 'Pizza');

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(100)
);

INSERT INTO users (username, password)
VALUES("sriraman", "#Sriraman24"),
      ("thiru", "#Sriraman24");

ALTER TABLE users ADD failed_attempts INT DEFAULT 0;
ALTER TABLE users ADD is_locked BOOLEAN DEFAULT FALSE;

select*
from users
where username = "sriraman";

select*
from orders;

DELETE 
FROM orders
WHERE order_id =1
OR order_id = 2
OR order_id =3;

UPDATE users 
SET failed_attempts = 0, is_locked = FALSE
WHERE username = 'sriraman';



