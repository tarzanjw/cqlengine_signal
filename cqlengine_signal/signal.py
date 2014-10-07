import blinker
import six


class ModelSignal(blinker.Signal):
    """
    Class for signals for the Model
    """

    def __init__(self, model, name, parent_signal=None, doc=None):
        """ Create a install of a signal for a model
        :param Model model: the model to create signal on
        :param string name: name of signal
        :param ModelSignal parent_signal: the same type signal of parent model
        """
        self.model = model
        self.name = name
        self.parent_signal = parent_signal
        super(ModelSignal, self).__init__(doc)

    def send(self, instance, **kwargs):
        """ This will make parent's signals will be sent with this signal """
        event = ModelEvent(instance, self)

        rs = super(ModelSignal, self).send(event, **kwargs)
        if self.parent_signal is not None:
            rs.extend(self.parent_signal.send(instance, **kwargs))
        return rs

    def __unicode__(self):
        return six.text_type('%s.%s' % (self.model.__name__, self.name))

    def __str__(self):
        return str(self.__unicode__())

    def __repr__(self):
        return self.__str__()


class ModelEvent(object):
    """ Class for the event to be sent whenever the model signal is fired
    """
    def __init__(self, instance, signal):
        """
        Create new event for a signal
        :param Model instance: the instance of Model that its action raises signal
        :param ModelSignal signal: the signal that makes event
        """
        self.instance = instance
        self.signal = signal

    @property
    def model(self):
        """ Get the model that owns current signal
        :return class:
        """
        return self.signal.model

    @property
    def batch(self):
        """ Get the batch that event's instance is currenly on
        """
        return self.instance._batch

    def __unicode__(self):
        return six.text_type('%r.%s' % (self.instance, self.signal.name))

    def __str__(self):
        return str(self.__unicode__())