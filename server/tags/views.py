from django.http import HttpResponse, JsonResponse
from background_task import background
from .reader.alien import TagReader
from .models import Tag, Entry



def index(request):
    if 2 == 2:
        print(locals())
        import json
        l = str(locals())
        return JsonResponse({"locals": l})
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
    try:
        reader = TagReader()
        reader.start()
    except Exception as e:
        print(e)
        raise e
start_rfid_reader()