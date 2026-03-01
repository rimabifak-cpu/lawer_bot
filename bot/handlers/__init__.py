import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.handlers.start import register_start_handlers
from bot.handlers.services import register_services_handlers
from bot.handlers.profile import register_profile_handlers
from bot.handlers.send_case import register_send_case_handlers
from bot.handlers.revenue import register_revenue_handlers
from bot.handlers.how_to_earn import register_how_to_earn_handlers
from bot.handlers.case_messages import register_case_messages_handlers

from bot.handlers.faq import register_faq_handlers
from bot.handlers.legal_services import register_legal_services_handlers
from bot.handlers.service_details import register_service_detail_handlers

def register_handlers(dp):
    register_start_handlers(dp)
    register_services_handlers(dp)
    register_profile_handlers(dp)
    register_send_case_handlers(dp)
    register_revenue_handlers(dp)
    register_how_to_earn_handlers(dp)
    register_case_messages_handlers(dp)

    register_faq_handlers(dp)
    register_legal_services_handlers(dp)
    register_service_detail_handlers(dp)