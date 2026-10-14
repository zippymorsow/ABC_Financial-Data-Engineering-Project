CREATE DATABASE ecom_db;

-- ===================================================================
-- START: ONE TIME SET UP
-- ===================================================================

-- 1. CREATE GLOBAL SERVER ROLE (Acts as the instance-level template)
-- In MSSQL, custom groups at the server level are called "Server Roles"
IF NOT EXISTS (SELECT * FROM sys.server_principals WHERE name = 'db_group_admin' AND type = 'R')
BEGIN
    CREATE SERVER ROLE db_group_admin;
END;

-- -------------------------------------------------------------------
-- FOR ecom_db
-- -------------------------------------------------------------------
USE ecom_db;

-- A. Create a Database Role inside this database to map to our Server Role later
IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = 'db_database_admin' AND type = 'R')
BEGIN
    CREATE ROLE db_database_admin;
END;

-- B. Grant absolute full administrative access (db_owner equivalent)
ALTER ROLE db_owner ADD MEMBER db_database_admin;

-- ===================================================================
-- END: ONE TIME SET UP
-- ===================================================================


-- ===================================================================
-- START: EXECUTE FOR EACH NEW USER
-- ===================================================================

USE master;

-- 1. CREATE SERVER-LEVEL LOGIN WITH PASSWORD
CREATE LOGIN admin_abc_financial WITH PASSWORD = 'xxxxxxsome paassword'; --please see .env to check correct password

-- 2. CREATE DATABASE-LEVEL USERS ASSOCIATING WITH THE LOGIN
-- For ecom_db
USE ecom_db;
CREATE USER admin_abc_financial FOR LOGIN admin_abc_financial;
ALTER ROLE db_database_admin ADD MEMBER admin_abc_financial; -- Bind to local database group

-- 3. ASSIGN THE GLOBAL ROLE TO THE LOGIN
-- This links the server identity to your master custom server role tracking
ALTER SERVER ROLE db_group_admin ADD MEMBER admin_abc_financial;

-- ===================================================================
-- END: EXECUTE FOR EACH NEW USER
-- ===================================================================