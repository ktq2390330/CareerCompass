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

class Category2(Base):
    category1=models.ForeignKey(Category1,on_delete=models.CASCADE,verbose_name="カテゴリ1",related_name="category2_category1")

    class Meta:
        db_table='Category2'
        verbose_name='カテゴリ2'

class Area1(Base):
    class Meta:
        db_table='Area1'
        verbose_name='エリア1'

class Area2(Base):
    area1=models.ForeignKey(Area1,on_delete=models.CASCADE,verbose_name="エリア1",related_name="area2_area1")

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
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,verbose_name="ユーザID",related_name="profile")
    nationality=models.CharField(max_length=255,verbose_name="国籍")
    birth=models.DateField(verbose_name="生年月日")
    gender=models.CharField(max_length=15,verbose_name="性別")
    graduation=models.IntegerField(verbose_name="卒業年度")
    uSchool=models.CharField(max_length=255,verbose_name="学校名")
    sClass=models.IntegerField(verbose_name="学校区分")
    sol=models.IntegerField(verbose_name="文理区分")
    department=models.CharField(max_length=31,verbose_name="学科名")
    uTel=models.CharField(max_length=15,verbose_name="電話番号")
    uAddress=models.CharField(max_length=255,verbose_name="住所")
    category1=models.ForeignKey(Category1,on_delete=models.SET_NULL,null=True,verbose_name="カテゴリ1",related_name="profile_category1")
    category2=models.ForeignKey(Category2,on_delete=models.SET_NULL,null=True,verbose_name="カテゴリ2",related_name="profile_category2")
    area1=models.ForeignKey(Area1,on_delete=models.SET_NULL,null=True,verbose_name="エリア1",related_name="profile_area1")
    uOffer=models.CharField(max_length=255,verbose_name="内定先")
    jOffer_l=models.CharField(max_length=255,verbose_name="応募求人リスト")

    class Meta:
        db_table="profile"
        verbose_name="プロフィール"

class Assessment(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,verbose_name="ユーザID")
    QA_l=models.TextField(verbose_name="自己分析リスト")

    class Meta:
        db_table='assessment'
        verbose_name='自己分析'

class Corporation(models.Model):
    corp=models.IntegerField(primary_key=True,unique=True,verbose_name="法人番号")
    cName=models.CharField(max_length=255,verbose_name="法人名")
    address=models.CharField(max_length=255,verbose_name="住所")
    cMail=models.CharField(max_length=255,unique=True,verbose_name="メールアドレス")
    cTel=models.CharField(max_length=15,verbose_name="電話番号")
    url=models.URLField(max_length=511,verbose_name="URL")

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
    area2=models.ForeignKey(Area2,on_delete=models.SET_NULL,null=True,verbose_name="エリア2",related_name="offer_area2")
    category1=models.ForeignKey(Category1,on_delete=models.SET_NULL,null=True,verbose_name="カテゴリ1",related_name="offer_category1")
    category2=models.ForeignKey(Category2,on_delete=models.SET_NULL,null=True,verbose_name="カテゴリ2",related_name="offer_category2")
    tag_l=models.TextField(verbose_name="タグリスト")
    corporation=models.ForeignKey(Corporation,on_delete=models.CASCADE,verbose_name="法人")
    user_l=models.TextField(verbose_name="応募者リスト")
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
    user=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="ユーザID")
    corp=models.ForeignKey(Corporation,on_delete=models.CASCADE,verbose_name="法人番号")

    class Meta:
        db_table='DM'
        verbose_name='DM'

class SupportDM(BaseDM):
    userSend=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="送信者ID",related_name="supportDM_send")
    userReceive=models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="受信者ID",related_name="supportDM_receive")

    class Meta:
        db_table='supportDM'
        verbose_name='サポートDM'

class Tag(Base):
    class Meta:
        db_table='Tag'
        verbose_name='タグ'