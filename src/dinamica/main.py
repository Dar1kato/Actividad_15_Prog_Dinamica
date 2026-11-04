"""
Problema del corte de varillas (Rod Cutting).

Compara tres técnicas para obtener el máximo ingreso y los cortes óptimos:
    1. Recursión pura
    2. Memoización (top-down)
    3. Tabulación (bottom-up)

Uso:
    uv run main.py
    uv run main.py --limite-recursivo 25   # omite la recursión pura para n > 25
"""

# importación de librerías
import argparse
import sys
import time
from collections.abc import Callable, Sequence

# Acotamiento del tiempo de ejecución para los algoritmos recursivos
sys.setrecursionlimit(2000)

# Definición de la entrada constante
PRECIOS = (0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30)
LONGITUDES = (5, 10, 15, 20, 25, 28, 30)
REPETICIONES = 1000  # repeticiones para promediar los métodos rápidos


# ---------------------------------------------------------------------------
# 1. Solución recursiva pura
# ---------------------------------------------------------------------------
def cut_rod(p: Sequence[int], n: int) -> tuple[int, list[int]]:
    """
    Función recursiva para calcular el máximo ingreso por los cortes realizados
    en una varilla de longitud n. Devuelve (ingreso máximo, lista de cortes).
    """
    if n == 0:
        return 0, []
    q = -1
    cortes: list[int] = []
    for i in range(1, n + 1):
        # Evaluar todas las opciones de corte inicial de tamaño i e invocando de
        # manera recursiva a la función para calcular el máximo ingreso con el remanente
        precio_i = p[i] if i < len(p) else 0
        ingreso_resto, cortes_resto = cut_rod(p, n - i)
        if precio_i + ingreso_resto > q:
            q = precio_i + ingreso_resto
            cortes = [i] + cortes_resto
    return q, cortes


# ---------------------------------------------------------------------------
# 2. Memoización
# ---------------------------------------------------------------------------
def cut_rod_memoized(p: Sequence[int], n: int) -> tuple[int, list[int]]:
    """
    Función recursiva para calcular el máximo ingreso por los cortes realizados
    en una varilla de longitud n, implementando una función auxiliar de memoización.
    Devuelve (ingreso máximo, lista de cortes).
    """
    # Arreglo "r" de tamaño n+1 inicializado a -1 (valores no calculados)
    r = [-1] * (n + 1)
    # Arreglo "s": tamaño del primer corte óptimo para cada longitud
    s = [0] * (n + 1)
    q = cut_rod_aux(p, n, r, s)
    return q, reconstruir_cortes(s, n)


def cut_rod_aux(p: Sequence[int], n: int, r: list[int], s: list[int]) -> int:
    """
    Función auxiliar para la técnica de memoización: verifica si el resultado
    ya fue evaluado previamente, en cuyo caso recupera el valor almacenado.
    """
    # Verificación de resultado en memoria
    if r[n] >= 0:
        return r[n]

    # Caso de finalización/retorno
    if n == 0:
        q = 0
    else:
        q = -1
        for i in range(1, n + 1):
            # Evaluar todas las opciones de corte inicial de tamaño i e invocando
            # de manera recursiva a la función para calcular el máximo ingreso con el remanente
            precio_i = p[i] if i < len(p) else 0
            candidato = precio_i + cut_rod_aux(p, n - i, r, s)
            if candidato > q:
                q = candidato
                s[n] = i  # se guarda el primer corte óptimo para longitud n

    # Almacenamiento del resultado en memoria
    r[n] = q
    return q


