from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

from django.http import JsonResponse
from django.core import serializers
from users.models import Module
from users.models import Class
from schedule import algo
import schedule.export_to_gcal

@login_required
def home(request):
    return render(request, 'schedule/home.html')


@login_required
def generateSchedule(request):
    if request.method == "POST":
        algo.run()
        messages.success(request, "Generating Schedule...")

    return render(request, 'schedule/generateSchedule.html')

def make_temp_model(data):
    FilteredResults.objects.delete()
    for i in data:
        FilteredResults(title=i["title"],start=i["start"],end=i["end"],description=i["description"],location=i["location"])
        FilteredResults.save()

def return_data(request,Classs = "",modyews = ""):
    json_serializer = serializers.get_serializer("json")()
    # obj = json_serializer.serialize(Class.timetable_objects.all(), ensure_ascii=False)
    # out = open("testJSON1.json", "w")
    # out.write(obj)
    # out.close()
    if Classs == "" and modyews == "":
        data = list(Class.objects.values('title', 'start','end','description','location'))
    else:
        if Classs != "" and modyews == "":
            if Classs == "courses":
                data = list(Class.objects.values('title').distinct())
            else:
                data = []
                if "Class" in Classs:
                    classes = Classs.split(" ")
                    for i in classes:
                        if i != "Class":
                            qsetclass = Class.objects.filter(class_related__contains = i)
                            data.extend(list(qsetclass.values('title', 'start','end','description','location')))
                else:
                    courses = Classs.split("+")
                    for i in courses:
                        qsetcourse = Class.objects.filter(title__contains = i)
                        data.extend(list(qsetcourse.values('title', 'start','end','description','location')))
                # else:
                #     qset1 = Class.objects.filter(class_related__contains = Classs)
                #     data = list(qset1.values('title', 'start','end','description','location'))
        else:
            courses = Classs.split()
            data = []
            for i in courses:
                qset = list((Class.objects.filter(title__contains = i)).values('title', 'start','end','description','location'))
                data.extend(qset)   

    # data = {
    #     'events': Module.timetable_objects.values('title', 'start','end','description','location')
    # }
    print(data)
    print (Classs)
    #make_temp_model(json_response.content)
    return JsonResponse(data, safe = False)


def runAlgo(request):
    reply = "nope"
    #if request.method == "POST": #os request.GET()
    reply = "yep"
    algo.run()
    messages.success(request, "Generating Schedule...")
    return HttpResponse(reply)

def gcalExport(request):
    if request.method == 'POST':
        # post_text = request.POST.get('the_post')
        # response_data = {}

        # post = Post(text=post_text, author=request.user)
        # post.save()

        # response_data['result'] = 'Create post successful!'
        # response_data['postpk'] = post.pk
        # response_data['text'] = post.text
        # response_data['created'] = post.created.strftime('%B %d, %Y %I:%M %p')
        # response_data['author'] = post.author.username
        print("YEET")
        django.mysite.schedule.export_to_gcal.main()
        return HttpResponse("Completed export to Google Calendar!" )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )