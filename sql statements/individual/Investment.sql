create table IF NOT EXISTS Investment (
	IID INT PRIMARY KEY,
	Type VARCHAR(50),
	Name VARCHAR(50),
	Risk_Assessment INT,
    Price DECIMAL(6,2)
);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311203, 'Medical Specialities', 'AET', 8, 6000.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311201, 'Railroads', 'RAIL', 33, 3500.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311240, 'Computer Software: Programming, Data Processing', 'MOXC', 35, 8000.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311278, 'Index Funds', 'VCLT', 91, 12000.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311294, 'Cryptocurrency', 'Bitcoin', 42, 9021.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311299, 'Cryptocurrency', 'Dogecoin', 64, 10000.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311248, 'Automotive Aftermarket', 'WMAR', 64, 9002.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311279, 'Diversified Commercial Services', 'CAI', 33, 12341.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311291, 'Electric Utilities: Central', 'MGEE', 89, 17437.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311295, 'Advertising', 'MDCA', 5, 577.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311208, 'Index Funds', 'Fidelity ZERO Large Cap Index (FNILX)', 12, 1641.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311280, 'Computer Software: Programming, Data Processing', 'TUL', 15, 7624.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311013, 'Medical Specialities', 'pHarmA', 8, 640.00);
insert into Investment (IID, Type, Name, Risk_Assessment, Price) values (00054311694, 'Cryptocurrency', 'Coinbase', 87, 15079.00);




