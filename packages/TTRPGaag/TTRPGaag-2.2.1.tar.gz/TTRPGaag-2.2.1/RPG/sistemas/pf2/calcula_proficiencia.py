from .data import Data


def calcula_proficiencia(proficiencia: str, nivel: int = 1):
    proficiencia = proficiencia.lower()

    if proficiencia == 'untrained':
        return 0

    return Data.proficiency[proficiencia] + nivel
