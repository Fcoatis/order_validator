import pytest
from hypothesis import given, strategies as st
from app.models import Item, Order, User
from app.main import approve_order

# --- 1. Geradores de Dados (Onde nasce o Caos) ---

# Gera textos aleatórios (incluindo emojis, caracteres nulos, etc)
st_text = st.text()

# Gera floats perigosos (NaN, Infinito, Negativos)
st_floats = st.floats(allow_nan=True, allow_infinity=True)

# Monta Itens aleatórios
st_items = st.builds(
    Item,
    name=st_text,
    price=st_floats
)

# Monta Usuários aleatórios
st_users = st.builds(
    User,
    is_premium=st.booleans(),
    is_admin=st.booleans(),
    is_trial=st.booleans(),
    region=st.sampled_from(["US", "EU", "BR", "CN", "Unknown", ""])
)

# Monta Pedidos aleatórios (A parte mais crítica)
st_orders = st.builds(
    Order,
    amount=st_floats,
    has_discount=st.booleans(),
    region=st.sampled_from(["US", "EU", "BR", "CN", "Unknown", ""]),
    currency=st.sampled_from(["USD", "EUR", "BRL", "BTC", "ETH", "Invalid"]),
    type=st.sampled_from(["normal", "bulk", "unknown"]),
    items=st.lists(st_items, min_size=0, max_size=20) # De 0 a 20 itens
)

# --- 2. Os Testes de Propriedade ---

@given(user=st_users, order=st_orders)
def test_system_stability_invariant(user, order):
    """
    PROPRIEDADE: Estabilidade
    Não importa o lixo que entre (NaN, Infinito), o sistema NÃO pode crashar (Exception).
    Deve sempre retornar uma decisão válida ('approved' ou 'rejected').
    """
    try:
        result = approve_order(order, user)
        assert result in ["approved", "rejected"]
    except Exception as e:
        # Se entrar aqui, o Hypothesis achou um bug que crasha o app!
        pytest.fail(f"CRASH DETECTADO! Input quebrou o sistema: {e}")

@given(user=st_users, order=st_orders)
def test_btc_safety_invariant(user, order):
    """
    PROPRIEDADE: Segurança BTC
    Se for BTC e valor > 2000, só aprova se for Premium.
    O Hypothesis vai tentar achar um caso onde isso falha.
    """
    # Executa a lógica
    result = approve_order(order, user)

    # Validação da Invariante
    is_risky_btc = (order.currency == "BTC" and order.amount > 2000)

    if is_risky_btc and not user.is_premium:
        # Se for arriscado e não for premium, TEM que rejeitar.
        # Se aprovou, temos uma falha grave de segurança.
        assert result == "rejected", \
            f"FALHA DE SEGURANÇA! BTC Alto Valor aprovado para não-premium. Order: {order}"