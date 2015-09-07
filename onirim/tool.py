from onirim import core

from etaprogress.progress import ProgressBar


def _progressed(iterator):
    """
    Yield items from iterator with a progress bar.
    """
    progress_bar = ProgressBar(len(iterator))
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
    for _ in _progressed(range(times)):
        core.run(actor, observer, content_factory())
