from typing import List, Dict, Tuple
import json
from pathlib import Path


# =========================
# 1) EJERCICIO PRINCIPAL
# =========================
def calculate_panels(panel_width: int, panel_height: int,
                     roof_width: int, roof_height: int) -> int:
    pw, ph = panel_width, panel_height
    W, H = roof_width, roof_height

    """
        Calcula el número máximo de paneles que caben en un techo rectangular de dimensiones W x H,
        considerando que los paneles pueden rotarse 90 grados.
        Args:
            panel_width(pw) (int): Ancho del panel. 
            panel_height(ph) (int): Alto del panel.
            roof_width (W) (int): Ancho del techo. 
            roof_height (H) (int): Alto del techo.
        Returns:
            int: Número máximo de paneles que caben en el techo.

        Estrategia:
        1) Calcular el número de paneles que caben en orientación normal y rotada.
        2) Probar combinaciones con cortes verticales y horizontales para maximizar el uso del espacio.
        3) Retornar el máximo encontrado.
    """

    # Si el panel no cabe ni rotado ni normal, no entra ninguno
    if (pw > W or ph > H) and (ph > W or pw > H):
        return 0

    def grid(w: int, h: int, a: int, b: int) -> int:
        return (w // a) * (h // b)

    best = max(
        grid(W, H, pw, ph),
        grid(W, H, ph, pw)
    )

    # Mezcla con corte vertical
    for cols in range(1, (W // pw) + 1):
        used_w = cols * pw
        left = cols * (H // ph)
        right = grid(W - used_w, H, ph, pw)
        best = max(best, left + right)

    for cols in range(1, (W // ph) + 1):
        used_w = cols * ph
        left = cols * (H // pw)
        right = grid(W - used_w, H, pw, ph)
        best = max(best, left + right)

    # Mezcla con corte horizontal
    for rows in range(1, (H // ph) + 1):
        used_h = rows * ph
        top = rows * (W // pw)
        bottom = grid(W, H - used_h, ph, pw)
        best = max(best, top + bottom)

    for rows in range(1, (H // pw) + 1):
        used_h = rows * pw
        top = rows * (W // ph)
        bottom = grid(W, H - used_h, pw, ph)
        best = max(best, top + bottom)

    return best


# =========================
# 2) BONUS 1
# =========================
def calculate_panels_triangle_isosceles(panel_width: int, panel_height: int,
                                        base_width: int, height: int) -> int:
    """
    Aproximación por 'filas' (strip packing):
    - A cada altura y, el ancho disponible es w(y) = B * (1 - y/H)
    - Sumamos cuántos paneles caben por fila.
    Probamos ambas orientaciones y nos quedamos con la mejor.
    """
    pw, ph = panel_width, panel_height
    B, H = base_width, height

    if B <= 0 or H <= 0 or pw <= 0 or ph <= 0:
        return 0

    def count_for_orientation(a: int, b: int) -> int:
        rows = H // b
        total = 0
        for r in range(rows):
            y = r * b
            y_top = y + b  # punto más angosto de la banda
            if y_top > H:
                break

            available_w = B * (1 - (y_top / H))
            if available_w <= 0:
                break

            total += int(available_w // a)
        return total

    return max(
        count_for_orientation(pw, ph),
        count_for_orientation(ph, pw)
    )
# =========================
# 2) BONUS 2
# =========================
def calculate_panels_two_overlapped_rectangles(
    panel_w: int, panel_h: int,
    x: int, y: int,
    dx: int, dy: int
) -> int:
    """
    Dos rectángulos iguales (x by y).
    Rect1: (0,0) a (x,y)
    Rect2: (dx,dy) a (dx+x, dy+y)

    Retorna aproximación: descomposición en rectángulos disjuntos y suma.
    """
    if x <= 0 or y <= 0 or panel_w <= 0 or panel_h <= 0:
        return 0

    # Si el rect2 está totalmente a la izquierda/abajo, normalizamos para trabajar con dx,dy >= 0
    # (no es necesario, pero ayuda a simplificar)
    if dx < 0:
        dx = -dx
    if dy < 0:
        dy = -dy

    # Caso 1: no se traslapan (dx >= x o dy >= y) -> son dos rectángulos separados
    if dx >= x or dy >= y:
        return calculate_panels(panel_w, panel_h, x, y) * 2

    # Caso 2: sí hay traslape
    overlap_w = x - dx
    overlap_h = y - dy

    total = 0

    # 1) Strip izquierdo (solo rect1): dx × y
    if dx > 0:
        total += calculate_panels(panel_w, panel_h, dx, y)

    # 2) Strip inferior (solo rect1): (x-dx) × dy
    if dy > 0 and overlap_w > 0:
        total += calculate_panels(panel_w, panel_h, overlap_w, dy)

    # 3) Overlap: (x-dx) × (y-dy)
    if overlap_w > 0 and overlap_h > 0:
        total += calculate_panels(panel_w, panel_h, overlap_w, overlap_h)

    # 4) Strip superior (solo rect2): (x-dx) × dy
    if dy > 0 and overlap_w > 0:
        total += calculate_panels(panel_w, panel_h, overlap_w, dy)

    # 5) Strip derecho (solo rect2): dx × y
    if dx > 0:
        total += calculate_panels(panel_w, panel_h, dx, y)

    return total


# =========================
# 3) INPUTS POR CONSOLA
# =========================
def _read_int(prompt: str, min_value: int = 1) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if val < min_value:
                print(f"⚠️ Debe ser >= {min_value}. Intenta de nuevo.")
                continue
            return val
        except ValueError:
            print("⚠️ Ingresa un número entero válido.")


def interactive_mode() -> None:
    print("\nModo interactivo")
    print("----------------")
    panel_w = _read_int("Ancho del panel: ")
    panel_h = _read_int("Alto del panel: ")

    print("\nElige tipo de techo:")
    print("  1) Rectángulo")
    print("  2) Triángulo isósceles")
    print("  3) Techo superpuesto")

    option = _read_int("Opción (1-3): ", min_value=1)
    while option not in (1, 2, 3):
        print("⚠️ Opción inválida. Debe ser 1, 2 o 3.")
        option = _read_int("Opción (1-3): ", min_value=1)

    if option == 1:
        roof_w = _read_int("Ancho del techo (rectángulo): ")
        roof_h = _read_int("Alto del techo (rectángulo): ")
        result = calculate_panels(panel_w, panel_h, roof_w, roof_h)
        print(f"\n✅ Paneles que caben: {result}\n")

    elif option == 2:
        base = _read_int("Base del triángulo: ")
        height = _read_int("Altura del triángulo: ")
        result = calculate_panels_triangle_isosceles(panel_w, panel_h, base, height)
        print(f"\n✅ Paneles que caben (triángulo): {result}\n")

    else:
        x = _read_int("Ancho de cada rectángulo (x): ")
        y = _read_int("Alto de cada rectángulo (y): ")
        dx = _read_int("Desplazamiento horizontal (dx): ", min_value=0)
        dy = _read_int("Desplazamiento vertical (dy): ", min_value=0)

        result = calculate_panels_two_overlapped_rectangles(panel_w, panel_h, x, y, dx, dy)
        print(f"\n✅ Paneles que caben (2 rectángulos superpuestos): {result}\n")


# =========================
# 4) TESTS DEL TEMPLATE
# =========================
def run_tests() -> None:
    base_dir = Path(__file__).resolve().parent
    test_path = base_dir / "test_cases.json"

    with test_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    test_cases: List[Dict[str, int]] = [
        {
            "panel_w": test["panelW"],
            "panel_h": test["panelH"],
            "roof_w": test["roofW"],
            "roof_h": test["roofH"],
            "expected": test["expected"]
        }
        for test in data["testCases"]
    ]

    print("Corriendo tests:")
    print("-------------------")

    for i, test in enumerate(test_cases, 1):
        result = calculate_panels(
            test["panel_w"], test["panel_h"],
            test["roof_w"], test["roof_h"]
        )
        passed = result == test["expected"]

        print(f"Test {i}:")
        print(f"  Panels: {test['panel_w']}x{test['panel_h']}, "
              f"Roof: {test['roof_w']}x{test['roof_h']}")
        print(f"  Expected: {test['expected']}, Got: {result}")
        print(f"  Status: {'✅ PASSED' if passed else '❌ FAILED'}\n")


def main() -> None:
    print("🐕 Wuuf wuuf wuuf 🐕")
    print("================================\n")

    print("¿Qué quieres hacer?")
    print("  1) Correr tests del template")
    print("  2) Ingresar valores manualmente (modo interactivo)")

    choice = _read_int("Opción (1-2): ", min_value=1)
    while choice not in (1, 2):
        print("⚠️ Opción inválida.")
        choice = _read_int("Opción (1-2): ", min_value=1)

    if choice == 1:
        run_tests()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
