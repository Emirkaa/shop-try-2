from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import *



urlpatterns = [
    path('', views.home_page, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
    path('category-title/<val>', views.CategoryTitle.as_view(), name='category-title'),
    path('productdescription/<int:pk>', views.ProductDetail.as_view(), name='productdescription'),
    path('address/', views.address, name='address'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('updateAddress/<int:pk>', views.UpdateAddress.as_view(), name='updateAddress'),



    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.order_page, name='orders'),
    
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name = 'minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),

    path('pluswishlist/',views.plus_wishlist),


    # Аунтефикация входа
    path('registration/', views.CustomerRegistrationView.as_view(), name='registration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='store/login.html', authentication_form=LoginForm), name='login'),
    path('resetpass/', auth_view.PasswordResetView.as_view(template_name='store/resetpass.html', form_class=MyPasswordResetForm), name='resetpass'),
    path('passchange/', auth_view.PasswordChangeView.as_view(template_name='store/passchange.html',form_class=MyPasswordChangeForm, success_url='/passchangedone'),name='passchange'),
    path('passchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='store/passchangedone.html'),name='passchangedone'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),

    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='store/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password_reset/done', auth_view.PasswordResetDoneView.as_view(template_name='store/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='store/password_reset_confirm.html', form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='store/password_reset_complete.html'), name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)