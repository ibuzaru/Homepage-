# views.py
from django.shortcuts import render, redirect
from .forms import ExampleForm
from django.conf import settings
from django.template.loader import render_to_string  # メール本文生成
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
            end_date = datetime.strptime(check_out_date, "%Y-%m-%d") - timedelta(days=1)  # チェックアウト日の前日までを予約不可にする
            while current_date <= end_date:
                reserved_dates.append(current_date.strftime("%Y-%m-%d"))  # ISO形式で文字列化
                current_date += timedelta(days=1)
    
    context = {
        'reserved_dates': json.dumps(reserved_dates)  # 重複は Python 側では不要なのでそのまま渡す
    }
    return render(request, 'ao/reservation.html', context)





@login_required
def mypage(request):
    # 現在の日付を取得
    from datetime import date
    today = date.today()

    # ログイン中のユーザーに紐付く予約情報を、チェックイン日が近い順に取得
    # 現在の日付よりチェックアウト日が前の予約を削除
    ExampleModel.objects.filter(user=request.user, check_out_date__lt=today).delete()

    # 残りの予約情報を取得
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


import logging
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datetime import datetime

def send_confirmation_email(data_list):
    """
    ユーザーおよび管理者（ホスト）に予約確認メールを送信するヘルパー関数。
    
    :param data_list: 予約データのリスト（複数の予約が含まれる可能性あり）
    """
    subject = '予約内容のご確認'
    
    admin_email = getattr(settings, 'ADMIN_EMAIL', 'sansoao6430366@gmail.com')
    recipient_list = list(set([entry['email'] for entry in data_list]))
    if admin_email:
        recipient_list.append(admin_email)

    price_per_person = 5500  # 1人あたりの料金（税込）

    for entry in data_list:
        # check_in_date, check_out_date を `datetime.date` に変換
        check_in_date = datetime.strptime(entry['check_in_date'], "%Y-%m-%d").date()
        check_out_date = datetime.strptime(entry['check_out_date'], "%Y-%m-%d").date()

        people = int(entry['people'])  # 念のため整数に変換

        # 宿泊日数を計算（最低1日）
        days = max(1, (check_out_date - check_in_date).days)

        # 合計金額を計算
        entry['total_amount'] = people * price_per_person * days

    context = {
        'reservations': data_list,
    }

    message_html = render_to_string('ao/confirmation_email.html', context)

    try:
        email_message = EmailMessage(
            subject=subject,
            body=message_html,
            from_email=settings.EMAIL_HOST_USER,
            to=recipient_list,
        )
        email_message.content_subtype = 'html'
        email_message.encoding = 'utf-8'
        email_message.send()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"メール送信中にエラーが発生しました: {e}")
        raise



def example_confirm(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data['email']
            password = data['password']

            reservation_exists = ExampleModel.objects.filter(
                check_in_date=data['check_in_date'],
                check_out_date=data['check_out_date']
            ).exists()

            if reservation_exists:
                return render(request, 'ao/reserve_error.html', {
                    'error_message': '指定された日に既に予約があります。他の日付をお試しください。'
                })

            user_qs = User.objects.filter(email=email)
            if user_qs.exists():
                user = user_qs.first()
            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password
                )

            # データを辞書にまとめる
            reservation_data = {
                'check_in_date': data['check_in_date'],
                'check_out_date': data['check_out_date'],
                'name': data['name'],
                'furigana': data['furigana'],
                'people': data['people'],
                'phone_number': data['phone_number'],
                'email': email,  # ユーザーのメールアドレス
            }

            # メール送信
            send_confirmation_email([reservation_data])

            # 予約情報を保存
            example_instance = form.save(commit=False)
            example_instance.user = user
            example_instance.save()

            return render(request, 'ao/success_reserve.html', {'form': form})
        else:
            return render(request, 'ao/example.html', {'form': form, 'errors': form.errors})




from django.contrib.auth import authenticate, login
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

from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
from django.conf import settings

def faq(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # メールの内容
            subject = f"お問い合わせ: {name}様"
            message_body = f"お名前: {name}\nメールアドレス: {email}\n\nお問い合わせ内容:\n{message}"
            recipient_list = [settings.ADMIN_EMAIL]

            # メール送信
            send_mail(subject, message_body, settings.EMAIL_HOST_USER, recipient_list)

            return render(request, 'ao/faq.html', {
                'form': ContactForm(),  # フォームをリセット
                'success': True
            })
    else:
        form = ContactForm()

    return render(request, 'ao/faq.html', {'form': form})


def supermarket(request):
    return render(request, 'ao/supermarket.html')

def sightseeing(request):
    return render(request, 'ao/sightseeing.html')

def howtostay(request):
    return render(request, 'ao/howtostay.html')

def kiyaku(request):
    return render(request, 'ao/kiyaku.html')

























