from django.db import models

# Create your models here.
class User(models.Model):
    uId=models.AutoField(primary_key=True,verbose_name="ユーザID")
    mail=models.EmailField(max_length=255,unique=True,verbose_name="メールアドレス")
    password=models.CharField(max_length=255,verbose_name="パスワード")
    authority=models.IntegerField(verbose_name="権限")

    class Meta:
        db_table = 'user'
        verbose_name = 'ユーザ'

class Profile(models.Model):
    uId=models.OneToOneField("User",primary_key=True,on_delete=models.CASCADE,verbose_name="ユーザID")
    uName=models.CharField(max_length=255,verbose_name="ユーザ名")
    nationality=models.CharField(max_length=255,verbose_name="国籍")
    graduation=models.IntegerField(verbose_name="卒業年度")
    uSchool=models.CharField(max_length=255,verbose_name="学校名")
    sClass=models.IntegerField(verbose_name="学校区分")
    sol=models.IntegerField(verbose_name="文理区分")
    department=models.CharField(verbose_name="学科名")
    uTel=models.IntegerField(verbose_name="電話番号")
    uAddress=models.CharField(max_length=255,verbose_name="住所")
    category1=models.ForeignKey("Category1",on_delete=models.CASCADE,verbose_name="カテゴリ1")
    category2=models.ForeignKey("category2",on_delete=models.CASCADE,verbose_name="カテゴリ2")
    area1=models.ForeignKey("Area1",on_delete=models.CASCADE,verbose_name="エリア1")
    uOffer=models.CharField(max_length=255,verbose_name="内定先")
    jOffer_l=models.CharField(max_length=255,verbose_name="応募求人リスト")

    class Meta:
        db_table="profile"
        verbose_name="プロフィール"

class Assessment(models.Model):
    uId=models.OneToOneField("User",primary_key=True,on_delete=models.CASCADE,verbose_name="ユーザID")
    QA_l=models.TextField(verbose_name="自己分析リスト")

    class Meta:
        db_table='assessment'
        verbose_name='自己分析'

class Corporation(models.Model):
    cId=models.IntegerField(primary_key=True,verbose_name="法人番号")
    cName=models.CharField(max_length=255,verbose_name="法人名")