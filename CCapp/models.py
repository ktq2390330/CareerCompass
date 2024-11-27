from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, mail, password=None, **extra_fields):
        if not mail:
            raise ValueError("メールアドレスを指定してください。")
        mail = self.normalize_email(mail)
        user = self.model(mail=mail, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mail, password=None, **extra_fields):
        extra_fields.setdefault('authority', 0)
        return self.create_user(mail, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    mail = models.EmailField(max_length=255, unique=True, verbose_name="メールアドレス")
    name = models.CharField(max_length=64, verbose_name="名前", blank=True)
    authority = models.IntegerField(
        choices=[(0, "Admin"), (1, "Support Staff"), (2, "Service User")],
        default=2,
        verbose_name="権限"
    )
    objects = UserManager()
    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user'
        verbose_name = 'ユーザー'
        verbose_name_plural = 'ユーザー'

    def is_admin(self):
        return self.authority == 0

    def is_staff_member(self):
        return self.authority == 1

    def is_service_user(self):
        return self.authority == 2

    def has_permission(self, level):
        return self.authority <= level

    def get_full_name(self):
        return self.name or "未設定"

    def __str__(self):
        return f"{self.name} ({self.get_authority_display()})"


class Base(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=64, verbose_name="名前")

    class Meta:
        abstract = True


# エリア
class Area0(Base):
    class Meta:
        db_table = 'Area0'
        verbose_name = 'エリア0'

    def get_area1_list(self):
        return self.area1_area0.all()

    def __str__(self):
        return self.name


class Area1(Base):
    area0 = models.ForeignKey(Area0, on_delete=models.CASCADE, verbose_name="エリア0", related_name="area1_area0")

    class Meta:
        db_table = 'Area1'
        verbose_name = 'エリア1'

    def get_area2_list(self):
        return self.area2_area1.all()

    def __str__(self):
        return f"{self.area0.name} - {self.name}"


class Area2(Base):
    area1 = models.ForeignKey(Area1, on_delete=models.CASCADE, verbose_name="エリア1", related_name="area2_area1")

    class Meta:
        db_table = 'Area2'
        verbose_name = 'エリア2'

    def __str__(self):
        return f"{self.area1.area0.name} - {self.area1.name} - {self.name}"


# カテゴリ
class Category00(Base):
    class Meta:
        db_table = 'Category00'
        verbose_name = 'カテゴリ00'


class Category01(Base):
    category00 = models.ForeignKey(Category00, on_delete=models.CASCADE, verbose_name="カテゴリ00", related_name="category01_category00")

    class Meta:
        db_table = 'Category01'
        verbose_name = 'カテゴリ01'


class Category10(Base):
    class Meta:
        db_table = 'Category10'
        verbose_name = 'カテゴリ10'


class Category11(Base):
    category10 = models.ForeignKey(Category10, on_delete=models.CASCADE, verbose_name="カテゴリ10", related_name="category11_category10")

    class Meta:
        db_table = 'Category11'
        verbose_name = 'カテゴリ11'


# タグ
class Tag(Base):
    class Meta:
        db_table = 'Tag'
        verbose_name = 'タグ'


# プロフィール
class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name="ユーザID", related_name="profile")
    furigana = models.CharField(max_length=256, verbose_name="フリガナ")
    nationality = models.CharField(max_length=256, verbose_name="国籍")
    birth = models.DateField(verbose_name="生年月日")
    gender = models.CharField(max_length=16, verbose_name="性別")
    graduation = models.IntegerField(verbose_name="卒業年度")
    uSchool = models.CharField(max_length=256, verbose_name="学校名")
    sClass = models.IntegerField(verbose_name="学校区分")
    sol = models.IntegerField(verbose_name="文理区分")
    department = models.CharField(max_length=32, verbose_name="学科名")
    uTel = models.CharField(max_length=16, verbose_name="電話番号")
    postalCode = models.CharField(max_length=8, verbose_name="郵便番号")
    uAddress = models.CharField(max_length=256, verbose_name="住所")
    category00 = models.ForeignKey(Category00, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ00")
    category01 = models.ForeignKey(Category01, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ01")
    category10 = models.ForeignKey(Category10, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ10")
    category11 = models.ForeignKey(Category11, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ11")
    area1 = models.ForeignKey(Area1, on_delete=models.SET_NULL, null=True, verbose_name="エリア1")
    uOffer = models.CharField(max_length=256, verbose_name="内定先")

    class Meta:
        db_table = "profile"
        verbose_name = "プロフィール"

    def get_full_address(self):
        return f"{self.postalCode} {self.uAddress}"

    def get_preferences(self):
        return {
            "業界": f"{self.category00.name} - {self.category01.name if self.category01 else '未設定'}",
            "職種": f"{self.category10.name} - {self.category11.name if self.category11 else '未設定'}",
            "エリア": f"{self.area1.name if self.area1 else '未設定'}",
        }

    def __str__(self):
        return f"{self.user.name} のプロフィール"

# 法人
class Corporation(models.Model):
    corp = models.CharField(max_length=13, primary_key=True, unique=True, verbose_name="法人番号")
    name = models.CharField(max_length=256, verbose_name="法人名")
    address = models.CharField(max_length=256, verbose_name="住所")
    cMail = models.EmailField(max_length=255, unique=True, verbose_name="メールアドレス")
    cTel = models.CharField(max_length=16, verbose_name="電話番号")
    url = models.URLField(max_length=512, verbose_name="URL")

    class Meta:
        db_table = 'corporation'
        verbose_name = '法人'

    def get_offers(self):
        return self.offer_set.all()

    def __str__(self):
        return self.name


# 求人情報
class Offer(Base):
    detail = models.TextField(verbose_name="詳細")
    solicitation = models.TextField(verbose_name="募集要項")
    course = models.CharField(max_length=256, verbose_name="コース名")
    forms = models.CharField(max_length=32, verbose_name="雇用形態")
    roles = models.CharField(max_length=256, verbose_name="配属職種")
    CoB = models.TextField(verbose_name="提出書類")
    subject = models.CharField(max_length=256, verbose_name="募集対象")
    NoP = models.CharField(max_length=64, verbose_name="募集人数")
    departments = models.CharField(max_length=256, verbose_name="募集学部・学科")
    characteristic = models.TextField(verbose_name="募集特徴")
    PES = models.TextField(verbose_name="採用後の対応")
    giving = models.CharField(max_length=256, verbose_name="初任給")
    allowances = models.CharField(max_length=256, verbose_name="諸手当")
    salaryRaise = models.CharField(max_length=64, verbose_name="昇給")
    bonus = models.CharField(max_length=32, verbose_name="賞与")
    holiday = models.TextField(verbose_name="休日休暇")
    welfare = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, verbose_name="福利厚生")
    workingHours = models.CharField(max_length=256, verbose_name="勤務時間")
    area1 = models.ForeignKey(Area1, on_delete=models.SET_NULL, null=True, verbose_name="エリア1", related_name="offer_area1")
    category00 = models.ForeignKey(Category00, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ00")
    category01 = models.ForeignKey(Category01, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ01")
    category10 = models.ForeignKey(Category10, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ10")
    category11 = models.ForeignKey(Category11, on_delete=models.SET_NULL, null=True, verbose_name="カテゴリ11")
    corporation = models.ForeignKey(Corporation, on_delete=models.CASCADE, null=True, verbose_name="法人")
    applicants = models.ManyToManyField(User, through="OfferEntry", verbose_name="応募者リスト", related_name="offer_offerEntry")
    period = models.DateTimeField(verbose_name="公開期限")
    status = models.BooleanField(default=False, verbose_name="公開状況")

    class Meta:
        db_table = 'offer'
        verbose_name = '求人'

    def is_active(self):
        return self.status and self.period > now()

    def get_applicant_count(self):
        return self.applicants.count()

    def __str__(self):
        return f"{self.name} ({self.corporation.name if self.corporation else '未設定'})"


class OfferEntry(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, verbose_name="求人", related_name="offerApp_offer")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザ", related_name="offerApp_user")
    applied_date = models.DateTimeField(auto_now_add=True, verbose_name="応募日")

    class Meta:
        db_table = 'offer_entry'
        verbose_name = '求人応募'
        unique_together = ('offer', 'user')

    def __str__(self):
        return f"{self.user.name} applied to {self.offer.name}"


# 自己分析
class Assessment(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, verbose_name="ユーザID")
    question01 = models.ForeignKey("Question01", on_delete=models.CASCADE, verbose_name="質問", related_name="assessment_question01")
    answer = models.TextField(verbose_name="回答")

    class Meta:
        db_table = 'assessment'
        verbose_name = '自己分析'

    def __str__(self):
        return f"Assessment for {self.user.name}"


# 質問
class Question00(Base):
    class Meta:
        db_table = "question00"
        verbose_name = "質問00"

    def get_questions(self):
        return self.question01_question00.all()

    def __str__(self):
        return self.name


class Question01(Base):
    question00 = models.ForeignKey(Question00, on_delete=models.CASCADE, verbose_name="質問00", related_name="question01_question00")

    class Meta:
        db_table = "question01"
        verbose_name = "質問01"

    def __str__(self):
        return f"{self.question00.name} - {self.name}"


# ダイレクトメッセージ (DM)
class BaseDM(Base):
    read = models.BooleanField(default=False, verbose_name="既読")
    detail = models.TextField(verbose_name="詳細")

    class Meta:
        abstract = True


class DM(BaseDM):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザID")
    corp = models.ForeignKey(Corporation, on_delete=models.CASCADE, verbose_name="法人番号")

    class Meta:
        db_table = 'DM'
        verbose_name = 'DM'

    def __str__(self):
        return f"DM to {self.user.name} from {self.corp.name}"


class SupportDM(BaseDM):
    userSend = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="送信者ID", related_name="supportDM_send")
    userReceive = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="受信者ID", related_name="supportDM_receive")

    class Meta:
        db_table = 'supportDM'
        verbose_name = 'サポートDM'

    def __str__(self):
        return f"DM from {self.userSend.name} to {self.userReceive.name}"
