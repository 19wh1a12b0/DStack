from django.urls import path
from dstack.views import *

urlpatterns = [
    path('', Home,name='home'),
    path('login/',Login,name='login'),
    path('userpage/',UserPage,name='userpage'),
    path('question/',Question,name='question'),
    path('questionAdd/',questionAdd,name='questionAdd'),
    path('questionId/<int:pkk>/',getByQuestion,name='questionId'),
    path('comment/<int:pkk>/',comment,name='comment'),
    path('finalDataSend/',finalDataSend,name='finalDataSend')
]
