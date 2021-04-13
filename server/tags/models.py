from datetime import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def now():
    return datetime.now(tz=timezone.utc)


class Antenna(models.Model):
    tag_id = models.CharField(max_length=40, unique=True)
    no = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=10, null=True, blank=True, editable=False)
    is_door = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        self.name = f"Ant:{self.no}"        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    @staticmethod
    def get_all():
        tags = {}
        for x in Antenna.objects.all():
            tags[x.tag_id] = x
        return tags
    
    @staticmethod
    def get_bag_antenna_names():
        return set(x.name for x in Antenna.objects.filter(is_door=False))
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tag_id = models.CharField(max_length=40, unique=True)
    onboard = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}"


    
    @staticmethod
    def get_all():
        tags = {}
        for x in Profile.objects.all():
            tags[x.tag_id] = x
        return tags
    
    def save(self, *args, **kwargs):
        if Tag.objects.filter(tag_id=self.tag_id).exists() or Antenna.objects.filter(tag_id=self.tag_id).exists():
            raise f"{self.tag_id} is not available"
        return super().save(*args, **kwargs)
        

class Bag(models.Model):
    name = models.CharField(max_length=40, unique=True)
    antenna = models.OneToOneField(Antenna, on_delete=models.SET_NULL, null=True, related_name="bag", unique=True)
    is_closed = models.BooleanField(default=True)
    current_user = models.OneToOneField(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return f"{self.name}"
    
    @property
    def total_tags(self):
        return self.tags.all().count()
    
    @property
    def missing_tags(self):
        return self.tags.all().filter(is_taken=True)
    
    @property
    def total_missing_tags(self):
        return self.missing_tags.count()
    
    def open(self, person:Profile):
        self.is_closed = False
        self.current_user = person
        person.onboard = True
        person.save()
        self.save()
        
        
    def close(self, person:Profile):
        self.is_closed = True
        self.current_user = None
        person.onboard = False
        person.save()
        self.save()

    


class Tag(models.Model):
    tag_id = models.CharField(max_length=40, unique=True)
    bag = models.ForeignKey(Bag, on_delete=models.SET_NULL, null=True, related_name="tags")
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tag_id} - {self.bag.name}"

    @staticmethod
    def get_all():
        tags = {}
        for x in Tag.objects.all():
            tags[x.tag_id] = x
        return tags

    def to_json(self):
        return {}
    
    def save(self, *args, **kwargs):
        if Profile.objects.filter(tag_id=self.tag_id).exists() or Antenna.objects.filter(tag_id=self.tag_id).exists():
            raise f"{self.tag_id} is not available"
        super().save(*args, **kwargs)


class Entry(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="entries")
    taken_tags = models.ManyToManyField(Tag, blank=True)
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(default=now)
    left_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    reason = models.TextField(blank=True)

    def __str__(self):
        count = self.total_tags
        return f"{self.registered_at} - {self.user} - {self.bag} - Total: {count}"
    
    @property
    def total_tags(self):
        return self.taken_tags.all().count()
    
    @property
    def taken(self):
        return ", ".join([x.tag_id for x in self.taken_tags.all()])

    def delete(self):
        raise "An entry instance can not be deleted."

    def get_user_json(self):
        return {"username": self.user.username}

    def to_json(self):
        return {}
