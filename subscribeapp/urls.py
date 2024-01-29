from django.urls import path

from subscribeapp.views import P_SubscriptionView, P_SubscriptionListView, A_SubscriptionView, A_SubscriptionListView, Per_SubscriptionView, Per_SubscriptionListView, CombinedSubscriptionListView
app_name = 'subscribeapp'

urlpatterns = [
    path('P_subscribe/', P_SubscriptionView.as_view(), name='P_subscribe'),
    path('P_list/', P_SubscriptionListView.as_view(), name='P_list'),
    path('A_subscribe/', A_SubscriptionView.as_view(), name='A_subscribe'),
    path('A_list/', A_SubscriptionListView.as_view(), name='A_list'),
    path('Per_subscribe/', Per_SubscriptionView.as_view(), name='Per_subscribe'),
    path('Per_list/', Per_SubscriptionListView.as_view(), name='Per_list'),
    
    path('C_list/', CombinedSubscriptionListView.as_view(), name='C_list'),

]