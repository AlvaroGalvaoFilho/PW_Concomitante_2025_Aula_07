from typing import List, Optional
from freelancers.freelancer import Freelancer  # Importa a classe de domínio
from freelancers import freelancer_sql as sql  # Importa as constantes SQL
from util import get_db_connection  # Importa o gerenciador de conexão
import sqlite3

class FreelancerRepo:
    """
    Repositório para gerenciar operações CRUD (Create, Read, Update, Delete)
    para a entidade Freelancer no banco de dados.
    """
    def __init__(self):
        """Inicializa o repositório e garante que a tabela de freelancers exista."""
        self._criar_tabela()

    def _criar_tabela(self):
        """Método privado para criar a tabela 'freelancers' se ela não existir."""
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.CREATE_TABLE)
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def adicionar(self, freelancer: Freelancer) -> Optional[int]:
        """
        Adiciona um novo freelancer ao banco de dados.
        Retorna o ID do freelancer inserido ou None em caso de erro.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.INSERT_FREELANCER, (freelancer.nome, freelancer.cpf, freelancer.idade))
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao adicionar freelancer: {e}")
            return None

    def obter(self, freelancer_id: int) -> Optional[Freelancer]:
        """
        Busca um freelancer no banco de dados pelo seu ID.
        Retorna um objeto Freelancer se encontrado, caso contrário, retorna None.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_FREELANCER, (freelancer_id,))
                row = cursor.fetchone()
                if row:
                    return Freelancer(id=row[0], nome=row[1], cpf=row[2], idade=row[3])
                return None
        except sqlite3.Error as e:
            print(f"Erro ao obter freelancer {freelancer_id}: {e}")
            return None

    def obter_todos(self) -> List[Freelancer]:
        """
        Busca todos os freelancers cadastrados no banco de dados.
        Retorna uma lista de objetos Freelancer.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_TODOS_FREELANCERS)
                rows = cursor.fetchall()
                return [Freelancer(id=row[0], nome=row[1], cpf=row[2], idade=row[3]) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao obter todos os freelancers: {e}")
            return []

    def atualizar(self, freelancer: Freelancer) -> bool:
        """
        Atualiza os dados de um freelancer existente no banco de dados.
        Retorna True se a atualização foi bem-sucedida, False caso contrário.
        """
        if freelancer.id is None:
            print("Erro: Freelancer sem ID não pode ser atualizado.")
            return False
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.UPDATE_FREELANCER, (freelancer.nome, freelancer.cpf, freelancer.idade, freelancer.id))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao atualizar freelancer {freelancer.id}: {e}")
            return False

    def excluir(self, freelancer_id: int) -> bool:
        """
        Exclui um freelancer do banco de dados pelo seu ID.
        Retorna True se a exclusão foi bem-sucedida, False caso contrário.
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.DELETE_FREELANCER, (freelancer_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao excluir freelancer {freelancer_id}: {e}")
            return False
