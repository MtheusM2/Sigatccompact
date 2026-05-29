from controle_ativos.database import init_db


class _FakeCursor:
    def __init__(self):
        self.executed = []
        self.fetchall_calls = 0
        self.nextset_calls = 0
        self._result_sets = [True, False]
        self.with_rows = False

    def execute(self, sql):
        self.executed.append(sql)
        self.with_rows = sql.strip().upper().startswith("SELECT")

    def fetchall(self):
        self.fetchall_calls += 1
        self.with_rows = False
        return []

    def nextset(self):
        self.nextset_calls += 1
        if not self._result_sets:
            return False

        has_next = self._result_sets.pop(0)
        self.with_rows = bool(has_next)
        return has_next


def test_executar_sql_texto_drena_resultados_pendentes():
    cur = _FakeCursor()

    init_db._executar_sql_texto(cur, "SELECT 1; ALTER TABLE ativos ADD COLUMN teste INT")

    assert cur.executed == ["SELECT 1", "ALTER TABLE ativos ADD COLUMN teste INT"]
    assert cur.fetchall_calls == 2
    assert cur.nextset_calls == 3
