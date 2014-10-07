import cqlengine.query


class DMLQuery(cqlengine.query.DMLQuery):

    def _send_signal(self, signal):
        """
        Send a signal that corresponding to current dmlquery
        :param cqlengine_signal.model.ModelSignal signal: signal to be sent
        """
        signal.send(self.instance)

    def save(self):
        self._send_signal(self.instance.PreInsertSignal)
        rs = super(DMLQuery, self).save()
        self._send_signal(self.instance.PostInsertSignal)
        return rs

    def update(self):
        self._send_signal(self.instance.PreUpdateSignal)
        rs = super(DMLQuery, self).update()
        self._send_signal(self.instance.PostUpdateSignal)
        return rs

    def delete(self):
        self._send_signal(self.instance.PreDeleteSignal)
        rs = super(DMLQuery, self).delete()
        self._send_signal(self.instance.PostDeleteSignal)
        return rs



