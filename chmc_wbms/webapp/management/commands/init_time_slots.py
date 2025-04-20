from django.core.management.base import BaseCommand
from django.utils import timezone
from webapp.models import TimeSlot
from datetime import time, timedelta
import datetime

class Command(BaseCommand):
    help = 'Initialize time slots for appointments'
    
    def handle(self, *args, **options):
        # Clear existing slots
        TimeSlot.objects.all().delete()
        
        # Morning slots (8AM - 12NN)
        current_time = time(8, 0)
        while current_time < time(12, 0):
            end_time = (datetime.datetime.combine(timezone.now().date(), current_time) + 
                       timedelta(minutes=10)).time()
            TimeSlot.objects.create(start_time=current_time, end_time=end_time)
            current_time = end_time
        
        # Afternoon slots (2PM - 5PM)
        current_time = time(14, 0)
        while current_time < time(17, 0):
            end_time = (datetime.datetime.combine(timezone.now().date(), current_time) + 
                       timedelta(minutes=10)).time()
            TimeSlot.objects.create(start_time=current_time, end_time=end_time)
            current_time = end_time
            
       # Special slots
        TimeSlot.objects.create(
            start_time=time(8, 0),
            end_time=time(12, 0),
            is_special=True,
            special_type='MORNING'
        )
        
        TimeSlot.objects.create(
            start_time=time(14, 0),
            end_time=time(17, 0),
            is_special=True,
            special_type='AFTERNOON'
        )
        
        TimeSlot.objects.create(
            start_time=time(8, 0),
            end_time=time(17, 0),
            is_special=True,
            special_type='DAY'
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully created time slots with whole day options'))