from .models import SystemAuditLog

class AuditLogMixin:
    """
    Mixin to automatically log create, update, and delete actions to SystemAuditLog.
    """
    def _log_action(self, action, instance, description=""):
        user = self.request.user if self.request.user.is_authenticated else None
        model_name = instance._meta.verbose_name
        object_repr = str(instance)
        
        # Get IP address
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        SystemAuditLog.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=str(instance.pk),
            object_repr=object_repr,
            change_message=description,
            ip_address=ip,
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')
        )

    def perform_create(self, serializer):
        instance = serializer.save()
        self._log_action("CREATE", instance, "Created new record")

    def perform_update(self, serializer):
        instance = serializer.save()
        self._log_action("UPDATE", instance, "Updated record")

    def perform_destroy(self, instance):
        # Log before destroying to capture regular representation
        self._log_action("DELETE", instance, "Deleted record")
        instance.delete()
