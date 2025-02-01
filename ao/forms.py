# forms.py
from django import forms
from .models import ExampleModel
from django.core.validators import MinLengthValidator
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="お名前", widget=forms.TextInput(attrs={'placeholder': 'お名前'}))
    email = forms.EmailField(label="メールアドレス", widget=forms.EmailInput(attrs={'placeholder': 'メールアドレス'}))
    message = forms.CharField(label="お問い合わせ内容", widget=forms.Textarea(attrs={'placeholder': 'お問い合わせ内容'}))


class ExampleForm(forms.ModelForm):


    PEOPLE_CHOICES = [(str(i), f"{i}人") for i in range(4, 51)]  # 3～50人の選択肢
    people = forms.ChoiceField(
            choices=PEOPLE_CHOICES,
            label="予約人数",
            widget=forms.Select(attrs={"class": "form-control"})  # 必要に応じてCSSクラスを追加
    )

    password = forms.CharField(
        label="パスワード（6文字以上）",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "6文字以上"}),
        validators=[MinLengthValidator(6)],
        required=True
    )
    class Meta:
        model = ExampleModel
        fields = [
            "check_in_date","check_out_date",
            "name", "furigana", "people", "email",
            "phone_number", "postal_code", "address"
        ]
    # フィールドごとに日本語のラベルを設定
    check_in_date = forms.CharField( label="チェックイン日(13:00~)"  , max_length=15  )
    check_out_date = forms.CharField( label="チェックアウト日(~10:00)", max_length=15  )
    name = forms.CharField(label="名前(例：山田　太郎)", max_length=50)
    furigana = forms.CharField(label="ふりがな(例：やまだ　たろう)", max_length=50)
    email = forms.EmailField(label="メールアドレス(gmail,yahoo,icloudのみ有効)")
    phone_number = forms.CharField(label="電話番号(例：12345678910)", max_length=15)
    postal_code = forms.CharField(label="郵便番号(例：6430366)", max_length=7)
    address = forms.CharField(label="住所", max_length=50)




    

