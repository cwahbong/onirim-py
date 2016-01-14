from onirim import core

from etaprogress.progress import ProgressBar


def progressed(iterator, length=None):
    """
    Yield items from iterator with a progress bar.
    """
    if length is None:
        length = len(iterator)
    progress_bar = ProgressBar(length)
    print(progress_bar, end="\r")
    for i in iterator:
        yield i
        progress_bar.numerator += 1
        print(progress_bar, end="\r")
    print()


def progressed_run(times, actor, observer, content_factory):
    """
    Run Onirim `times` times with a progress bar.

    Parameters:
        actor: The actor for :py:class:`onirim.core.Core`.
        observer: The observer for :py:class:`onirim.core.Core`.
        content_factory: Factory function that creates a new content for
            :py:class:`onirim.core.Core`.
    """
    for _ in progressed(range(times)):
        core.run(actor, observer, content_factory())
