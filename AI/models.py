from account.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    _detections_count = models.PositiveIntegerField(default=0)
    last_reset = models.DateTimeField(default=timezone.now)
    premium_till = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.name

    def can_make_detection(self):
        if self.detections_allowed == -1:
            return True
        if self.last_reset.date() < timezone.now().date():
            self.reset_detections()
        return self.detections_count < self.detections_allowed

    def set_premium(self):
        self.premium_till = timezone.now() + timezone.timedelta(days=30)  # Set expiration date one month ahead
        self.save()

    @property
    def premium(self):
        if self.premium_till and self.premium_till < timezone.now():
            # Premium subscription has expired, return False
            return False
        return True
    
    @property
    def detections_allowed(self):
        return settings.DETECTIONS_ALLOWED_PREMIUM if self.premium else settings.DETECTIONS_ALLOWED_FREE

    @property
    def detections_count(self):
        if self.last_reset.date() < timezone.now().date():
            # Reset the detection count for a new day
            self.reset_detections()
        return self._detections_count

    @property
    def remaining_detections(self):
        remaining = self.detections_allowed - self.detections_count
        return max(remaining, 0)

    def reset_detections(self):
        # Reset the detection count for a new day
        self._detections_count = 0
        self.last_reset = timezone.now()
        self.save()

class Plant(models.Model):
    name = models.CharField(max_length=255)
    prediction_model = models.FileField(upload_to='prediction_models/',null=True)

    def __str__(self) -> str:
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=255)
    plant = models.ForeignKey(to=Plant, on_delete=models.CASCADE, related_name='diseases')
    keyword = models.IntegerField(blank=False, null=True)

    def __str__(self) -> str:
        return self.name
    class Meta:
        unique_together = ('plant', 'keyword',)
    
def user_directory_path(instance, filename):
    file_extension = filename.split(".")[-1] if filename.split(".") else ""
    file_name = f"{instance.uuid}.{file_extension}"
    return 'images/{0}/{1}'.format(instance.profile.user.name, file_name)

class Detection(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='detections')
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.DateTimeField(default=timezone.now)
    plant_type = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='plants')
    disease_detected = models.ForeignKey(Disease,null=True,blank=True, on_delete=models.CASCADE)
    _complete = models.BooleanField(default=False)
    completion_time = models.DateTimeField(null=True,blank=True)
    confidence = models.FloatField(null=True, blank=True)
    img_path = models.ImageField(upload_to=user_directory_path,null=True)


    def __str__(self):
        return f"Detection for {self.profile.user.name}"
    
    @property
    def time_taken(self):
        if self._complete:
            return round(self.completion_time.timestamp() - self.start_time.timestamp(),2)
        return "Pending"
    
    @property
    def disease(self):
        if self.disease_detected:
            return self.disease_detected.name
        return "-"