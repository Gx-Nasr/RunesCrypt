from . import theme as th


def ease_out(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def tween(master, steps, step_fn, delay=16, done=None):
    def frame(i):
        step_fn(ease_out(i / steps) if steps else 1.0)
        if i < steps:
            master.after(delay, lambda: frame(i + 1))
        elif done:
            done()

    frame(0)
