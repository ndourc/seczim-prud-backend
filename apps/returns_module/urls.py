from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PrudentialReturnViewSet, IncomeStatementViewSet, BalanceSheetViewSet
)

router = DefaultRouter()
router.register(r'prudential-returns', PrudentialReturnViewSet)
router.register(r'income-statements', IncomeStatementViewSet)
router.register(r'balance-sheets', BalanceSheetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
