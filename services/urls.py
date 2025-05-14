from django.urls import path
from . import views


urlpatterns = [
    # web design
    path('web-design/', views.web_design_view, name='web_design'),
    path('web-design/portfolio', views.web_design_portfolio_view, name='web_design_portfolio'),
    path('web-design/order-form', views.web_design_order_form_view, name='web_design_order_form'),
    # telegram bot
    path('telegram-bot/', views.telegram_bot_view, name='telegram_bot'),
    path('telegram-bot/portfolio', views.telegram_bot_portfolio_view, name='telegram_bot_portfolio'),
    path('web-design/order-form', views.telegram_bot_order_form_view, name='telegram_bot_order_form'),
    # trading tools
    # ...
]