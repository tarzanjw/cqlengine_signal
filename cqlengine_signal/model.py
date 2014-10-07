import logging
import blinker
import cqlengine.models
from cqlengine_signal.query import DMLQuery
from cqlengine_signal.signal import ModelSignal
import six



class ModelMetaClass(cqlengine.models.ModelMetaClass):
    """ Metaclass for Model, use to control the signal create progress
    """
    def __new__(cls, name, bases, attrs):
        # create the class normally
        # create the signal for new class
        klass = super(ModelMetaClass, cls).__new__(cls, name, bases, attrs)
        for sig_name in ['PreInsertSignal', 'PostInsertSignal',
                         'PreUpdateSignal', 'PostUpdateSignal',
                         'PreDeleteSignal', 'PostDeleteSignal', ]:
            parent_klass = bases[0]
            try:
                parent_sig = getattr(parent_klass, sig_name)
                if not isinstance(parent_sig, ModelSignal):
                    logging.getLogger(__name__).warn('%s.%s is not ModelSignal instance',
                                                     parent_klass, sig_name)
                    parent_sig = None
            except AttributeError:
                parent_sig = None
            sig = ModelSignal(klass, sig_name, parent_sig)
            setattr(klass, sig_name, sig)
        return klass

    # PreInsertSignal = _ModelSignalDescriptor('PreInsertSignal')


@six.add_metaclass(ModelMetaClass)
class Model(cqlengine.models.Model):
    """
    Base class for all the models that want to fire signal during its editing
    progress.

    Supported signals for 3 actions: update, save, delete
    The Pre* signal is sent after validation and before dmlquery execution
    The Post* signal is sent after dmlquery execution
    """

    __abstract__ = True
    __dmlquery__ = DMLQuery

    # use to code intelligent sense
    PreInsertSignal = blinker.Signal()
    PostInsertSignal = blinker.Signal()
    PreUpdateSignal = blinker.Signal()
    PostUpdateSignal = blinker.Signal()
    PreDeleteSignal = blinker.Signal()
    PostDeleteSignal = blinker.Signal()