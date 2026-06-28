import time
from assistant.timer import TimerService, parse_duration


class TestParseDuration:
    def test_minutes(self):
        assert parse_duration("таймер на 10 минут") == 600

    def test_minutes_variants(self):
        assert parse_duration("засеки 5 мин") == 300

    def test_hours(self):
        assert parse_duration("таймер на 1 час") == 3600

    def test_hours_minutes_variants(self):
        assert parse_duration("засеки 2 часа") == 7200

    def test_seconds(self):
        assert parse_duration("таймер на 30 секунд") == 30

    def test_combined(self):
        assert parse_duration("1 час 30 минут") == 5400

    def test_no_match(self):
        assert parse_duration("просто текст") is None


class TestTimerService:
    def test_add_timer(self):
        svc = TimerService()
        tid = svc.add_timer(60)
        assert tid == 1

    def test_multiple_timers(self):
        svc = TimerService()
        t1 = svc.add_timer(60)
        t2 = svc.add_timer(120)
        assert t1 == 1
        assert t2 == 2

    def test_get_remaining_returns_approx(self):
        svc = TimerService()
        svc.add_timer(60)
        timers = svc.get_remaining()
        assert len(timers) == 1
        tid, remaining, label = timers[0]
        assert tid == 1
        assert 55 <= remaining <= 60
        assert label is not None

    def test_get_remaining_by_id(self):
        svc = TimerService()
        svc.add_timer(60)
        remaining = svc.get_remaining(timer_id=1)
        assert 55 <= remaining <= 60

    def test_get_remaining_unknown_id(self):
        svc = TimerService()
        svc.add_timer(60)
        assert svc.get_remaining(timer_id=99) is None

    def test_active_count(self):
        svc = TimerService()
        svc.add_timer(60)
        svc.add_timer(120)
        assert svc.active_count() == 2

    def test_no_active_timers(self):
        svc = TimerService()
        assert svc.get_remaining() == []

    def test_callback_on_fire(self):
        results = []
        svc = TimerService(callback=lambda label: results.append(label))
        svc.add_timer(0.01)
        svc.start()
        time.sleep(0.3)
        svc.stop()
        assert len(results) == 1
        assert "0 сек" in results[0]

    def test_callback_not_called_before_fire(self):
        results = []
        svc = TimerService(callback=lambda label: results.append(label))
        svc.add_timer(9999)
        svc.start()
        time.sleep(0.05)
        svc.stop()
        assert results == []

    def test_fired_timer_not_in_remaining(self):
        svc = TimerService(callback=lambda label: None)
        svc.add_timer(0.01)
        svc.start()
        time.sleep(0.3)
        svc.stop()
        assert svc.get_remaining() == []
        assert svc.active_count() == 0

    def test_start_stop_idempotent(self):
        svc = TimerService()
        svc.start()
        svc.start()  # should not crash
        svc.stop()
        svc.stop()  # should not crash

    def test_fmt_minutes_seconds(self):
        assert TimerService._fmt(125) == "2 мин 5 сек"

    def test_fmt_minutes_only(self):
        assert TimerService._fmt(120) == "2 мин"

    def test_fmt_seconds_only(self):
        assert TimerService._fmt(45) == "45 сек"
