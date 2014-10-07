========================================================
cqlengine_signal: A limitted signal system for cqlengine
========================================================

More information about cqlengine signal, please read here: 

    https://github.com/cqlengine/cqlengine/issues/195

This package provides a way to subscriber cqlengine's model signal, there are 6
signals: Pre/Post for Insert/Update/Delete.

This package uses `blinker`_ to dispatch signal.

.. _blinker: https://pypi.python.org/pypi/blinker

1. `PreInsertSignal`
2. `PostInsertSignal`
3. `PreUpdateSignal`
4. `PostUpdateSignal`
5. `PreDeleteSignal`
6. `PostDeleteSignal`

From about issue, there are some points of this package:

1. Pre* Signal get fired after validation
2. Post* Signal get fired after the DML query executed.
3. For blink updates: there is not any signal.
4. **You should care about the batch when use Signal yourself** (you can use `event.batch`)


-----
Usage
-----

Declare model
=============

You need to use `cqlengine_signal.Model` instead of `cqlengine.models.Model`

.. code:: python

    from cqlengine_signal import Model

    class ModelA(Model):
        __table_name__ = 'model_a'    
        __polymorphic_key__ = 'a'
        id = columns.BigInt(primary_key=True)
        type = columns.Text(polymorphic_key=True)
        name = columns.Text()
    
    
    class ModelA1(ModelA):
        __polymorphic_key__ = 'a1'
        foo = columns.Text()
    
    
    class ModelA2(ModelA):
        __polymorphic_key__ = 'a2'   
        bar = columns.Text()
    
    
    class ModelB(Model):
        __table_name__ = 'model_b'    
        id = columns.BigInt(primary_key=True)
        name = columns.Text()


Subscribe signal
================

To subscriber a model's signal, you have 3 options: use decorator or use signal
as decorator or use signal directly.

.. code:: python
    
    from cqlengine_signal import subscribe

    @subscribe(ModelA.PostInsertSignal)
    def subscriber_for_model_a_post_insert(event):
        print(event)

    # or

    @ModelA.PreInsertSignal.connect
    def subscriber_for_model_a_pre_insert(event):
        print(event)

    # or

    def subscriber_for_model_a_pre_update(event):
        print(event)

    ModelA.PreUpdateSignal.connect(subscriber_for_model_a_pre_update)


A subscriber will be called with an argument, this argument's class is
`cqlengine_signal.signal.ModelEvent` class.

.. code:: python

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


Model inheritance
=================

When you have some models that inherite from other model, for above codes they
are `ModelA1` and `ModelA2`.

Whenever ModelA1's signal get fired, the same kind signal of `ModelA` (base
classes of `ModelA1`) get fired, too.


-------------------
Why is it limitted?
-------------------

Just because of:

1. No signals for blink updates.
2. Is designed for a small of use cases.
3. Developer has to care about batch themselves.