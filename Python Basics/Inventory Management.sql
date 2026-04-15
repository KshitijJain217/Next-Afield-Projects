CREATE DATABASE inventory_db;


CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price DECIMAL(10,2),
    quantity INT
);

INSERT INTO products (product_name, category, price, quantity) VALUES
('Laptop', 'Electronics', 55000, 10),
('Mouse', 'Electronics', 500, 50),
('Keyboard', 'Electronics', 1500, 30),
('Chair', 'Furniture', 3000, 20),
('Table', 'Furniture', 7000, 15);

SELECT * FROM products;

UPDATE products
SET price = 52000
WHERE product_name = 'Laptop';

UPDATE products
SET quantity = quantity + 10
WHERE product_name = 'Mouse';

UPDATE products
SET quantity = quantity + 10
WHERE product_name = 'Mouse';


SELECT * FROM products
ORDER BY price ASC;

SELECT * FROM products
ORDER BY quantity DESC;


SELECT category, COUNT(*) AS total_items
FROM products
GROUP BY category;

SELECT category, AVG(price) AS avg_price
FROM products
GROUP BY category;


SELECT * FROM products
WHERE quantity < 20;

SELECT product_name, (price * quantity) AS total_value
FROM products;