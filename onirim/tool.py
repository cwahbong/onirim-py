from onirim import core

from etaprogress.progress import ProgressBar


def _progressed(iterator):
    progress_bar = ProgressBar(len(iterator))
    print(progress_bar, end="\r")
    for i in iterator:
        yield i
        progress_bar.numerator += 1
        print(progress_bar, end="\r")
    print()


def progressed_run(times, actor, observer, content_factory):
    for _ in _progressed(range(times)):
        core.run(actor, observer, content_factory())
