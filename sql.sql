CREATE DATABASE gerenciador;
USE gerenciador;

CREATE TABLE cargos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    cargo_id INT NOT NULL,
    FOREIGN KEY (cargo_id) REFERENCES cargos(id)
);

CREATE TABLE materiais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    imagem VARCHAR(255)
);

CREATE TABLE espessuras_materiais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    material_id INT,
    espessura_mm INT CHECK (espessura_mm IN (15, 18, 25, 50)),
    FOREIGN KEY (material_id) REFERENCES materiais(id) ON DELETE CASCADE
);


CREATE TABLE mobiliario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    imagem VARCHAR(255)
);

CREATE TABLE projetos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_cliente VARCHAR(100) NOT NULL,
    nome_arquiteto VARCHAR(100) NOT NULL
);

CREATE TABLE ambientes_projeto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projeto_id INT,
    nome_ambiente VARCHAR(100),
    usuario_id INT,
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE TABLE equipe_projeto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    projeto_id INT,
    usuario_id INT,
    cargo VARCHAR(100),
    FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE ambientes_mobiliario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ambiente_id INT,
    mobiliario_id INT,
    quantidade INT DEFAULT 1,
    FOREIGN KEY (ambiente_id) REFERENCES ambientes_projeto(id) ON DELETE CASCADE,
    FOREIGN KEY (mobiliario_id) REFERENCES mobiliario(id) ON DELETE CASCADE
);

CREATE TABLE ambientes_materiais (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ambiente_id INT,
    material_id INT,
    espessura_mm INT CHECK (espessura_mm IN (15, 18, 25, 50)),
    FOREIGN KEY (ambiente_id) REFERENCES ambientes_projeto(id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES materiais(id) ON DELETE CASCADE
);

INSERT INTO cargos (nome) VALUES
('consultor'),
('projetista'),
('tecnico'),
('financeiro');

INSERT INTO usuarios (nome, senha, cargo_id) VALUES
('Ana Consultora', 'senha123', 1),
('Bruno Projetista', 'senha123', 2),
('Carlos Técnico', 'senha123', 3),
('Daniela Financeira', 'senha123', 4);

INSERT INTO materiais (nome, imagem) VALUES
('MDF Branco', 'mdf_branco.jpg'),
('MDF Preto', 'mdf_preto.jpg'),
('Compensado Naval', 'compensado_naval.jpg'),
('Aglomerado Cru', 'aglomerado_cru.jpg'),
('Madeira Maciça', 'madeira_macica.jpg'),
('MDF Cinza', 'mdf_cinza.jpg'),
('MDF Texturizado', 'mdf_texturizado.jpg'),
('MDP Branco', 'mdp_branco.jpg'),
('MDF Carvalho', 'mdf_carvalho.jpg'),
('Compensado Plastificado', 'compensado_plastificado.jpg');

-- MDF Branco (15, 18, 25)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(1, 15), (1, 18), (1, 25);

-- MDF Preto (15, 18)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(2, 15), (2, 18);

-- Compensado Naval (18, 25)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(3, 18), (3, 25);

-- Aglomerado Cru (15)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(4, 15);

-- Madeira Maciça (18, 25, 50)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(5, 18), (5, 25), (5, 50);

-- MDF Cinza (15, 18)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(6, 15), (6, 18);

-- MDF Texturizado (25)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(7, 25);

-- MDP Branco (15, 18, 25)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(8, 15), (8, 18), (8, 25);

-- MDF Carvalho (18)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(9, 18);

-- Compensado Plastificado (25)
INSERT INTO espessuras_materiais (material_id, espessura_mm) VALUES
(10, 25);

INSERT INTO mobiliario (nome, imagem) VALUES
('Armário Aéreo', 'armario_aereo.jpg'),
('Balcão de Pia', 'balcao_pia.jpg'),
('Estante Modular', 'estante_modular.jpg'),
('Mesa de Escritório', 'mesa_escritorio.jpg'),
('Prateleira Simples', 'prateleira_simples.jpg'),
('Gabinete de Banheiro', 'gabinete_banheiro.jpg'),
('Roupeiro 3 Portas', 'roupeiro_3p.jpg'),
('Painel de TV', 'painel_tv.jpg'),
('Mesa de Centro', 'mesa_centro.jpg'),
('Criado-Mudo', 'criado_mudo.jpg');

