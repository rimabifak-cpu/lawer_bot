"""
Модуль для расчета вознаграждения в реферальной системе

Условия вознаграждения:
- До 250 000 руб. — 0.5%
- От 250 000 до 1 000 000 руб. — 1%
- От 1 000 000 руб. — 2%
"""


async def calculate_referral_commission(total_revenue: int) -> float:
    """
    Рассчитывает процент вознаграждения партнера в зависимости от общей выручки от рефералов
    
    Args:
        total_revenue: Общая выручка от рефералов за месяц в рублях
    
    Returns:
        Процент вознаграждения (в виде числа, например 0.5, 1.0, 2.0)
    """
    if total_revenue < 250000:
        return 0.5  # 0.5%
    elif total_revenue < 1000000:
        return 1.0  # 1.0%
    else:
        return 2.0  # 2.0%


async def calculate_referral_bonus(referrer_id: int, referred_revenue: int) -> dict:
    """
    Рассчитывает бонус для партнера за привлечение реферала
    
    Args:
        referrer_id: ID партнера, который привлек реферала
        referred_revenue: Выручка от реферала
    
    Returns:
        Словарь с информацией о бонусе
    """
    commission_percent = await calculate_referral_commission(referred_revenue)
    commission_amount = round(referred_revenue * (commission_percent / 100))
    
    return {
        "referrer_id": referrer_id,
        "referred_revenue": referred_revenue,
        "commission_percent": commission_percent,
        "commission_amount": commission_amount
    }