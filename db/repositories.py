from datetime import datetime, time, timedelta
from decimal import Decimal

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Expense, User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_or_create(self, telegram_id: int) -> User:
        user = await self.session.scalar(select(User).where(User.telegram_id == telegram_id))
        if user is not None:
            return user

        user = User(telegram_id=telegram_id)
        self.session.add(user)
        await self.session.flush()
        return user

    async def set_language(self, telegram_id: int, language_code: str) -> User:
        user = await self.get_or_create(telegram_id)
        user.language_code = language_code
        await self.session.flush()
        return user


class ExpenseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        user_id: int,
        amount: Decimal,
        description: str,
        category_name: str,
    ) -> Expense:
        expense = Expense(
            user_id=user_id,
            amount=amount,
            description=description,
            category_name=category_name,
        )
        self.session.add(expense)
        await self.session.flush()
        return expense

    async def delete_last(self, user_id: int) -> Expense | None:
        expense = await self.session.scalar(
            select(Expense)
            .where(Expense.user_id == user_id)
            .order_by(Expense.spent_at.desc(), Expense.id.desc())
            .limit(1)
        )
        if expense is None:
            return None

        await self.session.execute(delete(Expense).where(Expense.id == expense.id))
        return expense

    async def get_totals(self, user_id: int, now: datetime | None = None) -> dict[str, Decimal]:
        current = now or datetime.now()
        today_start = datetime.combine(current.date(), time.min)
        week_start = today_start - timedelta(days=current.weekday())
        month_start = today_start.replace(day=1)

        return {
            "today": await self._sum_since(user_id, today_start),
            "week": await self._sum_since(user_id, week_start),
            "month": await self._sum_since(user_id, month_start),
        }

    async def _sum_since(self, user_id: int, start: datetime) -> Decimal:
        result = await self.session.scalar(
            select(func.coalesce(func.sum(Expense.amount), 0)).where(
                Expense.user_id == user_id,
                Expense.spent_at >= start,
            )
        )
        return Decimal(result)
