import typing as t

import jinja2 as jinja
import nltk as n

CFG_STRUCTURE = n.CFG.fromstring(
    """
    S -> D D D D D D D D D D D | D D D '.' D D D '.' D D D '-' D D
    D -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    """
)

CFG_CHECK_DIGITS_PRODUCTIONS_TEMPLATE = """
    S -> FCD SCD
    FCD -> '{{ check_digit_1 }}'
    SCD -> '{{ check_digit_2 }}'
"""

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


def validate_check_digits(
    cpf: t.Union[str, int],
    check_digit_1: t.Union[str, int],
    check_digit_2: t.Union[str, int],
):
    """
    Valida os dígitos verificadores de um CPF com base em uma Gramática Livre
    de Contexto feita com os dígitso verificadores passados como argumento.

    Parâmetros:
        cpf (str | int): CPF a ter seus dígitos verificadores validados.
        check_digit_1 (str | int): Número que deve ser o primeiro dígito
        verificador do CPF.
        check_digit_2 (str | int): Número que deve ser o segundo dígito
        verificador do CPF.

    Retorna:
        bool: Indica se os dígitos verificadores do CPF estão corretos.
    """
    cfg_check_digits_productions = jinja.Template(
        CFG_CHECK_DIGITS_PRODUCTIONS_TEMPLATE
    ).render(check_digit_1=check_digit_1, check_digit_2=check_digit_2)

    cfg_check_digits = n.CFG.fromstring(cfg_check_digits_productions)

    check_digits_parser = n.parse.ChartParser(cfg_check_digits)

    tokens = list(str(cpf)[-2:])
    tree = list()
    try:
        for leaf in check_digits_parser.parse(tokens):
            tree.append(leaf)
        return bool(tree)
    except ValueError:
        return False

def calcular_digito_verificador(cpf_base) -> list:
    """
    Calcula dígitos verificadores do CPF fornecido

    Parâmetros:
        cpf_base (str): CPF a ser calculado

    Retorna:
        list: Lista com os dígitos verificadores
    """
    # Remover carácteres não numericos do cpf
    cpf_base = ''.join(filter(str.isdigit, cpf_base))

    # Função para cálculo padrão de digitos
    def calc_digit(cpf: str, multiplicadores: list, ) -> int:
        soma = 0
        for i in range(len(multiplicadores)):
            soma += int(cpf[i]) * multiplicadores[i]
            resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Cálculo do 1° digito
    multiplicadores = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    d1 = calc_digit(cpf_base, multiplicadores)

    # Cálculo do 2° digito
    multiplicadores.insert(0, 11)
    d2 = calc_digit(cpf_base, multiplicadores)

    return [d1, d2]

