-- -- Extended analytics view for Northwind DB
-- CREATE VIEW IF NOT EXISTS OrderDetailsExtended AS
-- SELECT
--     od.OrderID,
--     o.OrderDate,
--     o.RequiredDate,
--     o.ShippedDate,
--     o.ShipRegion AS Region,
--     o.ShipCountry,
--     c.CustomerID,
--     c.CompanyName AS CustomerName,
--     c.ContactName AS Contact,
--     c.Region AS CustomerRegion,
--     p.ProductID,
--     p.ProductName,
--     cat.CategoryName,
--     s.SupplierID,
--     s.CompanyName AS SupplierName,
--     e.EmployeeID,
--     e.LastName || ', ' || e.FirstName AS EmployeeName,
--     sh.ShipperID,
--     sh.CompanyName AS ShipperName,
--     od.Quantity,
--     od.UnitPrice
--     od.Discount,
--     (od.UnitPrice * od.Quantity * (1 - od.Discount)) AS LineTotal
-- FROM order_details od
-- JOIN orders o       ON od.OrderID = o.OrderID
-- JOIN products p     ON od.ProductID = p.ProductID
-- JOIN categories cat ON p.CategoryID = cat.CategoryID
-- JOIN customers c    ON o.CustomerID = c.CustomerID
-- JOIN employees e    ON o.EmployeeID = e.EmployeeID
-- JOIN suppliers s    ON p.SupplierID = s.SupplierID
-- JOIN shippers sh    ON o.ShipVia = sh.ShipperID;



CREATE VIEW IF NOT EXISTS OrderDetailsExtended AS
SELECT CustomerID,
      CompanyName,
      Region
      FROM customers