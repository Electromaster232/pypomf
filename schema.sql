--
-- File generated with SQLiteStudio v3.1.1 on Sun Mar 25 17:28:18 2018
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: key
CREATE TABLE "key" (allowed_keys STRING PRIMARY KEY, email STRING, authtoken STRING, ENABLED STRING);

-- Table: uploads
CREATE TABLE uploads (id INTEGER PRIMARY KEY AUTOINCREMENT, token STRING, datetime STRING, filename STRING, fileext STRING);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
