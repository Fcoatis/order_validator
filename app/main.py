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
    Refatoração 1: Guard Clauses (Achatamento da Lógica)
    """
    try:
        # 1. Regra para NÃO Premium (Simples e Direta)
        if not user.is_premium:
            if user.is_admin:
                return "approved"
            return "rejected"

        # --- Daqui para baixo, sabemos que o usuário É Premium ---

        # 2. Regra para Pedidos de Baixo Valor (<= 1000)
        if order.amount <= 1000:
            if order.type == "bulk" and not user.is_trial:
                return "approved"
            return "rejected"

        # --- Daqui para baixo, sabemos que é Premium E Alto Valor (> 1000) ---

        # 3. Descontos em Alto Valor são proibidos
        if order.has_discount:
            return "rejected"

        # 4. Regras Regionais (Geográficas)
        if user.region == "EU":
            # Compliance Europa
            if order.currency == "EUR":
                return "approved"
            return "rejected"
        else:
            # Regras Globais (Fora da UE): Validação de Sanidade dos Itens
            for item in order.items:
                if item.price < 0:
                    return "rejected"
            return "approved"

    except Exception:
        # Resiliência: Qualquer erro de dados rejeita o pedido
        return "rejected"