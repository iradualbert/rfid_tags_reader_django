from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    tag_name = models.CharField(max_length=100, unique=True)
    is_taken = models.BooleanField(default=False)
    has_left = models.BooleanField(default=False)
    last_time_taken = models.DateTimeField(null=True, blank=True)
    last_time_left = models.DateTimeField(null=True, blank=True)
    recent_user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, blank=True
    )

    def __str__(self):
        return self.tag_name

    def to_json(self):
        return {
            "tag_name": self.tag_name,
            "tag_id": self.tag_name,
            "is_taken": self.is_taken,
            "has_left": self.has_left,
        }
    
    @property
    def is_returning(self):
        return self.has_left
    
    @property
    def is_leaving(self):
        if self.is_taken:
            if self.has_left:
                return False
            return True
        return False
        # return (self.is_taken and not self.has_left)
    
    

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entries")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="entries")
    antenna = models.CharField(max_length=30, null=True, blank=True)
    registered_at = models.DateTimeField(default=datetime.utcnow)
    left_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.tag.tag_name} - {self.antenna}"

    def save(self, *args, **kwargs):
        if not self.returned_at:
            self.tag.is_taken = True
            self.tag.recent_user = self.user
            if self.left_at:
                self.tag.has_left = True
                self.tag.last_time_taken = self.registered_at
                self.tag.last_time_left = self.left_at
        if self.returned_at:
            self.tag.is_taken = False
            self.tag.has_left = False
        self.tag.save()
        return super().save(*args, **kwargs)
    
    def delete(self):
        raise "An entry instance can not be deleted."
    
    def get_user_json(self):
        return {"username": self.user.username}

    def to_json(self):
        return {
            "tag": self.tag.to_json(),
            "user": self.get_user_json(),
            "left_at": self.left_at,
            "antenna": self.antenna,
            "returned_at": self.returned_at,
        }
