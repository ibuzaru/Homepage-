# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ExampleForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string  # メール本文生成
from django.contrib import messages  # アラートメッセージ用
from .models import ExampleModel
from datetime import datetime, timedelta
import json  # 追加
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'ao/home.html')

def rooms(request):
    return render(request, 'ao/rooms.html')

def reservation(request):
    # 予約済み日付を取得
    reserved_dates = []
    reservations = ExampleModel.objects.all()
    for reservation in reservations:
        check_in_date = reservation.check_in_date
        check_out_date = reservation.check_out_date

        if check_in_date and check_out_date:
            # 日付を文字列のまま処理する
            current_date = datetime.strptime(check_in_date, "%Y-%m-%d")
            end_date = datetime.strptime(check_out_date, "%Y-%m-%d")
            while current_date <= end_date:
                reserved_dates.append(current_date.strftime("%Y-%m-%d"))  # ISO形式で文字列化
                current_date += timedelta(days=1)
    
    context = {
        'reserved_dates': json.dumps(reserved_dates)  # 重複は Python 側では不要なのでそのまま渡す
    }
    return render(request, 'ao/reservation.html', context)





@login_required
def mypage(request):
    # ログイン中のユーザーに紐付く予約情報を、チェックイン日が近い順に取得
    reservations = ExampleModel.objects.filter(user=request.user).order_by('check_in_date')
    return render(request, 'ao/mypage.html', {
        'user': request.user,
        'reservations': reservations
    })


def example(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # フォームが有効な場合、確認画面にデータを渡す
            form_data = form.cleaned_data
            return render(request, 'ao/example_confirm.html', {'data': form_data})
        else:
            # フォームが無効な場合、入力された値を保持して再表示
            return render(request, "ao/example.html", {"form": form})
    else:
        # GETリクエスト時は初期値を設定
        check_in = request.GET.get('check_in', '')
        check_out = request.GET.get('check_out', '')
        form = ExampleForm(initial={'check_in_date': check_in, 'check_out_date': check_out})
        return render(request, "ao/example.html", {"form": form})


def example_fix(request):
    if request.method == 'POST':
        # POSTデータから初期値を設定
        initial_data = {key: value[0] if isinstance(value, list) else value for key, value in request.POST.items()}
        form = ExampleForm(initial=initial_data)
        return render(request, "ao/example.html", {"form": form})
    else:
        # 初回アクセス時の空フォーム
        form = ExampleForm()
        return render(request, "ao/example.html", {"form": form})

def example_confirm(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():  # フォームが正しく送信されたか確認
            data = form.cleaned_data
            email = data['email']
            password = data['password']

            # 重複チェック（お好みで変更可）
            existing_entry = ExampleModel.objects.filter(
                name=data['name'], 
                email=email,
                check_in_date=data['check_in_date'],
                check_out_date=data['check_out_date']
            ).exists()
            if existing_entry:
                return render(
                    request, 
                    'ao/example.html', 
                    {
                        'form': form, 
                        'errors': {'duplicate': '同じ内容のデータが既に登録されています。'}
                    }
                )
            
            # ★User の新規作成★
            # 既に同じメールのユーザーがいないか確認
            user_qs = User.objects.filter(email=email)
            if user_qs.exists():
                # すでにユーザーがいる場合は取得（同じメールのユーザーで上書きはしない想定）
                user = user_qs.first()
            else:
                # 新規ユーザーを作成
                user = User.objects.create_user(
                    username=data['name'],   
                    email=email,
                    password=password
                )
            # 予約情報を保存 (User と紐付ける)
            example_instance = form.save(commit=False)
            example_instance.user = user
            example_instance.save()

            return render(request, 'ao/success_reserve.html', {'form': form})
        else:
            return render(request, 'ao/example.html', {'form': form, 'errors': form.errors})


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect





def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # 入力チェック（空欄チェック）
        if not email or not password:
            return render(request, 'ao/login.html', {
                'error': 'メールアドレスとパスワードを入力してください。',
                'email': email  # 入力内容保持
            })

        # メールアドレスでユーザーを取得
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'ao/login.html', {
                'error': 'メールアドレスまたはパスワードが間違っています。',
                'email': email  # 入力内容保持
            })

        # ユーザー名で認証
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mypage')  # ログイン成功 → マイページへ
        else:
            return render(request, 'ao/login.html', {
                'error': 'メールアドレスまたはパスワードが間違っています。',
                'email': email  # 入力内容保持
            })

    return render(request, 'ao/login.html')




























