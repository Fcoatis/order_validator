from abc import ABC, abstractmethod
from app.models import Order, User

# --- Specification Pattern (O Motor de Regras) ---

class Specification(ABC):
    """Classe base para todas as regras de negócio."""

    @abstractmethod
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        pass

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)

    def __invert__(self):
        return NotSpecification(self)


class AndSpecification(Specification):
    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, order: Order, user: User) -> bool:
        return self.spec1.is_satisfied_by(order, user) and \
               self.spec2.is_satisfied_by(order, user)


class OrSpecification(Specification):
    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, order: Order, user: User) -> bool:
        return self.spec1.is_satisfied_by(order, user) or \
               self.spec2.is_satisfied_by(order, user)


class NotSpecification(Specification):
    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied_by(self, order: Order, user: User) -> bool:
        return not self.spec.is_satisfied_by(order, user)


# --- Regras de Negócio Atômicas (Os Blocos de Lego) ---

class IsUserPremium(Specification):
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        return user.is_premium

class IsUserAdmin(Specification):
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        return user.is_admin

class IsHighValueOrder(Specification):
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        return order.amount > 1000

class HasNoDiscount(Specification):
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        return not order.has_discount

class IsValidBulkOrder(Specification):
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        # Regra: Bulk é válido se usuário NÃO for trial
        is_bulk = (order.type == "bulk")
        is_not_trial = (not user.is_trial)
        return is_bulk and is_not_trial

class IsEuCompliant(Specification):
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        # Regra: Se usuário é EU, moeda DEVE ser EUR
        if user.region == "EU":
            return order.currency == "EUR"
        return False

class IsNonEuCompliant(Specification):
    def is_satisfied_by(self, order: Order, user: User) -> bool:
        # Regra: Se NÃO é EU, checar sanidade dos itens
        if user.region != "EU":
            for item in order.items:
                if item.price < 0:
                    return False
            return True
        return False