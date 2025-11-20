from turing_machine import TuringMachine

# ==========================
# EJERCICIOS 6–10 (STIVEN)
# ==========================

# 6. Copia de una cadena {A,B,C}: AABC -> AABCAABC
def build_tm_copia_ABC(word: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        # q0: buscar próxima letra sin marcar
        if q == "q0":
            if s == "A":
                return ("qA_go_end", "a", "R")
            elif s == "B":
                return ("qB_go_end", "b", "R")
            elif s == "C":
                return ("qC_go_end", "c", "R")
            elif s == blank:
                # Ya todas marcadas, ahora restaurar mayúsculas
                return ("q_restore", blank, "L")
            else:  # a, b, c ya marcadas
                return ("q0", s, "R")

        # Ir al final para escribir copia
        if q == "qA_go_end":
            if s != blank:
                return ("qA_go_end", s, "R")
            else:
                return ("q_back_start", "A", "L")

        if q == "qB_go_end":
            if s != blank:
                return ("qB_go_end", s, "R")
            else:
                return ("q_back_start", "B", "L")

        if q == "qC_go_end":
            if s != blank:
                return ("qC_go_end", s, "R")
            else:
                return ("q_back_start", "C", "L")

        # Volver al inicio
        if q == "q_back_start":
            if s != blank:
                return ("q_back_start", s, "L")
            else:
                # estamos en blanco a la izquierda, avanzamos a primer símbolo
                return ("q0", blank, "R")

        # Restaurar a, b, c a A,B,C
        if q == "q_restore":
            if s == "a":
                return ("q_restore", "A", "L")
            if s == "b":
                return ("q_restore", "B", "L")
            if s == "c":
                return ("q_restore", "C", "L")
            if s in {"A", "B", "C"}:
                return ("q_restore", s, "L")
            if s == blank:
                # terminado
                return ("q_accept", blank, "R")

        return None

    return TuringMachine(
        tape_input=word,
        blank_symbol=blank,
        initial_state="q0",
        accept_states=accept,
        transition_function=delta,
    )


# 7. Reemplazo de M primeras A’s por B’s (ejemplo: 11AAAAB, M=2)
def build_tm_reemplazo_M_As(cinta: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        # q0: buscar un 1 sin marcar para gastar
        if q == "q0":
            if s == "1":
                return ("q_goA", "x", "R")  # marcar este 1
            elif s == "x":  # ya usado
                return ("q0", "x", "R")
            else:
                # ya no hay 1's sin usar -> restaurar
                return ("q_restore", s, "L")

        # q_goA: ir a la primera A sin transformar
        if q == "q_goA":
            if s in {"1", "x", "B"}:
                return ("q_goA", s, "R")
            elif s == "A":
                return ("q_back", "B", "L")  # convertir esta A en B
            elif s == blank:
                # No encontró A suficiente (caso borde)
                return ("q_restore", blank, "L")

        # q_back: volver al principio para usar el próximo 1
        if q == "q_back":
            if s != blank:
                return ("q_back", s, "L")
            else:
                return ("q0", blank, "R")

        # q_restore: restaurar x -> 1
        if q == "q_restore":
            if s == "x":
                return ("q_restore", "1", "L")
            elif s in {"1", "A", "B"}:
                return ("q_restore", s, "L")
            elif s == blank:
                return ("q_accept", blank, "R")

        return None

    return TuringMachine(
        tape_input=cinta,
        blank_symbol=blank,
        initial_state="q0",
        accept_states=accept,
        transition_function=delta,
    )


# 8. Comparación de dos palabras separadas por #
def build_tm_comparar_palabras(cinta: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}
    reject = {"q_reject"}

    def delta(q, s):
        # q_start: escoger siguiente símbolo del lado izquierdo
        if q == "q_start":
            if s == "0":
                return ("q_match0", "X", "R")  # marcar y comparar 0
            elif s == "1":
                return ("q_match1", "Y", "R")  # marcar y comparar 1
            elif s == "#":
                # ya no hay más en lado izquierdo -> revisar lado derecho
                return ("q_check_rest", "#", "R")
            elif s in {"X", "Y"}:
                return ("q_start", s, "R")
            elif s == blank:
                # caso raro: nada a la izquierda
                return ("q_check_rest", blank, "R")

        # q_match0: ir hasta el # y luego buscar un 0 sin marcar a la derecha
        if q == "q_match0":
            if s != "#":
                return ("q_match0", s, "R")
            else:
                return ("q_find0", "#", "R")

        if q == "q_find0":
            if s in {"X", "Y"}:
                return ("q_find0", s, "R")
            elif s == "0":
                return ("q_back_left", "X", "L")  # marcar y volver
            elif s in {"1", blank, "#"}:
                return ("q_reject", s, "N")

        # q_match1: análogo para el 1
        if q == "q_match1":
            if s != "#":
                return ("q_match1", s, "R")
            else:
                return ("q_find1", "#", "R")

        if q == "q_find1":
            if s in {"X", "Y"}:
                return ("q_find1", s, "R")
            elif s == "1":
                return ("q_back_left", "Y", "L")
            elif s in {"0", blank, "#"}:
                return ("q_reject", s, "N")

        # q_back_left: volver al inicio (lado izquierdo)
        if q == "q_back_left":
            if s != blank:
                return ("q_back_left", s, "L")
            else:
                return ("q_start", blank, "R")

        # q_check_rest: despues de procesar todo el lado izquierdo,
        # verificar que en el derecho no queden 0/1 sin marcar
        if q == "q_check_rest":
            if s in {"X", "Y"}:
                return ("q_check_rest", s, "R")
            elif s in {"0", "1"}:
                return ("q_reject", s, "N")
            elif s in {blank, "#"}:
                return ("q_accept", s, "N")

        return None

    return TuringMachine(
        tape_input=cinta,
        blank_symbol=blank,
        initial_state="q_start",
        accept_states=accept,
        reject_states=reject,
        transition_function=delta,
    )


# 9. Sucesor de un número binario
def build_tm_sucesor_binario(binary_input: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        if q == "q_scan_right":
            if s in {"0", "1"}:
                return ("q_scan_right", s, "R")
            elif s == blank:
                return ("q_add", blank, "L")

        if q == "q_add":
            if s == "0":
                return ("q_accept", "1", "N")
            elif s == "1":
                return ("q_add", "0", "L")
            elif s == blank:
                return ("q_accept", "1", "N")

        return None

    return TuringMachine(
        tape_input=binary_input,
        blank_symbol=blank,
        initial_state="q_scan_right",
        accept_states=accept,
        transition_function=delta,
    )


# 10. Antecesor de un número binario
def build_tm_antecesor_binario(binary_input: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        if q == "q_scan_right":
            if s in {"0", "1"}:
                return ("q_scan_right", s, "R")
            elif s == blank:
                return ("q_sub", blank, "L")

        if q == "q_sub":
            if s == "1":
                return ("q_accept", "0", "N")
            elif s == "0":
                return ("q_sub", "1", "L")
            elif s == blank:
                # caso borde, número era 0
                return ("q_accept", blank, "N")

        return None

    return TuringMachine(
        tape_input=binary_input,
        blank_symbol=blank,
        initial_state="q_scan_right",
        accept_states=accept,
        transition_function=delta,
    )


# ==========================
# PRUEBAS RÁPIDAS (STIVEN)
# ==========================
if __name__ == "__main__":
    print("=== PRUEBAS EJERCICIOS 6-10 ===")

    tm6 = build_tm_copia_ABC("AABC")
    tm6.run()
    print("Ej6 copia_ABC(AABC) ->", tm6.get_tape_as_string())

    tm7 = build_tm_reemplazo_M_As("11AAAAB")
    tm7.run()
    print("Ej7 reemplazo_M_As(11AAAAB) ->", tm7.get_tape_as_string())

    tm8 = build_tm_comparar_palabras("101#101")
    tm8.run()
    print("Ej8 comparar 101#101 (debe aceptar) -> estado final:", tm8.state)

    tm8b = build_tm_comparar_palabras("110#101")
    tm8b.run()
    print("Ej8 comparar 110#101 (debe rechazar) -> estado final:", tm8b.state)

    tm9 = build_tm_sucesor_binario("1011")
    tm9.run()
    print("Ej9 sucesor_binario(1011) ->", tm9.get_tape_as_string())

    tm10 = build_tm_antecesor_binario("1100")
    tm10.run()
    print("Ej10 antecesor_binario(1100) ->", tm10.get_tape_as_string())