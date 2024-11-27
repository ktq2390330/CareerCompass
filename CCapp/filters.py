from django_filters import rest_framework as filters
from .models import Offer
from django.db.models import Q
from django.utils.timezone import now
from .models import Offer

class OfferFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="求人名")
    welfare = filters.CharFilter(field_name="welfare__name", lookup_expr="icontains", label="福利厚生")
    area0 = filters.CharFilter(field_name="area1__area0__name", lookup_expr="icontains", label="エリア0")
    area1 = filters.CharFilter(field_name="area1__name", lookup_expr="icontains", label="エリア1")
    category00 = filters.CharFilter(field_name="category00__name", lookup_expr="icontains", label="カテゴリ00")
    category01 = filters.CharFilter(field_name="category01__name", lookup_expr="icontains", label="カテゴリ01")
    category10 = filters.CharFilter(field_name="category10__name", lookup_expr="icontains", label="カテゴリ10")
    category11 = filters.CharFilter(field_name="category11__name", lookup_expr="icontains", label="カテゴリ11")
    corporation = filters.CharFilter(field_name="corporation__name", lookup_expr="icontains", label="法人名")
    status = filters.BooleanFilter(field_name="status", label="公開状況")
    period = filters.DateTimeFromToRangeFilter(field_name="period", label="公開期間")
    
    class Meta:
        model = Offer
        fields = [
            "name", "welfare", "area0", "area1", "category00", 
            "category01", "category10", "category11", "corporation", 
            "status", "period"
        ]

def filter_offers(filters, is_admin=False):
    """
    Offersをフィルタリングする関数。
    
    :param filters: dict - フィルタ条件の辞書。
        - name: str | None - 求人名の部分一致。
        - welfare: list[str] | None - 福利厚生のリスト。
        - area0: str | None - エリア0名。
        - area1: str | None - エリア1名。
        - category00: list[str] | None - カテゴリ00のリスト。
        - category01: list[str] | None - カテゴリ01のリスト。
        - category10: list[str] | None - カテゴリ10のリスト。
        - category11: list[str] | None - カテゴリ11のリスト。
        - corporation: list[str] | None - 法人名のリスト。
    :param is_admin: bool - 管理者フィルターかどうか。デフォルトはFalse（ユーザー用フィルター）。
    
    :return: QuerySet - フィルタリングされたOfferのQuerySet。
    """
    query = Q()

    # 1. 求人名フィルタ
    if filters.get("name"):
        query &= Q(name__icontains=filters["name"])
    
    # 2. 福利厚生フィルタ
    if filters.get("welfare"):
        query &= Q(welfare__name__in=filters["welfare"])
    
    # 3. エリアフィルタ
    if filters.get("area0"):
        query &= Q(area1__area0__name__icontains=filters["area0"])
    if filters.get("area1"):
        query &= Q(area1__name__icontains=filters["area1"])
    
    # 4. カテゴリフィルタ
    if filters.get("category00"):
        query &= Q(category00__name__in=filters["category00"])
    if filters.get("category01"):
        query &= Q(category01__name__in=filters["category01"])
    if filters.get("category10"):
        query &= Q(category10__name__in=filters["category10"])
    if filters.get("category11"):
        query &= Q(category11__name__in=filters["category11"])
    
    # 5. 法人フィルタ
    if filters.get("corporation"):
        query &= Q(corporation__name__in=filters["corporation"])
    
    # 6. ユーザー用の公開状況フィルタ
    if not is_admin:
        query &= Q(status=True) & Q(period__gt=now())

    # Offerのフィルタリング
    return Offer.objects.filter(query)
