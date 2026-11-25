-- 1. total de vendas por mês

SELECT strftime('%Y-%m', data_pedido) AS mes,
       ROUND(SUM(valor_itens), 2) AS total_vendas
FROM pedidos
GROUP BY mes
ORDER BY mes;


-- teste da consulta 1) a soma geral da tabela
SELECT ROUND(SUM(valor_itens), 2) AS soma_geral FROM pedidos;

-- ...tem que ser igual à soma dos totais mensais
SELECT ROUND(SUM(total_vendas), 2) AS soma_dos_meses
FROM (
    SELECT strftime('%Y-%m', data_pedido) AS mes,
           SUM(valor_itens) AS total_vendas
    FROM pedidos
    GROUP BY mes
);


-- 2. quantidade de pedidos por estado
SELECT clientes.estado AS estado,
       COUNT(*) AS quantidade_pedidos
FROM pedidos
JOIN clientes ON clientes.id = pedidos.cliente_id
GROUP BY clientes.estado
ORDER BY quantidade_pedidos DESC;