from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin #ユーザー権限がなければログインページの遷移
from django.contrib.auth.models import User
from app.models import Task

#　ユーザーのログイン
class UserLoginView(LoginView):
    template_name = "app/login.html"
    fields = "__all__"
    # 認証が完了したらタスクページに遷移
    def get_success_url(self):
        return reverse_lazy("tasks")

#　ユーザーの作成
class UserRegister(FormView):
    template_name = "app/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("tasks")
    #　フォームで入力された内容を登録
    def form_valid(self, form):
        user = form.save()
        # userに値が保存されていたら
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)

#　ユーザーの削除
class UserDelete(LoginRequiredMixin,DeleteView):
    model = User
    context_object_name = "user"
    template_name = "app/user_confirm_delete.html"
    success_url = reverse_lazy("login")


################################################################
#　Taskのリストを取得
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"
    #ログインしているユーザーのタスクを取得
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user = self.request.user)
        # 検索で入力した文字を取得
        searchInputText = self.request.GET.get("search") or ""
        # title__startswith 最初の文字と一致するものを検索
        if searchInputText:
            context["tasks"] = context["tasks"].filter(title__icontains = searchInputText)
        # 検索した文字列をinputに残す
        context["search"] = searchInputText
        return context


#　Taskの詳細を取得
class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task"

#　Taskの作成
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title", "description", "completed"]
    success_url = reverse_lazy("tasks")
    # フォームを投稿をユーザーだけに制限する
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#　Taskの編集
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ["title", "description", "completed"]
    success_url = reverse_lazy("tasks")
    # フォームを投稿をユーザーだけに制限する
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

#　Taskの削除
class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    fields = "__all__"
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
