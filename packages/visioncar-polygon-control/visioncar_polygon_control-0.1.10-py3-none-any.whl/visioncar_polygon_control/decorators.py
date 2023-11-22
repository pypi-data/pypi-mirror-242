import threading


def debounce(delay):
    def decorator(original_fn):
        def fn(*args, **kwargs):
            def cb():
                fn._timer = None
                return original_fn(*args, **kwargs)

            if fn._timer:
                fn._timer.cancel()

            fn._timer = threading.Timer(delay, cb)
            fn._timer.start()

        fn._timer = None
        return fn

    return decorator
