CREATE DATABASE SEARCH_ENGINE;
use SEARCH_ENGINE;

CREATE TABLE web_pages (
    ID int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Link nvarchar(21000) NOT NULL,
    Content mediumtext,
	Visited bool,
    Indexed bool,
	LastVisited date,
	Frequecy int,
    Popularity int
);

CREATE TABLE words (
	word nvarchar(100) NOT NULL,
    L_ID int NOT NULL REFERENCES web_pages(ID) ON DELETE  CASCADE,
    TF int,
    No_Titles int,
    No_Headers int,
    No_Others int,
    PRIMARY KEY(word,L_ID)
);

CREATE TABLE phrase (
	word nvarchar(100) NOT NULL REFERENCES words(word) ON DELETE  CASCADE,
    L_ID int NOT NULL REFERENCES web_pages(ID) ON DELETE  CASCADE,
    Pos int,
    W_Type nvarchar(100),
	PRIMARY KEY(word,L_ID,pos,W_Type)
);