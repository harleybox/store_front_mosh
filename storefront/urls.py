from django.contrib import admin
from django.urls import path, include

#整个站点的设置
admin.site.site_header = "Storefront Admin"
admin.site.site_title = "Storefront Admin Portal"
admin.site.index_title = "Welcome to Storefronts Researcher Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls' )),
    path("__debug__/", include("debug_toolbar.urls")),
]
