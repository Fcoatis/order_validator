from app.models import Order, User
from app.rules import (
    IsUserPremium, IsUserAdmin, IsHighValueOrder,
    HasNoDiscount, IsValidBulkOrder, IsEuCompliant, IsNonEuCompliant
)

def approve_order(order: Order, user: User) -> str:
    try:
        # Montagem das Políticas
        non_premium_policy = (~IsUserPremium() & IsUserAdmin())

        low_value_policy = (IsUserPremium() & ~IsHighValueOrder() & IsValidBulkOrder())

        high_value_compliance = (IsEuCompliant() | IsNonEuCompliant())
        high_value_policy = (
            IsUserPremium() &
            IsHighValueOrder() &
            HasNoDiscount() &
            high_value_compliance
        )

        final_policy = non_premium_policy | low_value_policy | high_value_policy

        if final_policy.is_satisfied_by(order, user):
            return "approved"

        return "rejected"

    except Exception:
        return "rejected"