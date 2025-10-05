Modelo do Banco de Dados Cafeteria

Tabela produtos: Armazena as informações de cada item que a cafeteria vende.

id: Identificador único para cada produto (Chave Primária).

nome: O nome do produto (ex: "Café Expresso").

descricao: Um breve texto sobre o produto.

preco: O valor do produto, usando um tipo de dado ideal para moeda (DECIMAL).

Tabela pedidos: Armazena cada pedido feito por um cliente.

id: Identificador único para cada pedido (Chave Primária).

produto_id: A qual produto este pedido se refere (Chave Estrangeira, ligada à tabela produtos).

quantidade: Quantas unidades do produto foram pedidas.

preco_total: O valor total do pedido (quantidade * preço do produto + taxa).

tipo_entrega: Se o pedido é para 'retirada' ou 'entrega'.

endereco_entrega: O endereço, caso o tipo seja 'entrega'.

data_pedido: A data e hora em que o pedido foi feito.

Script: schema.sql

DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS produtos;

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER,
    quantidade INTEGER NOT NULL DEFAULT 1,
    preco_total DECIMAL(10, 2) NOT NULL,
    tipo_entrega TEXT NOT NULL CHECK(tipo_entrega IN ('retirada', 'entrega')),
    endereco_entrega TEXT,
    data_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT
);

INSERT INTO produtos (nome, descricao, preco) VALUES
('Café Comum', 'Café coado tradicional, feito com grãos selecionados.', 4.00),
('Café Expresso', 'Café forte e encorpado, extraído sob alta pressão.', 6.00),
('Achocolatado', 'Leite vaporizado com um toque de chocolate cremoso.', 8.00);

INSERT INTO pedidos (produto_id, quantidade, preco_total, tipo_entrega, endereco_entrega) VALUES
(2, 1, 6.00, 'retirada', NULL),
(3, 2, 22.00, 'entrega', 'Rua das Flores, 123, Centro'),
(1, 1, 10.00, 'entrega', 'Av. Principal, 456, Bairro Novo');
UPDATE produtos
SET preco = 7.50
WHERE nome = 'Café Expresso';

DELETE FROM produtos
WHERE id = 3;

SELECT * FROM produtos;

SELECT * FROM pedidos
WHERE tipo_entrega = 'entrega';

SELECT
    p.nome,
    ped.quantidade,
    ped.endereco_entrega,
    ped.preco_total
FROM pedidos ped
JOIN produtos p ON ped.produto_id = p.id
WHERE ped.tipo_entrega = 'entrega';

