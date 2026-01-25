import time

from core.speech.speech_loop import SpeechLoop
from core.control.interrupt_controller import InterruptController
from core.control.global_interrupt import GlobalInterrupt


def test_speech_loop_hard_interrupt_blocks_speech():
    spoken = []

    def speak_fn(text: str):
        spoken.append(text)

    interrupts = InterruptController()
    interrupts.trigger_hard()

    loop = SpeechLoop(
        speak_fn=speak_fn,
        interrupt_controller=interrupts,
    )

    loop.speak("hello world")

    assert spoken == []


def test_speech_loop_soft_interrupt_pauses_until_clear():
    spoken = []

    def speak_fn(text: str):
        spoken.append(text)

    interrupts = InterruptController()
    interrupts.trigger_soft()

    loop = SpeechLoop(
        speak_fn=speak_fn,
        interrupt_controller=interrupts,
    )

    # resume after short delay
    def resume():
        time.sleep(0.1)
        interrupts.clear()

    import threading
    threading.Thread(target=resume).start()

    loop.speak("paused speech")

    assert spoken == ["paused speech"]


def test_speech_loop_restart_restarts_speech():
    spoken = []

    def speak_fn(text: str):
        spoken.append(text)

    interrupts = InterruptController()
    loop = SpeechLoop(
        speak_fn=speak_fn,
        interrupt_controller=interrupts,
    )

    # trigger restart before first attempt
    interrupts.trigger_restart()

    loop.speak("restart speech")

    # speech should still happen exactly once
    assert spoken == ["restart speech"]


def test_speech_loop_ignore_allows_speech():
    spoken = []

    def speak_fn(text: str):
        spoken.append(text)

    interrupts = InterruptController()

    loop = SpeechLoop(
        speak_fn=speak_fn,
        interrupt_controller=interrupts,
    )

    loop.speak("normal speech")

    assert spoken == ["normal speech"]
