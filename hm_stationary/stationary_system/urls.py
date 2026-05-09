from django.urls import path

from .views import login
from .views.admin_views import admin_nav_bar, dashboard, customers, activities, stationaries, payments
from .views.stationary_views import s_activities, s_dashboard, nav_bar, s_payments
from .views.customer_views import c_dashboard, c_activities, notifications, payment


urlpatterns = [
    # login 
    path('admin/', login.login_page_admin, name='login_page_admin'),
    path('stationary/', login.login_page_stationary, name='login_page_stationary'),
    path('customer/', login.login_customer, name='login_page_customer'),
    path('customer/signup/', login.signup, name='signup_customer'),
    path("ping/", login.ping),

    # admin site
    path('admin/dashboard/', dashboard.admin_dashboard, name='admin_dashboard'),
    path('admin/activities/', activities.admin_activities, name='admin_activities'),
    path('admin/preview_activity/<str:activity_id>/', activities.preview_activity, name='admin_preview_activity'),
    path('admin/delete_activity/<str:activity_id>/', activities.delete_activity, name='admin_delete_activity'),
    path('admin/stationaries/', stationaries.admin_stationaries, name='admin_stationaries'),
    path('admin/payments/', payments.payments_list, name='admin_payments'),
    path('admin/payments-delete/', payments.delete_all_payments, name='delete_all_payments'),


    # other admin pages
    path('admin/register_stationary/', stationaries.register_stationary, name='register_stationary'),
    path('admin/save_stationary/', stationaries.save_stationary, name='save_stationary'),
    path('admin/register_validation/', stationaries.register_validation, name='register_validation'),

    path('admin/preview_stationary/<str:username>/', stationaries.preview_stationary, name='preview_stationary'),
    path('admin/delete_stationary/<str:username>/', stationaries.delete_stationary, name='admin_delete_stationary'),

    path('admin/customers/', customers.admin_customers, name='admin_customers'),
    path('admin/preview_customer/<int:user_id>/', customers.preview_customer, name='preview_customer'),
    path('admin/notifications/', admin_nav_bar.admin_notifications, name='admin_notifications'),
    path('admin/activity/mark-pending/', activities.mark_activity_pending, name='mark_pending'),
    path('admin/activity/delete-notification/', activities.delete_notifications, name='admin_delete_notification'),
    path('admin/user/', admin_nav_bar.admin_user, name='admin_user'),


    # stationary site
    path('stationary/dashboard/', s_dashboard.stationary_dashboard, name='stationary_dashboard'),
    path('stationary/activities/', s_activities.stationary_activities, name='stationary_activities'),

    # other stationary pages
    path('stationary/preview_activity/<str:activity_id>/', s_activities.preview_stationary_activity, name='preview_stationary_activity'),
    path('stationary/process_activity/<str:activity_id>/', s_activities.process_activity, name='process_activity'),
    path('stationary/download_all_files/<str:activity_id>/', s_activities.download_all_files, name='download_all_files'),
    path('stationary/send_costs/', s_activities.send_cost, name='send_cost'),
    path('stationary/accept_activity/<str:activity_id>/', s_activities.accept_activity, name='accept_activity'),
    path('stationary/decline_activity/<str:activity_id>/', s_activities.decline_activity, name='decline_activity'),
    path('stationary/notifications/', nav_bar.notifications, name='stationary_notifications'),
    path('stationary/user/', nav_bar.user, name='stationary_user'),
    
    # payments
    path('stationary/payments/', s_payments.payments_list, name='stationary_payments'),
    path('stationary/payments-delete/', s_payments.delete_all_payments, name='stationary_delete_all_payments'),


    # customer site    
    path('customer/dashboard/', c_dashboard.customer_dashboard, name='customer_dashboard'),
    path('customer/payment/<str:activity>', c_dashboard.make_payment, name='payment'),

    path('customer/submit_payment/', payment.submit_payment, name='submit_payment'),

    path('customer/more-services/', c_dashboard.more_services, name='more_services'),
    path('customer/implementation/', c_dashboard.implementation, name='implementation'),


    path('customer/printing/', c_activities.printing, name='printing'),
    path('customer/typing_editng/', c_activities.typing_editing, name='typing_editing'),
    
    path('customer/preview-activity/<str:activity_id>/', c_activities.preview_activity, name='preview_activity'),
    path('customer/delete-pending-activity/<str:activity_id>/', c_activities.delete_pending_activity, name='delete_pending_activity'),
    path('customer/edit-activity/<str:activity_id>/', c_activities.edit_activity, name='edit_activity'),
    path('customer/customer-activity-history/', c_activities.customer_activity_history, name='customer_activity_history'),
    path('customer/delete-uploaded-file/<int:file_id>/', c_activities.delete_uploaded_file, name='delete_uploaded_file'),
    path('customer/download-processed-file/<int:file_id>/', c_activities.download_processed_file, name='download_customer_processed_file'),

    

    
    # logout
    path('logout/', login.stationary_logout, name='stationary_logout'),
    path('admin/logout/', login.admin_logout, name='admin_logout'),
    path('customer/logout/', login.customer_logout, name='customer_logout'),
    path('change-password/', login.change_password, name='change_password'),


    path('notifications/', notifications.get_notifications, name='get_notifications'),
    path('notifications/read/', notifications.mark_notification_read, name='mark_notification_read'),
    path("notifications/delete/", notifications.delete_notification, name="delete_notification"),
]