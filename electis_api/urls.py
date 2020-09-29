from django.contrib import admin
from django.urls import path

from modernrpc.views import RPCEntryPoint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rpc/', RPCEntryPoint.as_view(enable_doc=True)),
]


from api.async_example import index, async_view, smoke_some_meats

urlpatterns += [
    path("", index),
    path("async/", async_view),
    path("smoke_some_meats/", smoke_some_meats),
]