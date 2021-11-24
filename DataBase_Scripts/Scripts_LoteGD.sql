## Seleciona USINAS enviadas hoje
SELECT * FROM USINAS_CLARO WHERE `data` = CURDATE() ORDER BY `data` DESC;
## Seleciona FATURAS enviadas hoje
SELECT * FROM USINAS_CLARO_LOG WHERE Data_Envio > CURDATE() ORDER BY Data_Envio DESC;