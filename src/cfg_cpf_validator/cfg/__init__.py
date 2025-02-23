import typing as t

import nltk as n

CFG_STRUCTURE = n.CFG.fromstring(
    """
    S -> D D D D D D D D D D D | D D D '.' D D D '.' D D D '-' D D
    D -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    """
)

structure_parser = n.parse.ChartParser(CFG_STRUCTURE)


def validate_structure(
    cpf: t.Union[
        str,
        int,
    ],
) -> bool:
    """
    Valida estrutura de um CPF com base em uma Gramática Livre de Contexto.

    Parâmetros:
        cpf (str | int): CPF a ser validado.

    Retorna:
        bool: Indica se a estrutura do CPF é válida.
    """
    tokens = list(str(cpf))
    tree = list()
    for leaf in structure_parser.parse(tokens):
        tree.append(leaf)
    return bool(tree)
