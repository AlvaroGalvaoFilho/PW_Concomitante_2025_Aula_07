from pydantic import BaseModel, Field
from typing import Optional

class Freelancer(BaseModel):
    id: Optional[int] = None
    nome: str
    cpf: str
    idade: int

    def __init__(self, **data):
        super().__init__(**data)

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._validate_nome(valor)
        self._nome = valor

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, valor: str) -> None:
        self._validate_cpf(valor)
        self._cpf = valor

    @property
    def idade(self) -> int:
        return self._idade

    @idade.setter
    def idade(self, valor: int) -> None:
        self._validate_idade(valor)
        self._idade = valor

    def _validate_nome(self, valor: str) -> None:
        if not valor.strip():
            raise ValueError("O nome não pode ser vazio.")

    def _validate_cpf(self, valor: str) -> None:
        if len(valor) != 11 or not valor.isdigit():
            raise ValueError("O CPF deve conter 11 dígitos numéricos.")

    def _validate_idade(self, valor: int) -> None:
        if valor <= 0:
            raise ValueError("A idade deve ser um número positivo.")
