from django.urls import path
from .views import SDPView, IceCandidateView, ChatMessageView, AudioCallInitiationView

urlpatterns = [
    path('sdp/<int:room_id>/', SDPView.as_view(), name='sdp'),
    path('ice-candidate/<int:room_id>/', IceCandidateView.as_view(), name='ice-candidate'),
    path('chat-message/<int:room_id>/', ChatMessageView.as_view(), name='chat-message'),
    path('audio-call-initiation/', AudioCallInitiationView.as_view(), name='audio-call-initiation'),
]
