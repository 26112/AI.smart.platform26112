from django.contrib import admin
from .models import AIServiceLog


@admin.register(AIServiceLog)
class AIServiceLogAdmin(admin.ModelAdmin):
    """
    Admin interface for viewing AI service usage logs
    """
    list_display = [
        'service_name', 
        'status', 
        'user_identifier', 
        'response_time_ms', 
        'timestamp'
    ]
    list_filter = ['service_name', 'status', 'timestamp']
    search_fields = ['service_name', 'user_identifier', 'error_message']
    readonly_fields = [
        'service_name', 
        'user_identifier', 
        'request_payload', 
        'status', 
        'error_message', 
        'response_time_ms', 
        'timestamp'
    ]
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        """Logs are created automatically, not manually"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Keep logs for audit trail"""
        return request.user.is_superuser

