from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    price: float


@dataclass
class Order:
    amount: float
    has_discount: bool
    region: str
    currency: str
    type: str  # e.g. "bulk" or "normal"
    items: list[Item] = field(default_factory=list)


@dataclass
class User:
    is_premium: bool
    is_admin: bool
    is_trial: bool
    region: str


def approve_order(order: Order, user: User) -> str:
    """
    Função principal: Agora atua apenas como um 'Orquestrador'.
    Ela delega a decisão para funções especialistas.
    """
    try:
        if not user.is_premium:
            return _check_non_premium_rules(user)

        if order.amount <= 1000:
            return _check_low_value_rules(order, user)

        return _check_high_value_rules(order, user)

    except Exception:
        return "rejected"


# --- Funções Especialistas (Helpers Privados) ---

def _check_non_premium_rules(user: User) -> str:
    # Regra: Se não paga, só aprova se for Admin
    if user.is_admin:
        return "approved"
    return "rejected"


def _check_low_value_rules(order: Order, user: User) -> str:
    # Regra: Pedidos pequenos (<= 1000)
    # Só aprova atacado (bulk) se não for conta de teste (trial)
    if order.type == "bulk" and not user.is_trial:
        return "approved"
    return "rejected"


def _check_high_value_rules(order: Order, user: User) -> str:
    # Regra: Pedidos grandes (> 1000)

    # 1. Proibido desconto em valores altos
    if order.has_discount:
        return "rejected"

    # 2. Compliance Europa
    if user.region == "EU":
        if order.currency == "EUR":
            return "approved"
        return "rejected"

    # 3. Validação de Itens (Resto do Mundo)
    return _validate_items_integrity(order.items)


def _validate_items_integrity(items: list[Item]) -> str:
    for item in items:
        if item.price < 0:
            return "rejected"
    return "approved"