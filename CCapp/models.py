from django.db import models

# Create your models here.

class Base(models.Model):
    id=models.AutoField(primary_key=True,verbose_name="ID")
    name=models.CharField(max_length=15,verbose_name="名前")

    class Meta:
        abstract=True

class Category1(Base):
    class Meta:
        db_table='Category1'
        verbose_name='カテゴリ1'

class Category2(Category1):
    category1=models.ForeignKey(Category1,on_delete=models.CASCADE,verbose_name="カテゴリ1")

    class Meta:
        db_table='Category2'
        verbose_name='カテゴリ2'

class Area1(models.Model):
    class Meta:
        db_table='Area1'
        verbose_name='エリア1'

class Area2(Area1):
    area1=models.ForeignKey(Area1,verbose_name="エリア1")

    class Meta:
        db_table='Area2'
        verbose_name='エリア2'

class User(Base):
    mail=models.EmailField(max_length=255,unique=True,verbose_name="メールアドレス")
    password=models.CharField(max_length=255,verbose_name="パスワード")
    authority=models.IntegerField(verbose_name="権限")

    class Meta:
        db_table='user'
        verbose_name='ユーザ'

class Profile(models.Model):
    uId=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,verbose_name="ユーザID")
    nationality=models.CharField(max_length=255,verbose_name="国籍")
    graduation=models.IntegerField(verbose_name="卒業年度")
    uSchool=models.CharField(max_length=255,verbose_name="学校名")
    sClass=models.IntegerField(verbose_name="学校区分")
    sol=models.IntegerField(verbose_name="文理区分")
    department=models.CharField(verbose_name="学科名")
    uTel=models.IntegerField(verbose_name="電話番号")
    uAddress=models.CharField(max_length=255,verbose_name="住所")
    category1=models.ForeignKey(Category1,on_delete=models.CASCADE,verbose_name="カテゴリ1")
    category2=models.ForeignKey(Category2,on_delete=models.CASCADE,verbose_name="カテゴリ2")
    area1=models.ForeignKey(Area1,on_delete=models.CASCADE,verbose_name="エリア1")
    uOffer=models.CharField(max_length=255,verbose_name="内定先")
    jOffer_l=models.CharField(max_length=255,verbose_name="応募求人リスト")

#     class Meta:
#         db_table="profile"
#         verbose_name="プロフィール"

class Assessment(models.Model):
    uId=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,verbose_name="ユーザID")
    QA_l=models.TextField(verbose_name="自己分析リスト")

#     class Meta:
#         db_table='assessment'
#         verbose_name='自己分析'

class Corporation(models.Model):
    cId=models.IntegerField(primary_key=True,verbose_name="法人番号")
    cName=models.CharField(max_length=255,verbose_name="法人名")
    address=models.CharField(max_length=255,verbose_name="住所")
    cMail=models.CharField(max_length=255,verbose_name="メールアドレス")
    cTel=models.IntegerField(verbose_name="電話番号")
    url=models.CharField(max_length=511,verbose_name="URL")

    class Meta:
        db_table='corporation'
        verbose_name='法人'

class Offer(Base):
    detail=models.TextField(verbose_name="詳細")
    solicitation=models.TextField(verbose_name="募集要項")
    course=models.CharField(max_length=255,verbose_name="コース名")
    forms=models.CharField(max_length=31,verbose_name="雇用形態")
    roles=models.CharField(max_length=255,verbose_name="配属職種")
    CoB=models.TextField(verbose_name="提出書類")
    subject=models.CharField(max_length=255,verbose_name="募集対象")
    NoP=models.CharField(max_length=63,verbose_name="募集人数")
    departments=models.CharField(max_length=255,verbose_name="募集学部・学科")
    characteristic=models.TextField(verbose_name="募集特徴")
    PES=models.TextField(verbose_name="採用後の対応")
    giving=models.CharField(max_length=255,verbose_name="初任給")
    allowances=models.CharField(max_length=255,verbose_name="諸手当")
    salaryRaise=models.CharField(max_length=63,verbose_name="昇給")
    bonus=models.CharField(max_length=31,verbose_name="賞与")
    holiday=models.TextField(verbose_name="休日休暇")
    welfare=models.TextField(verbose_name="福利厚生")
    workingHours=models.CharField(max_length=255,verbose_name="勤務時間")
    area2=models.ForeignKey(Area2,on_delete=models.CASCADE,verbose_name="エリア2")
    category1=models.ForeignKey(Category1,on_delete=models.CASCADE,verbose_name="カテゴリ1")
    category2=models.ForeignKey(Category2,on_delete=models.CASCADE,verbose_name="カテゴリ2")
    tagId_l=models.TextField(verbose_name="タグIDリスト")
    corporation=models.ForeignKey(Corporation,on_delete=models.CASCADE,verbose_name="法人")
    uId_l=models.TextField(verbose_name="応募者リスト")
    period=models.DateTimeField(verbose_name="公開期限")
    status=models.BooleanField(default=False,verbose_name="公開状況")

    class Meta:
        db_table='offer'
        verbose_name='求人'

class BaseDM(Base):
    read=models.BooleanField(default=False,verbose_name="既読")
    detail=models.TextField(verbose_name="詳細")
    
    class Meta:
        abstract=True

class DM(BaseDM):
    uId=models.ForeignKey(User,verbose_name="ユーザID")
    cId=models.ForeignKey(Corporation,verbose_name="法人番号")

    class Meta:
        db_table='DM'
        verbose_name='DM'

class SupportDM(BaseDM):
    uIdSend=models.ForeignKey(User,verbose_name="送信者ID")
    uIdReceive=models.ForeignKey(User,verbose_name="受信者ID")

    class Meta:
        db_table='supportDM'
        verbose_name='サポートDM'

class Tag(Base):
    upperTag=models.ForeignKey("")
