from django.http import HttpResponse, JsonResponse
from background_task import background
from .reader.alien import read_tags
from .models import Tag, Entry





def index(request):
    return HttpResponse('Scanning Tags')



def get_tags(request):
    tags = Tag.objects.all()
    return JsonResponse({
        "tags": [x.to_json() for x in tags]
    })
    
    
def get_entries(request):
    entries = Entry.objects.all().order_by('left_at')
    return JsonResponse({
        "entries": [x.to_json() for x in entries]
    })

@background(schedule=2)
def start_rfid_reader():
    read_tags()

start_rfid_reader()