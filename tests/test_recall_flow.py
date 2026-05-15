# ruff: noqa: E402
import asyncio
import sys
import types

astrbot = types.ModuleType("astrbot")
api = types.ModuleType("astrbot.api")
api.logger = types.SimpleNamespace(warning=lambda *a, **k: None)

event = types.ModuleType("astrbot.api.event")

class DummyFilter:
    class EventMessageType:
        GROUP_MESSAGE = 1

    def command(self, *_a, **_k):
        return lambda f: f

    def command_group(self, *_a, **_k):
        return lambda f: f

    def event_message_type(self, *_a, **_k):
        return lambda f: f

filter_obj = DummyFilter()
event.filter = filter_obj
event.AstrMessageEvent = object

star = types.ModuleType("astrbot.api.star")
star.Context = object
class Star:
    def __init__(self, _):
        pass
star.Star = Star
star.register = lambda *_a, **_k: (lambda cls: cls)

sys.modules["astrbot"] = astrbot
sys.modules["astrbot.api"] = api
sys.modules["astrbot.api.event"] = event
sys.modules["astrbot.api.star"] = star

from main import ImageRecaller


class Api:
    def __init__(self, fail=False):
        self.called = False
        self.fail = fail

    async def call_action(self, *_args, **_kwargs):
        self.called = True
        if self.fail:
            raise RuntimeError("x")


class Bot:
    def __init__(self, fail=False):
        self.api = Api(fail=fail)


class Sender:
    user_id = "200"


class Msg:
    group_id = "100"
    message_id = "300"
    sender = Sender()
    raw_message = "[CQ:image,file=1]"


class Event:
    def __init__(self, fail=False):
        self.message_obj = Msg()
        self.bot = Bot(fail)
        self.stopped = False

    def stop_event(self):
        self.stopped = True


def test_dry_run_not_delete():
    async def _run():
        p = ImageRecaller(None, {"targets": {"100": ["200"]}, "dry_run": True})
        await p.initialize()
        e = Event()
        await p.on_group_message(e)
        assert not e.bot.api.called
    asyncio.run(_run())


def test_success_delete():
    async def _run():
        p = ImageRecaller(None, {"targets": {"100": ["200"]}})
        await p.initialize()
        e = Event()
        await p.on_group_message(e)
        assert e.bot.api.called
    asyncio.run(_run())


def test_delete_exception_no_crash():
    async def _run():
        p = ImageRecaller(None, {"targets": {"100": ["200"]}})
        await p.initialize()
        e = Event(True)
        await p.on_group_message(e)
        assert p.stats.total_failed == 1
    asyncio.run(_run())
