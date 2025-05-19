CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sku VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE product_categories (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    sale_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE inventory (
    product_id INTEGER PRIMARY KEY,
    stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE inventory_transactions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity_change INTEGER NOT NULL,
    previous_stock_quantity INTEGER NOT NULL CHECK (previous_stock_quantity >= 0),
    new_stock_quantity INTEGER NOT NULL CHECK (new_stock_quantity >= 0),
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('restock', 'sale', 'adjustment')),
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);


-- Sales related indexes
CREATE INDEX idx_sales_product_id ON sales(product_id);
CREATE INDEX idx_sales_sale_date ON sales(sale_date);

-- Product Categories table (for sales by category analysis)
CREATE INDEX idx_product_categories_category_id ON product_categories(category_id);

-- Inventory related indexes
CREATE INDEX idx_inventory_product_id ON inventory(product_id);
CREATE INDEX idx_inventory_transactions_product_id ON inventory_transactions(product_id);
CREATE INDEX idx_inventory_transactions_transaction_date ON inventory_transactions(transaction_date);

-- Inserting products
INSERT INTO products (name, sku, description, price)
VALUES 
    ('Laptop', 'SKU12345', 'High-performance laptop for work and gaming', 1500.00),
    ('Smartphone', 'SKU67890', 'Latest model with high-end specifications', 800.00),
    ('Tablet', 'SKU11223', 'Portable tablet with a 10-inch display', 300.00),
    ('Headphones', 'SKU44556', 'Noise-cancelling over-ear headphones', 120.00),
    ('Smartwatch', 'SKU78901', 'Fitness smartwatch with heart rate monitoring', 200.00);
	
-- Inserting categories
INSERT INTO categories (name, description)
VALUES 
    ('Electronics', 'Devices and gadgets including computers, phones, etc.'),
    ('Wearables', 'Smartwatches, fitness trackers, etc.'),
    ('Audio', 'Headphones, speakers, and related accessories'),
    ('Computing', 'Laptops, tablets, and accessories');

-- Associating products with categories
INSERT INTO product_categories (product_id, category_id)
VALUES
    (1, 4),  -- Laptop belongs to Computing
    (2, 1),  -- Smartphone belongs to Electronics
    (3, 4),  -- Tablet belongs to Computing
    (4, 3),  -- Headphones belongs to Audio
    (5, 2);  -- Smartwatch belongs to Wearables

-- Inserting sales
INSERT INTO sales (product_id, quantity, total_amount, sale_date)
VALUES
    (1, 2, 3000.00, '2025-05-01 10:00:00'),
    (2, 5, 4000.00, '2025-05-02 11:30:00'),
    (3, 3, 900.00, '2025-05-03 09:00:00'),
    (4, 1, 120.00, '2025-05-04 15:45:00'),
    (5, 2, 400.00, '2025-05-05 13:30:00');

-- Inserting inventory data
INSERT INTO inventory (product_id, stock_quantity)
VALUES
    (1, 50),  -- 50 units of Laptop
    (2, 100), -- 100 units of Smartphone
    (3, 30),  -- 30 units of Tablet
    (4, 75),  -- 75 units of Headphones
    (5, 60);  -- 60 units of Smartwatch

-- Inserting inventory transaction data
INSERT INTO inventory_transactions (product_id, quantity_change, previous_stock_quantity, new_stock_quantity, transaction_type, transaction_date)
VALUES
    (1, -2, 50, 48, 'sale', '2025-05-01 10:00:00'),  -- 2 laptops sold
    (2, -5, 100, 95, 'sale', '2025-05-02 11:30:00'),  -- 5 smartphones sold
    (3, -3, 30, 27, 'sale', '2025-05-03 09:00:00'),  -- 3 tablets sold
    (4, -1, 75, 74, 'sale', '2025-05-04 15:45:00'),  -- 1 headphone sold
    (5, -2, 60, 58, 'sale', '2025-05-05 13:30:00');  -- 2 smartwatches sold
/*
Explanation of Data:
Products: 5 different products are added (Laptop, Smartphone, Tablet, Headphones, and Smartwatch) with their unique SKU and prices.

Categories: Four categories are added (Electronics, Wearables, Audio, and Computing), and products are linked to them using the product_categories table.

Sales: 5 sales records are created, each representing a sale of some quantity of a product on a specific date.

Inventory: Stock quantities for each product are inserted, representing the initial inventory.

Inventory Transactions: The inventory_transactions table records the changes in stock due to sales, showing how inventory decreases when a product is sold.
*/