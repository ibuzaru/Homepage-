# views.py
from django.shortcuts import render
from .forms import ExampleForm
from django.conf import settings
from django.template.loader import render_to_string  # メール本文生成
from .models import ExampleModel
from datetime import datetime, timedelta
import json  # 追加
from django.contrib.auth.models import User

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


from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.conf import settings

def example_confirm(request):
    if request.method == 'POST':
        data = request.POST.dict()
        
        # 合計金額計算ロジック（必要に応じて）
        # ...
        
        # お客様へのメール送信
        send_customer_email(data)
        
        # 自分（管理者）へのメール送信
        send_admin_email(data)
        
        # 成功ページへリダイレクト
        return redirect('success_reserve')
    
    return render(request, 'ao/example_confirm.html', {'data': data})

def success_reserve(request):
    return render(request, 'ao/success_reserve.html')

def send_customer_email(data):
    subject = '【予約完了】ご予約ありがとうございます'
    message = render_to_string('ao/customer_email.txt', {'data': data})
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [data.get('email')]
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )

def send_admin_email(data):
    subject = '【新規予約】新しい予約が入りました'
    message = render_to_string('ao/admin_email.txt', {'data': data})
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [settings.ADMIN_EMAIL]  # settings.pyで設定
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )



from django.shortcuts import render, redirect



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

























