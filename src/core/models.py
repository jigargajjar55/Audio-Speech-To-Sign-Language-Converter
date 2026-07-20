from django.db import models
from django.contrib.auth.models import User

class TranslationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='translations')
    input_text = models.TextField()
    stitched_video_path = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.input_text[:20]}"
