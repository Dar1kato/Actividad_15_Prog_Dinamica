# Problema del corte de varillas (Rod Cutting)

Daniel Peña Cruz
200818

---

## 1. Descripción del problema

Dada una varilla de longitud `n` pulgadas y una tabla de precios `p[i]` para cada longitud de pieza `i = 1, 2, ..., n`, se busca determinar el **máximo ingreso** que se puede obtener cortando la varilla (o sin cortarla) y **qué cortes** producen ese ingreso.

Una varilla de `n` pulgadas puede cortarse de `2^(n-1)` formas distintas, ya que en cada una de las `n-1` posiciones intermedias se puede o no realizar un corte.

**Tabla de precios utilizada:**

| Longitud (i) | 1  | 2  | 3  | 4  | 5   | 6   | 7   | 8   | 9   | 10  |
|--------------|----|----|----|----|-----|-----|-----|-----|-----|-----|
| Precio       | $1 | $5 | $8 | $9 | $10 | $17 | $17 | $20 | $24 | $30 |

> Para piezas de más de 10 pulgadas el precio se considera `$0` (`p[i] if i < len(p) else 0`), por lo que nunca conviene venderlas sin cortar.

La relación de recurrencia que resuelve el problema es:

```
r(0) = 0
r(n) = max { p[i] + r(n - i) }   para 1 ≤ i ≤ n
```

donde `r(n)` es el máximo ingreso para una varilla de longitud `n`.

---

## 2. Estructura del proyecto

```
corte-varillas/
├── main.py          # Script con las tres implementaciones y la tabla comparativa
├── pyproject.toml   # Generado por `uv init`
└── README.md
```

Todo el código vive en un único archivo: `main.py`.

---

## 3. Cómo ejecutar el script

### Requisitos

