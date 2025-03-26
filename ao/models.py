# models.py
from django.db import models

class ExampleModel(models.Model):
    # 日付フィールド
    check_in_date = models.CharField(max_length=15, blank=True,null=True, verbose_name="チェックイン日")
    check_out_date = models.CharField(max_length=15, blank=True,null=True, verbose_name="チェックアウト日")
    
    # 名前フィールド
    name = models.CharField(max_length=20, blank=True,null=True, verbose_name="名前")
    furigana = models.CharField(max_length=20, blank=True,null=True, verbose_name="ふりがな")

    # 人数フィールド（デフォルト値0）
    men = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="男性")
    women = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="女性")

    # 連絡先
    email = models.EmailField(max_length=254, blank=True,null=True, verbose_name="メールアドレス")
    phone_number = models.CharField(max_length=15, blank=True,null=True, verbose_name="電話番号")
    postal_code = models.CharField(max_length=7, blank=True,null=True)  # 郵便番号は7桁に修正
    address = models.TextField(blank=True,null=True, verbose_name="住所")

    # オプション
    yakiniku = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name="焼肉セット数量")
    soumen = models.BooleanField(default=False, verbose_name="流しそうめん", blank=True)
    games = models.BooleanField(default=False, verbose_name="ゲーム・漫画セット", blank=True)
    others = models.BooleanField(default=False, verbose_name="その他", blank=True)
    

    # 日時フィールド
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    updated_at = models.DateTimeField(null=True,auto_now=True)

    messages =models.TextField(blank=True,null=True, verbose_name="要望")
    def __str__(self):
        return f"{self.name} ({self.check_in_date} - {self.check_out_date})"


   





    



