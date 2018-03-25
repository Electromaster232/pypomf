--
-- File generated with SQLiteStudio v3.1.1 on Sat Mar 24 21:00:14 2018
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: key
CREATE TABLE "key" (allowed_keys STRING PRIMARY KEY);

-- Table: uploads
CREATE TABLE uploads (id INTEGER PRIMARY KEY AUTOINCREMENT, token STRING, datetime STRING, filename STRING, fileext STRING);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
