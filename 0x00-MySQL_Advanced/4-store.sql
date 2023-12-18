-- SQL script that creates a trigger that decreases
-- the quantity of an item after adding a new order.

-- Sets a custom delimiter
DELIMITER |

CREATE TRIGGER decrease_item_qty AFTER INSERT
ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END |

-- Restores defualt delimiter
DELIMITER ;
