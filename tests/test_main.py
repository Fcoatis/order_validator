import pytest
from app.main import Item, Order, User, approve_order

# --- Auxiliares para os dados de teste ---
def create_standard_items():
    return [Item("Stock A", 100.0), Item("Stock B", 200.0)]

def create_negative_items():
    return [Item("Stock A", 100.0), Item("Bad Data", -50.0)]

# --- Bateria de Testes ---
@pytest.mark.parametrize(
    "case_description, user_kwargs, order_kwargs, expected_result",
    [
        # --- GRUPO A: Usuário NÃO Premium ---
        (
            "User Not Premium, Is Admin -> Approved",
            {"is_premium": False, "is_admin": True, "is_trial": False, "region": "US"},
            {"amount": 500, "has_discount": False, "region": "US", "currency": "USD", "type": "normal", "items": []},
            "approved"
        ),
        (
            "User Not Premium, Not Admin -> Rejected",
            {"is_premium": False, "is_admin": False, "is_trial": False, "region": "US"},
            {"amount": 500, "has_discount": False, "region": "US", "currency": "USD", "type": "normal", "items": []},
            "rejected"
        ),
        # --- GRUPO B1: Premium, Amount > 1000 ---
        (
            "Premium, >1000, Has Discount -> Rejected",
            {"is_premium": True, "is_admin": False, "is_trial": False, "region": "US"},
            {"amount": 1500, "has_discount": True, "region": "US", "currency": "USD", "type": "normal", "items": create_standard_items()},
            "rejected"
        ),
        (
            "Premium, >1000, No Discount, Not EU, Negative Price Item -> Rejected",
            {"is_premium": True, "is_admin": False, "is_trial": False, "region": "US"},
            {"amount": 1500, "has_discount": False, "region": "US", "currency": "USD", "type": "normal", "items": create_negative_items()},
            "rejected"
        ),
        (
            "Premium, >1000, No Discount, Not EU, Valid Items -> Approved",
            {"is_premium": True, "is_admin": False, "is_trial": False, "region": "BR"},
            {"amount": 1500, "has_discount": False, "region": "US", "currency": "BRL", "type": "normal", "items": create_standard_items()},
            "approved"
        ),
        (
            "Premium, >1000, No Discount, User EU, Currency NOT EUR -> Rejected",
            {"is_premium": True, "is_admin": False, "is_trial": False, "region": "EU"},
            {"amount": 1500, "has_discount": False, "region": "EU", "currency": "USD", "type": "normal", "items": create_standard_items()},
            "rejected"
        ),
        (
            "Premium, >1000, No Discount, User EU, Currency EUR -> Approved",
            {"is_premium": True, "is_admin": False, "is_trial": False, "region": "EU"},
            {"amount": 1500, "has_discount": False, "region": "EU", "currency": "EUR", "type": "normal", "items": create_standard_items()},
            "approved"
        ),
        # --- GRUPO B2: Premium, Amount <= 1000 ---
        (
            "Premium, <=1000, Bulk, Not Trial -> Approved",
            {"is_premium": True, "is_admin": False, "is_trial": False, "region": "US"},
            {"amount": 900, "has_discount": False, "region": "US", "currency": "USD", "type": "bulk", "items": []},
            "approved"
        ),
        (
            "Premium, <=1000, Bulk, Is Trial -> Rejected",
            {"is_premium": True, "is_admin": False, "is_trial": True, "region": "US"},
            {"amount": 900, "has_discount": False, "region": "US", "currency": "USD", "type": "bulk", "items": []},
            "rejected"
        ),
        (
            "Premium, <=1000, Type Normal (Not Bulk) -> Rejected",
            {"is_premium": True, "is_admin": False, "is_trial": False, "region": "US"},
            {"amount": 900, "has_discount": False, "region": "US", "currency": "USD", "type": "normal", "items": []},
            "rejected"
        ),
    ]
)
def test_approve_order_scenarios(case_description, user_kwargs, order_kwargs, expected_result):
    user = User(**user_kwargs)
    order = Order(**order_kwargs)
    result = approve_order(order, user)
    assert result == expected_result, f"Falha no cenário: {case_description}"

def test_approve_order_exception_handling():
    # Testa resiliência (try/except)
    user = User(is_premium=True, is_admin=False, is_trial=False, region="US")
    order = Order(amount=1500, has_discount=False, region="US", currency="USD", type="normal", items=None)
    result = approve_order(order, user)
    assert result == "rejected"