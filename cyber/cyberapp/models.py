from django.db import models
from django.utils import timezone

# Create your models here.
class Student(models.Model):
    firstname = models.CharField(max_length=20)
    lastname= models.CharField(max_length=20)
    idnumber = models.CharField(max_length=20, unique=True)
    phonenumber = models.IntegerField()

    def __str__(self):
        return f"{self.firstname} {self.lastname} {self.idnumber}"
    
class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"{self.student.firstname} - {self.amount}"


class Usage_sessions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def duration_hours(self):
        if self.end_date:
            duration = self.end_date - self.start_date
        else:
            duration = timezone.now() - self.start_date
        total_minutes = duration.total_seconds() / 60  # Convert seconds to minutes
        hours = int(total_minutes // 60)  # Get total hours
        minutes = int(total_minutes % 60)  # Get remaining minutes
        return f"{hours:02} hrs {minutes:02} mins"  # Format
    
    def amount_due(self, rate_per_day=100):
        hours = self.duration_hours()
        days = hours / 24
        return days * rate_per_day
    

    def __str__(self):
        return f"{self.student.firstname} - {self.start_date} to {self.end_date if self.end_date else 'ongoing'}"
    

    
    
