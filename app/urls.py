from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from .views import UserDelete, UserLoginView,UserRegister,TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete

urlpatterns = [
    #ユーザー
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegister.as_view(), name="register"),
    path("deleteUser/<int:pk>/", UserDelete.as_view(), name="delete-user"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    #タスク
    path("", TaskList.as_view(), name="tasks"),
    path("task/<int:pk>/", TaskDetail.as_view(), name="task"),
    path("createTask/", TaskCreate.as_view(), name="create-task"),
    path("editTask/<int:pk>/", TaskUpdate.as_view(), name="edit-task"),
    path("deleteTask/<int:pk>/", TaskDelete.as_view(), name="delete-task"),
]