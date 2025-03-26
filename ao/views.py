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
        # POSTデータから初期値を設定（チェックボックスを正しく処理）
        initial_data = {}
        for key, value in request.POST.items():
            # チェックボックスフィールドの場合
            if key in ['soumen','games', 'others']:
                initial_data[key] = True if value == 'on' else False
            # その他のフィールド
            else:
                initial_data[key] = value[0] if isinstance(value, list) else value
        
        form = ExampleForm(initial=initial_data)
        return render(request, "ao/example.html", {"form": form})
    else:
        form = ExampleForm()
        return render(request, "ao/example.html", {"form": form})


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, redirect
from django.conf import settings
from .models import ExampleModel
from datetime import datetime

def example_confirm(request):
    if request.method == 'POST':
        data = request.POST.dict()
        
        # チェックボックス値の正規化
        if 'games' in data:
            data['soumen'] = 'on' if data['soumen'] in ('on', 'true', 'True', True) else 'off'
        if 'games' in data:
            data['games'] = 'on' if data['games'] in ('on', 'true', 'True', True) else 'off'
        if 'others' in data:
            data['others'] = 'on' if data['others'] in ('on', 'true', 'True', True) else 'off'
        
        # 合計金額計算
        total_amount, price_per_person = calculate_prices(data)
        
        # データベースに保存
        reservation = save_reservation(data, total_amount, price_per_person)
        
        # メール送信
        send_customer_email(data, total_amount, price_per_person)
        send_admin_email(data, total_amount, reservation.id)
        
        return redirect('success_reserve')
    
    return render(request, 'ao/example_confirm.html', {'data': data})

def calculate_prices(data):
    base_price = 20000
    extra_price_per_person = 2000
    yakiniku_price = 2500

    men = int(data.get('men', 0))
    women = int(data.get('women', 0))
    yakiniku_sets = int(data.get('yakiniku', 0))
    
    # 宿泊日数計算
    check_in = datetime.strptime(data['check_in_date'], '%Y-%m-%d')
    check_out = datetime.strptime(data['check_out_date'], '%Y-%m-%d')
    days = (check_out - check_in).days
    
    people_total = men + women
    total_amount = (base_price + extra_price_per_person * people_total) * days
    total_amount += yakiniku_price * yakiniku_sets
    
    # deposit priceは加算しない（削除）
    price_per_person = total_amount // people_total if people_total > 0 else 0
    
    return total_amount, price_per_person

def save_reservation(data, total_amount, price_per_person):
    # チェックボックス値の処理を改善
    soumen_value = data.get('soumen') in ('on', 'true', 'True', True)
    games_value = data.get('games') in ('on', 'true', 'True', True)
    others_value = data.get('others') in ('on', 'true', 'True', True)
    
    return ExampleModel.objects.create(
        check_in_date=data['check_in_date'],
        check_out_date=data['check_out_date'],
        name=data['name'],
        furigana=data['furigana'],
        men=data.get('men', 0),
        women=data.get('women', 0),
        email=data['email'],
        phone_number=data['phone_number'],
        postal_code=data['postal_code'],
        address=data['address'],
        yakiniku=data.get('yakiniku', 0),
        soumen=soumen_value,
        games=games_value,
        others=others_value,
        messages=data.get('messages', ''),
    )


def send_customer_email(data, total_amount, price_per_person):
    subject = '【予約完了】ご予約ありがとうございます'
    message = render_to_string('ao/customer_email.txt', {
        'data': data,
        'total_amount': f"{total_amount:,}",
        'pricePerPerson': f"{price_per_person:,}"
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [data['email']],
        fail_silently=False
    )

def send_admin_email(data, total_amount, reservation_id):
    subject = f'【新規予約】予約ID: {reservation_id}'
    message = render_to_string('ao/admin_email.txt', {
        'data': data,
        'total_amount': f"{total_amount:,}",
        'reservation_id': reservation_id
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=False
    )
def success_reserve(request):
    return render(request, 'ao/success_reserve.html')




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

