# ---------------------------------------------------------------------------
# 3. Tabulación (bottom-up)
# ---------------------------------------------------------------------------
def cut_rod_tabulated(p: Sequence[int], n: int) -> tuple[int, list[int]]:
    """
    Calcula el máximo ingreso de forma iterativa (bottom-up): resuelve las
    longitudes 1, 2, ..., n en orden, reutilizando los subproblemas menores ya
    resueltos. Devuelve (ingreso máximo, lista de cortes).
    """
    r = [0] * (n + 1)  # r[j] = máximo ingreso para una varilla de longitud j
    s = [0] * (n + 1)  # s[j] = tamaño del primer corte óptimo para longitud j

    for j in range(1, n + 1):
        q = -1
        for i in range(1, j + 1):
            precio_i = p[i] if i < len(p) else 0
            if precio_i + r[j - i] > q:
                q = precio_i + r[j - i]
                s[j] = i
        r[j] = q

    return r[n], reconstruir_cortes(s, n)


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def reconstruir_cortes(s: list[int], n: int) -> list[int]:
    """Reconstruye la lista de cortes a partir del arreglo de primeros cortes s."""
    cortes = []
    while n > 0:
        cortes.append(s[n])
        n -= s[n]
    return cortes


def medir(
    func: Callable[[Sequence[int], int], tuple[int, list[int]]],
    n: int,
    repeticiones: int = 1,
) -> tuple[float, int, list[int]]:
    """Ejecuta func(PRECIOS, n) y devuelve (tiempo promedio en s, ingreso, cortes)."""
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        ingreso, cortes = func(PRECIOS, n)
    tiempo = (time.perf_counter() - inicio) / repeticiones
    return tiempo, ingreso, cortes


def formatear_tiempo(segundos: float | None) -> str:
    if segundos is None:
        return "omitido"
    if segundos < 1e-3:
        return f"{segundos * 1e6:.2f} µs"
    if segundos < 1:
        return f"{segundos * 1e3:.2f} ms"
    return f"{segundos:.2f} s"


def formatear_cortes(cortes: list[int]) -> str:
    return " + ".join(str(c) for c in cortes) if cortes else "-"


def imprimir_tabla(filas: list[tuple[str, ...]]) -> None:
    encabezados = (
        "Longitud de la varilla",
        "Recursivo",
        "Memoización",
        "Tabulación",
        "Ingreso Máximo",
        "Cortes",
    )
    anchos = [
        max(len(encabezados[c]), *(len(fila[c]) for fila in filas))
        for c in range(len(encabezados))
    ]
    separador = "+-" + "-+-".join("-" * a for a in anchos) + "-+"

    def linea(valores: Sequence[str]) -> str:
        return "| " + " | ".join(v.rjust(a) if c < 5 else v.ljust(a)
                                 for c, (v, a) in enumerate(zip(valores, anchos))) + " |"

    print(separador)
    print(linea(encabezados))
    print(separador)
    for fila in filas:
        print(linea(fila))
    print(separador)


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Corte de varillas: recursivo vs memoización vs tabulación")
    parser.add_argument(
        "--limite-recursivo",
        type=int,
        default=None,
        help="Longitud máxima para ejecutar la recursión pura (por defecto se ejecuta en todas; "
        "n=28 y n=30 pueden tardar varios minutos).",
    )
    args = parser.parse_args()

    filas = []
    for n in LONGITUDES:
        t_rec = None
        if args.limite_recursivo is None or n <= args.limite_recursivo:
            if n >= 25:
                print(f"Calculando recursión pura para n={n} (puede tardar)...", file=sys.stderr, flush=True)
            t_rec, ingreso_rec, cortes_rec = medir(cut_rod, n)

        t_memo, ingreso_memo, cortes_memo = medir(cut_rod_memoized, n, REPETICIONES)
        t_tab, ingreso_tab, cortes_tab = medir(cut_rod_tabulated, n, REPETICIONES)

        # Verificación de que las técnicas coinciden
        assert (ingreso_memo, cortes_memo) == (ingreso_tab, cortes_tab), f"Memoización y tabulación difieren en n={n}"
        if t_rec is not None:
            assert (ingreso_rec, cortes_rec) == (ingreso_tab, cortes_tab), f"Recursivo difiere en n={n}"

        filas.append((
            str(n),
            formatear_tiempo(t_rec),
            formatear_tiempo(t_memo),
            formatear_tiempo(t_tab),
            f"${ingreso_tab}",
            formatear_cortes(cortes_tab),
        ))

    print()
    imprimir_tabla(filas)
    print(
        f"\nNota: recursivo = 1 ejecución; memoización y tabulación = promedio de {REPETICIONES} ejecuciones."
    )


if __name__ == "__main__":
    main()
