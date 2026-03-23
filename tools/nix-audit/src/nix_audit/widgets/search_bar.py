from textual.widgets import Input
from textual.message import Message
from textual.timer import Timer


class SearchBar(Input):
    """Input with debounced search."""

    class Submitted(Message):
        def __init__(self, value: str) -> None:
            super().__init__()
            self.value = value

    DEBOUNCE_SECONDS = 0.4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._debounce_timer: Timer | None = None

    def _on_input_changed(self, event: Input.Changed) -> None:
        if self._debounce_timer:
            self._debounce_timer.stop()
        self._debounce_timer = self.set_timer(
            self.DEBOUNCE_SECONDS,
            lambda: self.post_message(self.Submitted(self.value)),
        )
