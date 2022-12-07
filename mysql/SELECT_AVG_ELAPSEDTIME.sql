USE robottests;
SELECT AVG(elapsedTime) FROM (SELECT elapsedTime FROM executiontimes WHERE longname = 'Testcases.Example-Tests.Invalid Login.Invalid Username' ORDER BY ID DESC LIMIT 2) AS TEMP;