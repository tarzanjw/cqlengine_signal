from cqlengine import columns, BatchQuery
from cqlengine_signal import Model, subscribe
from . import ModelA, ModelA1, ModelA2
import random


def test_subscribe_decorator():
    @subscribe(ModelA.PreInsertSignal)
    def subsriber(event):
        pass

    assert subsriber in list(ModelA.PreInsertSignal.
                             receivers_for(Model.PreInsertSignal.ANY))


def test_model_metaclass():
    assert ModelA1.PreInsertSignal != ModelA.PreInsertSignal
    assert ModelA1.PreInsertSignal != ModelA2.PreInsertSignal


# def test_signals_is_readonly():
#     a1 = ModelA1()
#     try:
#         a1.PreInsertSignal = 'abc'
#         raise RuntimeError('Test failed')
#     except NotImplementedError:
#         pass
#     try:
#         ModelA1.PreInsertSignal = 'abc'
#         raise RuntimeError('Test failed')
#     except NotImplementedError:
#         pass


def test_send_all_signal_in_orders():
    a = ModelA1(id=random.randint(0x00, 0x8fffffff), name='dummy', foo='haha')
    received_signals = []

    @subscribe(ModelA1.PreInsertSignal)
    @subscribe(ModelA1.PreUpdateSignal)
    @subscribe(ModelA1.PreDeleteSignal)
    @subscribe(ModelA1.PostInsertSignal)
    @subscribe(ModelA1.PostUpdateSignal)
    @subscribe(ModelA1.PostDeleteSignal)
    def subscriber(event):
        """:type event: cqlengine_signal.ModelEvent"""
        assert event.instance == a
        received_signals.append(event.signal)

    a.save()
    a.update(name='updated Dummy')
    a.delete()

    assert received_signals == [
        ModelA1.PreInsertSignal,
        ModelA1.PostInsertSignal,
        ModelA1.PreUpdateSignal,
        ModelA1.PostUpdateSignal,
        ModelA1.PreDeleteSignal,
        ModelA1.PostDeleteSignal,
    ]


def test_send_signal_after_validation_only():
    from cqlengine.exceptions import ValidationError
    a1 = ModelA1()
    received_signals = []

    @subscribe(ModelA1.PreInsertSignal)
    @subscribe(ModelA1.PreUpdateSignal)
    def subscriber(event):
        """:type event: cqlengine_signal.ModelEvent"""
        raise ValueError('This event %s is not welcome', event)

    a1.id = 'abc'
    try:
        a1.save()
    except ValidationError:
        pass


def test_signal_inheritance():
    received_signals = []

    @subscribe(ModelA1.PreInsertSignal)
    @subscribe(ModelA.PreInsertSignal)
    def subscriber(event):
        """:type event: cqlengine_signal.ModelEvent"""
        received_signals.append(event.signal)

    a1 = ModelA1(id=random.randint(0x00, 0x8fffffff), name='dummy', foo='haha')
    a1.save()

    assert received_signals == [ModelA1.PreInsertSignal, ModelA.PreInsertSignal]

# def test_send_signal_with_batch():
#
#     received_signals = []
#
#     @subscribe(ModelA.PreSaveSignal)
#     @subscribe(ModelA.PostUpdateSignal)
#     def receiver_a(event):
#         """:type event: cqlengine_signal.ModelEvent"""
#         received_signals.append((event.signal, event.instance, event.batch))
#
#     @subscribe(ModelA.PostDeleteSignal)
#     def receiver_a_for_delete(event):
#         """:type event: cqlengine_signal.ModelEvent"""
#         received_signals.append((event.signal, event.instance, event.batch))
#
#     def assert_signal_came(signal, instance, batch):
#         for rs in received_signals:
#             if rs == (signal, instance, batch):
#                 return
#         assert False, 'Signal "%s" did not came' % (signal, )
#
#     def assert_signal_not_came(signal, instance, batch):
#         for rs in received_signals:
#             if rs == (signal, instance, batch):
#                 assert False, 'Signal "%s" is unexpected' % (signal, )
#
#     bq = BatchQuery()
#     a = ModelA()
#     a.batch(bq).save()
#
#     assert_signal_came(ModelA.PreSaveSignal, a, bq)
#     assert_signal_not_came(ModelA.PostSaveSignal, a, bq)
#
#     a.batch(bq).update(name='hehehe')
#
#     assert_signal_came(ModelA.PostUpdateSignal, a, bq)
#     assert_signal_not_came(ModelA.PreUpdateSignal, a, bq)
#
#     a.batch(bq).delete()
#
#     assert_signal_came(ModelA.PostDeleteSignal, a, bq)
#     assert_signal_not_came(ModelA.PreDeleteSignal, a, bq)
#
#     del bq