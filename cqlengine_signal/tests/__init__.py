from cqlengine_signal import Model
from cqlengine import columns


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