class DisciplineEnforcer:
    def can_modify(self, locked: bool) -> bool:
        return not locked
