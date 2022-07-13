create table IF NOT EXISTS HasBought (
ClientID INT NOT NULL REFERENCES Clients,
InvestmentID INT NOT NULL REFERENCES Investment,
Price DECIMAL(8,2),
DateBought DATE, CONSTRAINT hasbought_pk PRIMARY KEY(ClientID,InvestmentID),
Quantity INT
);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100224, 00054311203, 42000.00, '2022-01-10', 7);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100112, 00054311240, 64000.00, '2021-02-12', 8);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100251, 00054311299, 100000.0, '2021-04-17', 10);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100188, 00054311278, 36000.00, '2022-03-29', 3);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100188, 00054311248, 126028.00, '2021-10-17', 14);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100191, 00054311013, 45440.00, '2021-05-30', 71);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100199, 00054311208, 40000.00, '2021-09-21', 4);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100126, 00054311294, 45105.00, '2020-10-15', 5);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100206, 00054311201, 31500.00, '2021-08-14', 9);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100298, 00054311279, 24682.00, '2021-04-27', 2);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100235, 00054311291, 69748.00, '2021-05-05', 4);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100156, 00054311240, 64000.00, '2021-12-30', 8);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100139, 00054311295, 147712.00, '2022-02-17', 256);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100137, 00054311240, 80000.0, '2020-09-18', 10);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100249, 00054311299, 70000.0, '2021-11-18', 7);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100105, 00054311295, 19618.00, '2021-06-24', 34);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100150, 00054311299, 50000.00, '2022-02-08', 5);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100125, 00054311295, 14425.00, '2020-08-24', 25);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100123, 00054311291, 87185.00, '2021-05-28', 5);
insert into HasBought (ClientID, InvestmentID, Price, DateBought, Quantity) values (2100250, 00054311299, 60000.00, '2021-09-01', 6);
