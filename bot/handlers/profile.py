import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database.database import get_db
from database.models import User, PartnerProfile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Импортируем состояния
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from states.states import ProfileStates

# Импортируем настройки
from config.settings import settings

router = Router()

@router.callback_query(F.data == "profile_update")
async def profile_update_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик для обновления профиля партнера
    """
    await callback_query.message.answer("Введите ваше ФИО:")
    await state.set_state(ProfileStates.waiting_for_full_name)
    await callback_query.answer()

@router.message(ProfileStates.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода ФИО
    """
    await state.update_data(full_name=message.text)
    await message.answer("Введите название вашей компании:")
    await state.set_state(ProfileStates.waiting_for_company_name)

@router.message(ProfileStates.waiting_for_company_name)
async def process_company_name(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода названия компании
    """
    await state.update_data(company_name=message.text)
    await message.answer("Введите ваш телефон:")
    await state.set_state(ProfileStates.waiting_for_phone)

@router.message(ProfileStates.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода телефона
    """
    await state.update_data(phone=message.text)
    await message.answer("Введите ваш email:")
    await state.set_state(ProfileStates.waiting_for_email)

@router.message(ProfileStates.waiting_for_email)
async def process_email(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода email
    """
    await state.update_data(email=message.text)
    await message.answer("Введите вашу специализацию (например: НДС, зарплата, отчетность):")
    await state.set_state(ProfileStates.waiting_for_specialization)

@router.message(ProfileStates.waiting_for_specialization)
async def process_specialization(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода специализации
    """
    await state.update_data(specialization=message.text)
    await message.answer("Введите ваш опыт в годах:")
    await state.set_state(ProfileStates.waiting_for_experience)

@router.message(ProfileStates.waiting_for_experience)
async def process_experience(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода опыта
    """
    try:
        experience = int(message.text)
        await state.update_data(experience=experience)
        
        # Получаем все данные
        data = await state.get_data()
        
        # Сохраняем в базу данных
        async with get_db() as db:
            # Находим пользователя
            result = await db.execute(select(User).filter(User.telegram_id == message.from_user.id))
            user = result.scalar_one_or_none()
            
            if user:
                # Проверяем, существует ли уже профиль
                result = await db.execute(select(PartnerProfile).filter(PartnerProfile.user_id == user.id))
                profile = result.scalar_one_or_none()
                
                if profile:
                    # Обновляем существующий профиль
                    profile.full_name = data['full_name']
                    profile.company_name = data['company_name']
                    profile.phone = data['phone']
                    profile.email = data['email']
                    profile.specialization = data['specialization']
                    profile.experience = data['experience']
                else:
                    # Создаем новый профиль
                    new_profile = PartnerProfile(
                        user_id=user.id,
                        full_name=data['full_name'],
                        company_name=data['company_name'],
                        phone=data['phone'],
                        email=data['email'],
                        specialization=data['specialization'],
                        experience=data['experience']
                    )
                    db.add(new_profile)
                
                await db.commit()
        
        await message.answer("Ваш профиль успешно обновлен!")
        
        # Отправляем уведомление в чат -1003899118823
        try:
            profile_notification = (
                f"👤 ID пользователя: {message.from_user.id}\n"
                f"🔗 Ссылка: https://t.me/{message.from_user.username or 'N/A'}\n"
                f"📝 ФИО: {data['full_name']}\n"
                f"🏢 Компания: {data['company_name']}\n"
                f"📞 Телефон: {data['phone']}\n"
                f"✉️ Email: {data['email']}\n"
                f"💼 Специализация: {data['specialization']}\n"
                f"📅 Опыт: {data['experience']} лет"
            )
            await message.bot.send_message(-1003899118823, profile_notification)
        except Exception as e:
            print(f"Ошибка при отправке уведомления о профиле в чат: {e}")
        
    except ValueError:
        await message.answer("Пожалуйста, введите число лет опыта.")
        return
    
    await state.clear()

@router.callback_query(F.data == "profile_view")
async def profile_view_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик для просмотра профиля партнера
    """
    user_id = callback_query.from_user.id
    
    async with get_db() as db:
        # Находим пользователя
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            # Получаем профиль партнера отдельно, чтобы избежать lazy loading ошибки
            profile_result = await db.execute(select(PartnerProfile).filter(PartnerProfile.user_id == user.id))
            profile = profile_result.scalar_one_or_none()
            
            if profile:
                profile_info = (
                    f"<b>Ваш профиль партнера:</b>\n\n"
                    f"ФИО: {profile.full_name}\n"
                    f"Компания: {profile.company_name}\n"
                    f"Телефон: {profile.phone}\n"
                    f"Email: {profile.email}\n"
                    f"Специализация: {profile.specialization}\n"
                    f"Опыт: {profile.experience} лет\n"
                    f"Согласие на передачу данных: {'Да' if profile.consent_to_share_data else 'Нет'}"
                )
            else:
                profile_info = "Вы еще не заполнили свой профиль партнера. Нажмите 'Заполнить/обновить мои данные'."
        else:
            profile_info = "Ошибка: пользователь не найден в системе."
    
    from bot.keyboards.keyboards import get_partner_profile_keyboard
    await callback_query.message.edit_text(profile_info, reply_markup=get_partner_profile_keyboard())
    await callback_query.answer()

@router.callback_query(F.data == "profile_consent")
async def profile_consent_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик для согласия на передачу данных
    """
    user_id = callback_query.from_user.id
    
    async with get_db() as db:
        # Находим пользователя
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            # Получаем профиль партнера отдельно, чтобы избежать lazy loading ошибки
            profile_result = await db.execute(select(PartnerProfile).filter(PartnerProfile.user_id == user.id))
            profile = profile_result.scalar_one_or_none()
            
            if profile:
                # Меняем статус согласия
                profile.consent_to_share_data = not profile.consent_to_share_data
                await db.commit()
                
                status = "да" if profile.consent_to_share_data else "нет"
                response = f"Вы {status} согласны на передачу ваших данных клиентам."
            else:
                response = "Для изменения согласия на передачу данных, сначала заполните свой профиль."
        else:
            response = "Ошибка: пользователь не найден в системе."
    
    from bot.keyboards.keyboards import get_partner_profile_keyboard
    await callback_query.message.edit_text(response, reply_markup=get_partner_profile_keyboard())
    await callback_query.answer()


@router.callback_query(F.data == "referral_program")
async def referral_program_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик для раздела реферальной программы
    """
    user_id = callback_query.from_user.id
    
    async with get_db() as db:
        # Находим пользователя
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            # Получаем или создаем реферальный код для пользователя
            from database.models import ReferralLink, ReferralRelationship, ReferralMonthlyStats, PartnerRevenue
            from bot.utils.referral_calculator import calculate_referral_commission
            from datetime import datetime
            
            result = await db.execute(select(ReferralLink).filter(ReferralLink.partner_id == user.id))
            referral_link = result.scalar_one_or_none()
            
            if not referral_link:
                import secrets
                referral_code = secrets.token_urlsafe(8)[:8].upper()  # 8-символьный код
                
                # Проверяем, что такой код не существует
                while True:
                    result = await db.execute(select(ReferralLink).filter(ReferralLink.referral_code == referral_code))
                    existing = result.scalar_one_or_none()
                    if not existing:
                        break
                    referral_code = secrets.token_urlsafe(8)[:8].upper()
                
                referral_link = ReferralLink(
                    partner_id=user.id,
                    referral_code=referral_code
                )
                db.add(referral_link)
                await db.commit()
                await db.refresh(referral_link)
            
            # Получаем список рефералов
            referrals_result = await db.execute(
                select(ReferralRelationship).filter(ReferralRelationship.referrer_id == user.id)
            )
            referrals = referrals_result.scalars().all()
            
            # Текущий месяц и год
            current_month = datetime.now().month
            current_year = datetime.now().year
            month_names = {
                1: 'январе', 2: 'феврале', 3: 'марте', 4: 'апреле',
                5: 'мае', 6: 'июне', 7: 'июле', 8: 'августе',
                9: 'сентябре', 10: 'октябре', 11: 'ноябре', 12: 'декабре'
            }
            
            # Считаем выручку каждого реферала за текущий месяц
            referral_stats = []
            total_revenue = 0
            
            for referral in referrals:
                # Получаем информацию о реферале
                referred_user_result = await db.execute(select(User).filter(User.id == referral.referred_id))
                referred_user = referred_user_result.scalar_one_or_none()
                
                if referred_user:
                    # Получаем выручку реферала за текущий месяц
                    from sqlalchemy import func
                    revenue_result = await db.execute(
                        select(func.sum(PartnerRevenue.amount)).filter(
                            PartnerRevenue.partner_id == referred_user.id,
                            func.extract('month', PartnerRevenue.created_at) == current_month,
                            func.extract('year', PartnerRevenue.created_at) == current_year
                        )
                    )
                    referral_revenue = revenue_result.scalar() or 0
                    total_revenue += referral_revenue
                    
                    # Формируем имя реферала
                    user_name = referred_user.first_name or ""
                    if referred_user.last_name:
                        user_name += f" {referred_user.last_name}"
                    if referred_user.username:
                        user_name += f" (@{referred_user.username})"
                    
                    referral_stats.append({
                        'name': user_name.strip() or f"ID {referred_user.telegram_id}",
                        'revenue': referral_revenue
                    })
            
            # Рассчитываем процент комиссии
            commission_percent = await calculate_referral_commission(total_revenue)
            commission_amount = round(total_revenue * (commission_percent / 100))
            
            # Формируем информацию о реферальной программе
            referral_info = (
                f"🔗 <b>Реферальная программа</b>\n\n"
                f"📋 Ваша реферальная ссылка:\n"
                f"<code>https://t.me/legaldecision_bot?start={referral_link.referral_code}</code>\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📊 <b>Ваша статистика за {month_names[current_month]} {current_year}:</b>\n\n"
                f"• Всего рефералов: {len(referrals)}\n"
                f"• Общая выручка: {total_revenue:,} ₽\n"
                f"• Текущий процент: {commission_percent}%\n"
                f"• Ваше вознаграждение: {commission_amount:,} ₽\n\n"
            )
            
            # Добавляем список рефералов с выручкой
            if referral_stats:
                referral_info += f"━━━━━━━━━━━━━━━━━━━━\n\n"
                referral_info += f"👥 <b>Ваши рефералы в этом месяце:</b>\n\n"
                
                for idx, stat in enumerate(referral_stats, 1):
                    referral_info += f"{idx}. {stat['name']}\n"
                    referral_info += f"   Выручка: {stat['revenue']:,} ₽\n\n"
            else:
                referral_info += f"━━━━━━━━━━━━━━━━━━━━\n\n"
                referral_info += f"👥 У вас пока нет рефералов.\n"
                referral_info += f"Пригласите партнёров по вашей ссылке!\n\n"
            
            # Добавляем информацию о прогрессивной шкале
            referral_info += (
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📈 <b>Условия программы:</b>\n\n"
                f"• До 250 000 ₽ — 0.5%\n"
                f"• 250 000 - 1 000 000 ₽ — 1%\n"
                f"• От 1 000 000 ₽ — 2%\n\n"
                f"Процент применяется ко всей сумме выручки!\n\n"
                f"Выплаты: 10 числа каждого месяца"
            )
        else:
            referral_info = "Произошла ошибка при получении данных реферальной программы."
    
    from bot.keyboards.keyboards import get_referral_program_keyboard
    await callback_query.message.edit_text(referral_info, reply_markup=get_referral_program_keyboard(), parse_mode="HTML")
    await callback_query.answer()


@router.callback_query(F.data == "copy_referral_link")
async def copy_referral_link_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик для копирования реферальной ссылки
    """
    user_id = callback_query.from_user.id
    
    async with get_db() as db:
        # Находим пользователя
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            from database.models import ReferralLink
            result = await db.execute(select(ReferralLink).filter(ReferralLink.partner_id == user.id))
            referral_link = result.scalar_one_or_none()
            
            if referral_link:
                referral_url = f"https://t.me/legaldecision_bot?start={referral_link.referral_code}"
                
                # Отправляем ссылку в отдельном сообщении для удобного копирования
                await callback_query.message.answer(
                    f"📋 <b>Ваша реферальная ссылка:</b>\n\n"
                    f"<code>{referral_url}</code>\n\n"
                    f"Нажмите на ссылку выше, чтобы скопировать её.",
                    parse_mode="HTML"
                )
                await callback_query.answer("Ссылка отправлена в сообщении выше!")
            else:
                await callback_query.answer("Ошибка: реферальная ссылка не найдена.")
        else:
            await callback_query.answer("Ошибка: пользователь не найден.")


@router.callback_query(F.data == "payout_history")
async def payout_history_handler(callback_query: CallbackQuery) -> None:
    """
    Обработчик для просмотра истории выплат
    """
    user_id = callback_query.from_user.id
    
    async with get_db() as db:
        # Находим пользователя
        result = await db.execute(select(User).filter(User.telegram_id == user_id))
        user = result.scalar_one_or_none()
        
        if user:
            from database.models import ReferralPayout
            
            # Получаем историю выплат
            payouts_result = await db.execute(
                select(ReferralPayout)
                .filter(ReferralPayout.referrer_id == user.id)
                .order_by(ReferralPayout.created_at.desc())
                .limit(20)
            )
            payouts = payouts_result.scalars().all()
            
            if payouts:
                history_text = "📊 <b>История выплат:</b>\n\n"
                
                status_emojis = {
                    'pending': '⏳',
                    'paid': '✅',
                    'cancelled': '❌'
                }
                
                status_names = {
                    'pending': 'Ожидает',
                    'paid': 'Выплачено',
                    'cancelled': 'Отменено'
                }
                
                for payout in payouts:
                    emoji = status_emojis.get(payout.status, '❓')
                    status = status_names.get(payout.status, payout.status)
                    paid_date = payout.paid_at.strftime('%d.%m.%Y') if payout.paid_at else '-'
                    
                    history_text += (
                        f"{emoji} <b>{payout.amount:,} ₽</b>\n"
                        f"   Период: {payout.month:02d}.{payout.year}\n"
                        f"   Статус: {status}\n"
                        f"   Дата выплаты: {paid_date}\n\n"
                    )
            else:
                history_text = (
                    "📊 <b>История выплат:</b>\n\n"
                    "У вас пока нет выплат.\n"
                    "Привлекайте партнёров и получайте вознаграждение!"
                )
        else:
            history_text = "Ошибка: пользователь не найден."
    
    from bot.keyboards.keyboards import get_referral_program_keyboard
    await callback_query.message.edit_text(history_text, reply_markup=get_referral_program_keyboard(), parse_mode="HTML")
    await callback_query.answer()

def register_profile_handlers(dp):
    dp.include_router(router)