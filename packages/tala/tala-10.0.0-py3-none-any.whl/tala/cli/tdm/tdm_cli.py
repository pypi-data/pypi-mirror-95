from pathlib import Path
import prompt_toolkit
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.validation import Validator

from tala.cli.tdm.passivity_timer import PassivityTimer, PASSIVE
from tala.utils.tdm_client import TDMClient
from tala.utils.observable import Observer


class TDMCLI(object):
    def __init__(self, url):
        self._client = TDMClient(url)
        self._tdm_session = None
        self._passivity_timer = PassivityTimer()
        self._passivity_timer.add_observer(PassivityTimerObserver(self))
        history = self._create_file_history()
        activity_detector = self._create_activity_detector_as_empty_validator()
        self._session = PromptSession(history=history, mouse_support=True, validator=activity_detector)

    def _create_activity_detector_as_empty_validator(self):
        def on_active(text):
            if text:
                self._passivity_timer.stop()
            return True

        return Validator.from_callable(on_active)

    def stop(self):
        self._passivity_timer.stop()

    def run(self):
        for system_turn in self.system_turns():
            print(system_turn)

    def system_turns(self):
        greeting = self._request(self._client.start_session)
        yield greeting
        while True:
            message = self._session.prompt("U> ").rstrip()
            self._passivity_timer.stop()
            yield self._request(self._client.request_text_input, self._tdm_session, message)

    def _request(self, callable, *args, **kwargs):
        response = callable(*args, **kwargs)
        if not self._tdm_session:
            self._tdm_session = response["session"]["session_id"]
        expected_passivity = response["output"]["expected_passivity"]
        if expected_passivity is not None:
            self._passivity_timer.start(expected_passivity)
        system_utterance = response["output"]["utterance"]
        return "S> {}".format(system_utterance)

    def request_passivity(self):
        system_utterance = self._request(self._client.request_passivity, self._tdm_session)

        def print_passivity_turn():
            print("U>")
            print(system_utterance)

        prompt_toolkit.application.run_in_terminal(print_passivity_turn)

    def _create_file_history(self):
        history_file = Path(".tala") / "history"
        if not history_file.parent.exists():
            history_file.parent.mkdir()
        if not history_file.exists():
            history_file.touch()
        return FileHistory(str(history_file))


class PassivityTimerObserver(Observer):
    def __init__(self, tdm_cli):
        self._tdm_cli = tdm_cli

    def update(self, value):
        if value == PASSIVE:
            self._tdm_cli.request_passivity()
