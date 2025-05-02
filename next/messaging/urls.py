from django.urls import path
from next.messaging import views

urlpatterns = [
    path('chats/', views.show_chats, name='show-chats'),
    path('chats/<int:chat_id>/messages/', views.show_chat_messages, name='show-chat-messages'),
    path('chats/send-message/', views.send_message, name='send-message'),
    path('chats/<int:chat_id>/delete/', views.delete_chat, name='delete-chat'),
]
