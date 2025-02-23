import typing as t

import cfg_cpf_validator.cfg as c


def validate(
    cpf: t.Union[
        str,
        int,
    ],
) -> bool:
    """
    Valida um CPF.

    Parâmetros:
        cpf (str | int): CPF a ser validado.

    Retorna:
        bool: Indica se o CPF é válido.
    """

    structure = c.validate_structure(cpf)

    return structure
