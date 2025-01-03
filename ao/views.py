from django.shortcuts import render, redirect
from .forms import ExampleForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string  # メール本文生成
from django.contrib import messages  # アラートメッセージ用

def home(request):
    return render(request, 'ao/home.html')

def reservation(request):
    return render(request, 'ao/reservation.html')

def contact(request):
    return render(request, 'ao/contact.html')

def test(request):
    return render(request, 'ao/test.html')

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
            # フォームデータの保存
            form.save()

            # メール送信
            email = form.cleaned_data.get('email')  # フォームからメールアドレスを取得
            message = (
                f"チェックイン日: {form.cleaned_data.get('check_in_date')}\n"
                f"チェックアウト日: {form.cleaned_data.get('check_out_date')}\n"
                f"名前: {form.cleaned_data.get('name')}\n"
                f"ふりがな: {form.cleaned_data.get('furigana')}\n"
                f"予約人数: {form.cleaned_data.get('people')}\n"
                f"メールアドレス: {form.cleaned_data.get('email')}\n"
                f"電話番号: {form.cleaned_data.get('phone_number')}\n"
                f"郵便番号: {form.cleaned_data.get('postal_code')}\n"
                f"住所: {form.cleaned_data.get('address')}\n"
            )
            send_mail(
                subject='予約内容確認',
                message=message,
                from_email='your-email@gmail.com',  # 送信元メールアドレス
                recipient_list=[email],  # フォームに入力されたメールアドレス
                fail_silently=False,
            )

            # 成功時のレンダリング
            return render(request, 'ao/home.html', {'form': form})
        else:
            # バリデーションエラーが発生した場合
            return render(request, 'ao/example.html', {'form': form, 'errors': form.errors})


















