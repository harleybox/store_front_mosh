from django.contrib import admin, messages
from django.db.models import Count
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.html import format_html, urlencode

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ["collection"]  # 下拉菜单搜索功能
    prepopulated_fields = {"slug": ["title"]}
    actions = ["clear_inventory"]
    list_display = [
        "title",
        "unit_price",
        "inventory_status",
        "collection_title",
    ]  # 用'collection'这个代替自定义的字段，因为collection的return self.title，所以最终是显示collection的title;如果要显示指定的字段，添加函数collection_title为新的字段
    search_fields = ["title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    list_select_related = [
        "collection"
    ]  # 用到自定义函数字段的时候，优化效率，减少查询次数 //一对多的关系，用select_related

    def collection_title(self, product):
        return product.collection.title

    # 添加自定义的字段
    @admin.display(ordering="inventory")  # 让自定义的字段可以排序，排序的字段是product里的inventory
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated.",
            messages.ERROR,
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "membership",
    ]
    # ordering = ['first_name', 'last_name'] # 写到模块的meta里面了
    list_editable = ["membership"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    @admin.display(ordering="orders_count")
    def orders(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{} Orders</a>', url, customer.orders_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ["product"]
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = [
        "id",
        "placed_at",
        "payment_status",
        "customer",
    ]  # 在customer的模型里面要定义__str__方法，否则显示的是customer object
    list_per_page = 10
    list_select_related = [
        "customer"
    ]  # 用到自定义函数字段的时候，优化效率，减少查询次数 //一对多的关系，用select_related


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ["featured_product"]
    list_display = ["title", "products_count"]
    search_fields = ["title"]
    list_per_page = 10

    @admin.display(ordering="products_count")  # 可以排序
    def products_count(self, collection):
        # 返回带连接的html字段,反向指向product的changelist
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

        # 返回没有链接的字段
        # return collection.products_count #并没有这个字段，所以需要annotation,用自定义的get_queryset方法

    # 重写base queryset的方法，修改在admin页面显示的数据，添加了聚合的数据
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .annotate(products_count=Count("product"))  # 在默认的方法后面加上.annotate
        )


# admin.site.register(models.Product, ProductAdmin) #因为有上面的装饰器，所以这里就不需要了
