from collections import defaultdict

class TuringMachine:
    def __init__(
        self,
        tape_input,
        blank_symbol="_",
        initial_state="q0",
        accept_states=None,
        reject_states=None,
        transition_function=None,
    ):
        """
        tape_input: string con el contenido inicial de la cinta (sin blancos).
        blank_symbol: símbolo usado como blanco.
        initial_state: estado inicial.
        accept_states: conjunto de estados de aceptación.
        reject_states: conjunto de estados de rechazo.
        transition_function:
            - dict: { (estado, símbolo) : (nuevo_estado, nuevo_símbolo, movimiento) }
            - o función: f(estado, símbolo) -> (nuevo_estado, nuevo_símbolo, movimiento) | None
        movimiento: 'L', 'R' o 'N' (no moverse).
        """
        self.blank = blank_symbol
        self.state = initial_state
        self.accept_states = set(accept_states or [])
        self.reject_states = set(reject_states or [])
        self.transition_function = transition_function

        # Cinta infinita simulada con diccionario
        self.tape = defaultdict(lambda: self.blank)
        for i, ch in enumerate(tape_input):
            self.tape[i] = ch

        self.head = 0
        self.halted = False

    def _get_transition(self, state, symbol):
        """Obtiene la transición desde dict o función."""
        if self.transition_function is None:
            return None
        if callable(self.transition_function):
            return self.transition_function(state, symbol)
        # Se asume dict
        return self.transition_function.get((state, symbol))

    def step(self):
        """Ejecuta un solo paso de la máquina."""
        if self.halted:
            return

        current_symbol = self.tape[self.head]
        trans = self._get_transition(self.state, current_symbol)

        # Si no hay transición definida, se detiene
        if trans is None:
            self.halted = True
            return

        new_state, new_symbol, movement = trans

        # Escribir símbolo
        self.tape[self.head] = new_symbol
        # Cambiar estado
        self.state = new_state

        # Mover cabezal
        if movement == "R":
            self.head += 1
        elif movement == "L":
            self.head -= 1
        # 'N' -> no moverse

        # Verificar si se debe detener
        if self.state in self.accept_states or self.state in self.reject_states:
            self.halted = True

    def run(self, max_steps=10000):
        """Ejecuta la máquina hasta halting o hasta max_steps."""
        steps = 0
        while not self.halted and steps < max_steps:
            self.step()
            steps += 1
        return steps

    def get_tape_as_string(self):
        """Devuelve el contenido 'útil' de la cinta (sin blancos extremos)."""
        keys_with_non_blank = [k for k, v in self.tape.items() if v != self.blank]
        if not keys_with_non_blank:
            return ""

        min_i = min(keys_with_non_blank)
        max_i = max(keys_with_non_blank)
        return "".join(self.tape[i] for i in range(min_i, max_i + 1))
