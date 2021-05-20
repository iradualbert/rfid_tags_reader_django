import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from background_task import background
from .reader.alien import TagReader
from .models import Profile, Tag, Entry, Bag




def index(request):
    if 2 == 2:
        print(locals())
        import json
        l = str(locals())
        return JsonResponse({"locals": l})
    return HttpResponse('Scanning Tags')


def get_bag_info(request):
    bag = Bag.objects.all()[0]
    return JsonResponse(bag.to_json())

def get_tags(request):
    tags = Tag.objects.all()
    return JsonResponse({
        "tags": [x.to_json() for x in tags]
    })
    
    
def get_entries(request):
    auth_token = request.GET.get('auth_token', None)
    if auth_token is None:
        return JsonResponse({'message': 'Not authenticated'}, status=400)
    user = Profile.get_profile(auth_token)
    if user is None:
        return JsonResponse({'message': 'Invalid Token'}, status=400)
    entries = Entry.objects.filter(user=user).order_by('-registered_at')[0:10]
    return JsonResponse({
        "entries": [x.to_json() for x in entries]
    })
    
@require_POST
@csrf_exempt
def login(request):
    data = json.loads(request.body)
    username = data.get('username')
    auth_key = data.get('auth_key')
    profile = Profile.authenticate(username=username, auth_key=auth_key)
    if profile:
        return JsonResponse({"auth_token": profile.auth_token, "first_name": profile.user.first_name, "username": username })
    
    return JsonResponse({'error': 'Invalid Login'}, status=400)

@background(schedule=2)
def start_rfid_reader():
    try:
        reader = TagReader()
        reader.start()
    except Exception as e:
        print(e)
        raise e
start_rfid_reader()