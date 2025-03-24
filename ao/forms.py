# forms.py
from django import forms
from .models import ExampleModel


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="お名前", widget=forms.TextInput(attrs={'placeholder': 'お名前'}))
    email = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'placeholder': 'メールアドレス'}))
    message = forms.CharField(label="お問い合わせ内容", widget=forms.Textarea(attrs={'placeholder': 'お問い合わせ内容'}))


class ExampleForm(forms.ModelForm):
    # 人数選択肢
    PEOPLE_CHOICES = [(str(i), f"{i}人") for i in range(0, 51)]
    
    men = forms.ChoiceField(
        choices=PEOPLE_CHOICES,
        label="男性人数",
        initial=0,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    women = forms.ChoiceField(
        choices=PEOPLE_CHOICES,
        label="女性人数",
        initial=0,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    yakiniku = forms.IntegerField(
        label="焼肉セット(5人分/1セット)：3500円",
        min_value=0,
        max_value=10,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '数量'})
    )

    games = forms.BooleanField(
        label="ゲーム・漫画セット<デポジット2000円>",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    others = forms.BooleanField(
        label="その他（カヌーなど）<デポジット2000円>",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )

    # 🔥 messagesフィールドを追加
    messages = forms.CharField(
        label="ご要望",
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '300文字まで'})
    )

    class Meta:
        model = ExampleModel
        fields = [
            "check_in_date", "check_out_date",
            "name", "furigana", "men", "women",
            "email", "phone_number", "postal_code",
            "address", "yakiniku", "games", "others", "messages"
        ]

    # フィールドごとのラベルとウィジェット
    check_in_date = forms.CharField(
        label="チェックイン日(13:00~)", max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'チェックイン日'})
    )
    check_out_date = forms.CharField(
        label="チェックアウト日(~10:00)", max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'チェックアウト日'})
    )
    name = forms.CharField(
        label="名前", max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(例：山田 太郎)'})
    )
    furigana = forms.CharField(
        label="ふりがな", max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(例：やまだ たろう)'})
    )
    email = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '@gmail.comなど'})
    )
    phone_number = forms.CharField(
        label="携帯電話番号", max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(例：12345678910)'})
    )
    postal_code = forms.CharField(
        label="郵便番号", max_length=7,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(例：6430366)'})
    )
    address = forms.CharField(
        label="住所", max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )





    

