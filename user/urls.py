from django.urls import path
from .  import views
from django.conf import settings
from django.conf.urls.static import static

 
urlpatterns = [
    path("login",views.login,name="login"),
    path("register",views.register,name="register"),
    path("",views.home,name="home"),
    path("shop",views.shop,name="shop"),
    path("otp",views.otp,name="otp"),
    path("s!<type>!<name>",views.sortshop,name="sort"),
    path("logout",views.logout,name="logout"),
    path("details!<type>",views.details,name="details"),
    path("cart",views.cart,name="cart"),
    path("test",views.test,name="test"),
    path("add_cart",views.add_cart,name="add_cart"),
    path("remove_frm_cart",views.remove_frm_cart,name="remove_frm_cart"),
    path("quant_add",views.quant_add,name="quant_add"),
    path("add_to_wishlist",views.add_to_wishlist,name="add_to_wishlist"),
    path("wishlist",views.wishlist,name="wishlist"),
    path("checkout!<value>",views.checkout,name="checkout"),
    path("placeorder!<id>",views.Placeorder,name="placeorder"),
    path('oders',views.oders,name="orders"),
    path('view-oders!<id>',views.view_oders,name="veiw_oders"),
    path('cancel-order',views.cancelorder,name="canceloders"),
    path('confirm',views.confirm,name="comfirm"),
    path('profile',views.user_profile,name="profile"),
    path('apply_cop',views.apply_coupon,name="apply_coupon"),
    path('return-order',views.returnorder,name="returnorder"),
    path('searched',views.searched,name="searched"),
    path("remove_frm_wishlist",views.remove_frm_wishlist,name="remove_frm_wishlist"),
    path("editaddres!<id>",views.edit_address,name="edit_address"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'user.views.error_404'
handler500 = 'user.views.error_500'
