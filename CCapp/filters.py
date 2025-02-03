from django_filters import rest_framework as filters
from .models import Offer
from django.db.models import Q
from django.utils.timezone import now

class OfferFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", label="求人名")
    welfare = filters.ModelMultipleChoiceFilter(queryset=Offer.objects.all(), field_name="welfare", label="福利厚生")
    area0 = filters.NumberFilter(field_name="area1__area0__id", lookup_expr="exact", label="エリア0ID")
    area1 = filters.NumberFilter(field_name="area1__id", lookup_expr="exact", label="エリア1ID")
    category00 = filters.NumberFilter(field_name="category00__id", lookup_expr="exact", label="カテゴリ00ID")
    category01 = filters.NumberFilter(field_name="category01__id", lookup_expr="exact", label="カテゴリ01ID")
    category10 = filters.NumberFilter(field_name="category10__id", lookup_expr="exact", label="カテゴリ10ID")
    category11 = filters.NumberFilter(field_name="category11__id", lookup_expr="exact", label="カテゴリ11ID")
    corporation = filters.CharFilter(field_name="corporation__name", lookup_expr="icontains", label="法人名")
    status = filters.BooleanFilter(field_name="status", label="公開状況")
    period = filters.DateTimeFromToRangeFilter(field_name="period", label="公開期間")
    course = filters.CharFilter(field_name="course", lookup_expr="icontains", label="コース名")
    forms = filters.CharFilter(field_name="forms", lookup_expr="icontains", label="雇用形態")
    roles = filters.CharFilter(field_name="roles", lookup_expr="icontains", label="配属職種")
    departments = filters.CharFilter(field_name="departments", lookup_expr="icontains", label="募集学部・学科")
    characteristic = filters.CharFilter(field_name="characteristic", lookup_expr="icontains", label="募集特徴")
    workingHours = filters.CharFilter(field_name="workingHours", lookup_expr="icontains", label="勤務時間")

    class Meta:
        model = Offer
        fields = [
            "name", "welfare", "area0", "area1", "category00", 
            "category01", "category10", "category11", "corporation", 
            "status", "period", "course", "forms", "roles", 
            "departments", "characteristic", "workingHours"
        ]

def filter_offers(filters, authority):
    query = Q()
    
    if filters.get("name"):
        name_query = Q()
        keywords = filters["name"]
        if isinstance(keywords, str):
            keywords = [keywords]
        for keyword in keywords:
            keyword = keyword.strip()
            name_query |= Q(name__icontains=keyword) | Q(corporation__name__icontains=keyword)
        if name_query.children:
            query &= name_query
    
    if filters.get("welfare"):
        query &= Q(welfare__in=filters["welfare"])
    
    if filters.get("area0"):
        query &= Q(area1__area0__id__in=filters["area0"])
    
    if filters.get("area1"):
        query &= Q(area1__id__in=filters["area1"])
    
    if filters.get("category00"):
        query &= Q(category00__id__in=filters["category00"])
    if filters.get("category01"):
        query &= Q(category01__id__in=filters["category01"])
    if filters.get("category10"):
        query &= Q(category10__id__in=filters["category10"])
    if filters.get("category11"):
        query &= Q(category11__id__in=filters["category11"])
    
    if filters.get("corporation"):
        corp_query = Q()
        for keyword in filters["corporation"]:
            corp_query |= Q(corporation__name__icontains=keyword)
        if corp_query.children:
            query &= corp_query
    
    if authority == 2:
        query &= Q(status=True) & Q(period__gt=now())
    
    return Offer.objects.filter(query)
