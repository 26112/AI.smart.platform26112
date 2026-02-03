from django.db import models
from django.utils import timezone


class AIServiceLog(models.Model):
    """
    Tracks usage of AI services for analytics and monitoring
    
    Production-level logging for:
    - Usage analytics
    - Performance monitoring
    - Debugging
    - Billing (future)
    """
    
    # Service information
    service_name = models.CharField(max_length=100, db_index=True)
    
    # User tracking (anonymous for now, can add FK to User later)
    user_identifier = models.CharField(
        max_length=100, 
        default='anonymous',
        help_text="User ID or 'anonymous'"
    )
    
    # Request details
    request_payload = models.TextField(
        null=True, 
        blank=True,
        help_text="Stored for debugging, consider privacy implications"
    )
    
    # Response tracking
    status = models.CharField(
        max_length=20,
        choices=[
            ('success', 'Success'),
            ('error', 'Error'),
        ],
        db_index=True
    )
    
    error_message = models.TextField(null=True, blank=True)
    
    # Performance metrics
    response_time_ms = models.IntegerField(
        help_text="Response time in milliseconds"
    )
    
    # Timestamps
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'AI Service Log'
        verbose_name_plural = 'AI Service Logs'
        indexes = [
            models.Index(fields=['-timestamp', 'service_name']),
            models.Index(fields=['status', 'service_name']),
        ]
    
    def __str__(self):
        return f"{self.service_name} - {self.status} - {self.timestamp}"
    
    @classmethod
    def get_service_stats(cls, service_name=None, days=7):
        """
        Get usage statistics for analytics
        
        Returns:
            dict: Statistics including total calls, success rate, avg response time
        """
        from django.db.models import Count, Avg
        from datetime import timedelta
        
        queryset = cls.objects.filter(
            timestamp__gte=timezone.now() - timedelta(days=days)
        )
        
        if service_name:
            queryset = queryset.filter(service_name=service_name)
        
        stats = queryset.aggregate(
            total_calls=Count('id'),
            success_count=Count('id', filter=models.Q(status='success')),
            avg_response_time=Avg('response_time_ms')
        )
        
        # Calculate success rate
        if stats['total_calls'] > 0:
            stats['success_rate'] = (stats['success_count'] / stats['total_calls']) * 100
        else:
            stats['success_rate'] = 0
        
        return stats
