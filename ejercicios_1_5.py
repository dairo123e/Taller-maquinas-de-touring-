from turing_machine import TuringMachine

# ==========================
# EJERCICIOS 1–5 
# ==========================

# 1. Complemento de un número binario
def build_tm_complemento_binario(binary_input: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        if q == "q0":
            if s == "0":
                return ("q0", "1", "R")
            elif s == "1":
                return ("q0", "0", "R")
            elif s == blank:
                return ("q_accept", blank, "N")
        return None  # no definida -> halt

    return TuringMachine(
        tape_input=binary_input,
        blank_symbol=blank,
        initial_state="q0",
        accept_states=accept,
        transition_function=delta,
    )


# 2. Sucesor en unario: 111 -> 1111
def build_tm_sucesor_unario(unary_input: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        if q == "q0":
            if s == "1":
                return ("q0", "1", "R")
            elif s == blank:
                return ("q_accept", "1", "N")
        return None

    return TuringMachine(
        tape_input=unary_input,
        blank_symbol=blank,
        initial_state="q0",
        accept_states=accept,
        transition_function=delta,
    )


# 3. Predecesor en unario: 1111 -> 111
def build_tm_predecesor_unario(unary_input: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        if q == "q0":
            if s == "1":
                return ("q0", "1", "R")
            elif s == blank:
                # Retroceder al último 1
                return ("q_back", blank, "L")

        elif q == "q_back":
            if s == "1":
                # borrar este último 1
                return ("q_accept", blank, "N")
        return None

    return TuringMachine(
        tape_input=unary_input,
        blank_symbol=blank,
        initial_state="q0",
        accept_states=accept,
        transition_function=delta,
    )


# 4. Paridad de un número binario
# Si #1's es par -> añade 0; si es impar -> añade 1
def build_tm_paridad_binaria(binary_input: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        # q_even = par, q_odd = impar
        if q == "q_even":
            if s == "0":
                return ("q_even", "0", "R")
            elif s == "1":
                return ("q_odd", "1", "R")
            elif s == blank:
                # número de 1's par -> añadir 0
                return ("q_accept", "0", "N")

        elif q == "q_odd":
            if s == "0":
                return ("q_odd", "0", "R")
            elif s == "1":
                return ("q_even", "1", "R")
            elif s == blank:
                # número de 1's impar -> añadir 1
                return ("q_accept", "1", "N")

        return None

    return TuringMachine(
        tape_input=binary_input,
        blank_symbol=blank,
        initial_state="q_even",
        accept_states=accept,
        transition_function=delta,
    )


# 5. Contador unario de {a, b, c}: abca -> 1111
def build_tm_contador_abc(word: str) -> TuringMachine:
    blank = "_"
    accept = {"q_accept"}

    def delta(q, s):
        if q == "q0":
            if s in {"a", "b", "c"}:
                # sustituir cualquier letra por '1'
                return ("q0", "1", "R")
            elif s == blank:
                return ("q_accept", blank, "N")
        return None

    return TuringMachine(
        tape_input=word,
        blank_symbol=blank,
        initial_state="q0",
        accept_states=accept,
        transition_function=delta,
    )


# ==========================
# PRUEBAS 
# ==========================
if __name__ == "__main__":
    print("=== PRUEBAS EJERCICIOS 1–5 ===")

    # Ejercicio 1
    tm1 = build_tm_complemento_binario("10101")
    tm1.run()
    print("Ej1 complemento(10101) ->", tm1.get_tape_as_string())

    # Ejercicio 2
    tm2 = build_tm_sucesor_unario("111")
    tm2.run()
    print("Ej2 sucesor unario(111) ->", tm2.get_tape_as_string())

    # Ejercicio 3
    tm3 = build_tm_predecesor_unario("1111")
    tm3.run()
    print("Ej3 predecesor unario(1111) ->", tm3.get_tape_as_string())

    # Ejercicio 4
    tm4 = build_tm_paridad_binaria("1011")
    tm4.run()
    print("Ej4 paridad(1011) ->", tm4.get_tape_as_string())

    # Ejercicio 5
    tm5 = build_tm_contador_abc("abca")
    tm5.run()
    print("Ej5 contador_abc('abca') ->", tm5.get_tape_as_string())
