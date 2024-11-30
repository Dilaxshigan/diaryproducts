from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .import views
from .views import checkout 
from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm
from django.contrib import admin

urlpatterns = [
    path("", views.home),
    path("about", views.about, name = "about"),
    path("contact", views.contact, name = "contact"),
    path("category/ <slug:val>", views.CategoryView.as_view(), name ="category"),
    path("categorytitle/ <val>", views.CategoryTitle.as_view(), name ="categorytitle"),
    path("productdetail/<int:pk>/", views.ProductDetail.as_view(), name="productdetail"),
    path("accounts/profile/", views.ProfileView.as_view(), name ="profile"),
    path("address/", views.address, name ="address"),
    path("updateaddress/ <int:pk>", views.updateAddress.as_view(), name ="updateAddress"),

    path("add-to-cart/", views.add_to_cart, name='add-to-cart'),
    path("cart/", views.show_cart, name='showcart'),
    path('checkout/', checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('search/', views.search, name='search'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('pluswishlist/', views.plus_wishlist),
    path('minuswishlist/', views.minus_wishlist),


    #login authentication
    path("registration/", views.CustomerRegistrationView.as_view(), name ="registration"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name='login'),
    path("password-change/", auth_views.PasswordChangeView.as_view(template_name="change_password.html", form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='change_password'),
    path("passwordchangedone/", auth_views.PasswordChangeDoneView.as_view(template_name="passwordchangedone.html"), name='passwordchangedone'),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html", form_class=MyPasswordResetForm), name='password_reset'),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html",form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header= "Fresh Milk Diary"
admin.site.site_title= "Fresh Milk Diary"
admin.site.site_index_title= "Welcome to Fresh Milk Diary"