- [uv](https://docs.astral.sh/uv/) instalado.
- Python 3.10 o superior (se usan anotaciones como `list[int]` y `float | None`).

### Pasos

```bash
# 1. Crear el proyecto
uv init corte-varillas
cd corte-varillas

# 2. Reemplazar el main.py generado por el script de esta práctica

# 3. Ejecutar
uv run main.py
```

El script imprime en la terminal la tabla comparativa de tiempos, el ingreso máximo y los cortes para las longitudes `5, 10, 15, 20, 25, 28 y 30`.

### Opciones

| Opción                    | Descripción                                                                                     |
|---------------------------|-------------------------------------------------------------------------------------------------|
| `--limite-recursivo N`    | Omite la recursión pura para longitudes mayores a `N` (se muestra `omitido` en la tabla).       |

Ejemplo de ejecución rápida:

```bash
uv run main.py --limite-recursivo 25
```

> ⚠️ **Advertencia:** la recursión pura es exponencial. Sin la opción anterior, las filas de `n = 28` y `n = 30` pueden tardar varios minutos (en la corrida de este reporte, la ejecución completa tomó alrededor de 4.5 minutos, la mayor parte en `n = 30`).

---

## 4. Explicación de los métodos

Las tres funciones devuelven una tupla `(ingreso_máximo, cortes)`. Ante empates, todas eligen el **primer** corte que alcanza el máximo (comparación con `>` estricto), por lo que las tres producen exactamente los mismos cortes. El script lo verifica con `assert`.

### 4.1 Recursión pura — `cut_rod(p, n)`

Implementa directamente la recurrencia. Para una varilla de longitud `n`, prueba **todos** los tamaños posibles del primer corte `i = 1..n` y resuelve de forma recursiva el remanente `n - i`.

- Los cortes se construyen al regresar de la recursión: cada vez que una opción mejora el máximo, se guarda `[i] + cortes_del_remanente`.
- **Problema:** los mismos subproblemas se resuelven una y otra vez (por ejemplo, `cut_rod(p, 3)` se calcula muchas veces dentro de `cut_rod(p, 30)`).
- **Complejidad temporal:** `O(2^n)`. **Espacio:** `O(n)` por la profundidad de la pila de recursión.

### 4.2 Memoización — `cut_rod_memoized(p, n)` y `cut_rod_aux(p, n, r, s)`

Es la misma recursión (enfoque *top-down*), pero guarda cada resultado la primera vez que se calcula:

- `r[j]` almacena el máximo ingreso para longitud `j` (`-1` indica "aún no calculado").
- `s[j]` almacena el **tamaño del primer corte óptimo** para longitud `j`.
- Antes de calcular, `cut_rod_aux` revisa si `r[n]` ya existe y, de ser así, lo devuelve sin volver a recursar.

Cada subproblema `0..n` se resuelve **una sola vez**, y cada uno realiza un ciclo de hasta `n` iteraciones.

- Los cortes se reconstruyen a partir de `s` con `reconstruir_cortes`: se toma `s[n]`, se resta de `n` y se repite hasta llegar a 0.
- **Complejidad temporal:** `O(n²)`. **Espacio:** `O(n)`.

### 4.3 Tabulación — `cut_rod_tabulated(p, n)`

Enfoque *bottom-up*, sin recursión. Se resuelven las longitudes en orden creciente `j = 1, 2, ..., n`, de modo que cuando se necesita `r[j - i]` este ya fue calculado:

```python
r[0] = 0
for j in range(1, n + 1):
    q = -1
    for i in range(1, j + 1):
        if p[i] + r[j - i] > q:
            q = p[i] + r[j - i]
            s[j] = i          # primer corte óptimo para longitud j
    r[j] = q
```

- Al igual que en la memoización, `s` permite reconstruir los cortes óptimos.
- Evita el costo de las llamadas recursivas y no tiene riesgo de exceder el límite de recursión.
- **Complejidad temporal:** `O(n²)`. **Espacio:** `O(n)`.

### 4.4 Resumen comparativo

| Método        | Enfoque   | Subproblemas repetidos | Tiempo   | Espacio |
|---------------|-----------|------------------------|----------|---------|
| Recursivo     | Top-down  | Sí                     | `O(2^n)` | `O(n)`  |
| Memoización   | Top-down  | No (se reutilizan)     | `O(n²)`  | `O(n)`  |
| Tabulación    | Bottom-up | No (se reutilizan)     | `O(n²)`  | `O(n)`  |

---

## 5. Resultados

```
+------------------------+-----------+-------------+------------+----------------+-----------------+
| Longitud de la varilla | Recursivo | Memoización | Tabulación | Ingreso Máximo | Cortes          |
+------------------------+-----------+-------------+------------+----------------+-----------------+
|                      5 |  11.22 µs |     1.93 µs |    1.50 µs |            $13 | 2 + 3           |
|                     10 | 179.43 µs |     4.83 µs |    3.82 µs |            $30 | 10              |
|                     15 |   5.58 ms |     9.46 µs |    6.68 µs |            $43 | 2 + 3 + 10      |
|                     20 | 179.61 ms |    16.05 µs |   11.09 µs |            $60 | 10 + 10         |
|                     25 |    5.95 s |    25.21 µs |   16.98 µs |            $73 | 2 + 3 + 10 + 10 |
|                     28 |   50.66 s |    32.48 µs |   23.15 µs |            $82 | 2 + 6 + 10 + 10 |
|                     30 |  218.61 s |    42.78 µs |   28.95 µs |            $90 | 10 + 10 + 10    |
+------------------------+-----------+-------------+------------+----------------+-----------------+
```

**Notas sobre la medición:**

- El tiempo de la recursión pura corresponde a **1 ejecución**.
- Los tiempos de memoización y tabulación son el **promedio de 1000 ejecuciones**, ya que duran microsegundos y una sola medición sería muy ruidosa.
- Los tiempos dependen del equipo en el que se ejecute el script; lo importante es la tendencia.

### Análisis

- **Recursión pura:** el tiempo crece de forma exponencial. Cada 5 pulgadas adicionales multiplica el tiempo por ~30 (de `n = 20` a `n = 25`: 179.61 ms → 5.95 s; de `n = 25` a `n = 30`: 5.95 s → 218.61 s), lo cual concuerda con el factor `2^5 = 32` esperado para `O(2^n)`.
- **Memoización y tabulación:** el tiempo crece de forma suave (polinomial). Para `n = 30` tardan decenas de microsegundos, frente a más de 3 minutos de la recursión pura.
- **Tabulación vs. memoización:** la tabulación fue consistentemente más rápida (entre 20 % y 35 % menos tiempo en esta corrida) porque evita la sobrecarga de las llamadas recursivas, aunque ambas tienen la misma complejidad asintótica.
- **Cortes y valor óptimo:** para `n = 10` y `n = 30` conviene usar piezas de 10 pulgadas (`$30` cada una, el mejor precio por pulgada de la tabla). En longitudes que no son múltiplos de 10 se complementan con piezas pequeñas como `2 + 3` (`$13`) o `2 + 6` (`$22`).
