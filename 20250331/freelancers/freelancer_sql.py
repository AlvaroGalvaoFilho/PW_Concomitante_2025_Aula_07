# SQL para criar a tabela 'freelancers' se ela não existir.
CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS freelancers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    idade INTEGER NOT NULL
)
'''

# SQL para inserir um novo freelancer.
INSERT_FREELANCER = '''
INSERT INTO freelancers (nome, cpf, idade)
VALUES (?, ?, ?)
'''

# SQL para selecionar um freelancer específico pelo seu ID.
SELECT_FREELANCER = '''
SELECT id, nome, cpf, idade
FROM freelancers
WHERE id = ?
'''

# SQL para selecionar todos os freelancers da tabela.
SELECT_TODOS_FREELANCERS = '''
SELECT id, nome, cpf, idade
FROM freelancers
'''

# SQL para atualizar os dados de um freelancer existente, identificado pelo ID.
UPDATE_FREELANCER = '''
UPDATE freelancers
SET nome = ?, cpf = ?, idade = ?
WHERE id = ?
'''

# SQL para excluir um freelancer da tabela, identificado pelo ID.
DELETE_FREELANCER = '''
DELETE FROM freelancers
WHERE id = ?
'''
