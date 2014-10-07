import blinker
from cqlengine_signal.signal import ModelSignal


def subscribe(signal, sender=blinker.ANY, weak=True):
    """
    Alias for signal.connect
    :param Signal signal: signal to be subscribed
    :param ModelSignal sender: the record to be subscribe on
    """
    def subscriber_decorator(subscriber):
        signal.connect(subscriber, sender, weak)
        return subscriber
    assert isinstance(signal, ModelSignal), 'You can subscribe instance of ' \
                                            'cqlengine_signal.ModelSignal only, ' \
                                            'not %s' % signal
    return subscriber_decorator