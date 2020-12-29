from django.urls import path

from .views import topicsView, topicView, quizView, answerView, incorrectView, finishView, thanksView, cheaterView

urlpatterns = [
    path('', topicsView, name='home'),
    path('topic/<int:tid>/', topicView, name='topic'),
    path('quiz/<int:tid>/', quizView, name='quiz'),
    path('incorrect/', incorrectView, name='wrong'),
    path('finish/', finishView, name='finish'),
    path('thanks/', thanksView, name='thanks'),
    path('cheater/', cheaterView, name='cheater'),
    path('quiz/<int:tid>/<int:aid>/', answerView, name='answer'),
]
