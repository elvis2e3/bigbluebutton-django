
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import json

from .forms import CreateMeetingForm
from .models import BBBMeeting


def index(request):

   if request.method == 'POST':
        form = CreateMeetingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'created succesfully')
        else:
            messages.warning(request, 'Cannot insert new meeting in database')

   open_meetings = []
   bbb_meeting = BBBMeeting.get_meetings_list()
   filtro = []
   for m in bbb_meeting:
       # if m['meetingID'][0:6] == "prueba":
       filtro.append(m)
       open_meetings.append(m['meetingID'])

   context = {
        'open_meetings': open_meetings,
        'live_meetings': filtro,
        'meetingsdb': BBBMeeting.objects.all().order_by('meetingID'),
        'form': CreateMeetingForm()
    }

   return render(request, 'bbb/index.html', context)


def create_meeting(request, meetingID):
    try:
        meeting = BBBMeeting.objects.get(meetingID=meetingID)
        parameters = BBBMeeting.modelfield_to_url(meeting)
        result = BBBMeeting.create_meeting(parameters)
        BBBMeeting.catch_messages(request, result)

        open_meetings = []
        for m in BBBMeeting.get_meetings_list():
            open_meetings.append(m['meetingID'])

        context = {
            'open_meetings': open_meetings,
            'live_meetings': BBBMeeting.get_meetings_list(),
            'meetingsdb': BBBMeeting.objects.all().order_by('meetingID'),
            'form': CreateMeetingForm()
        }
    except:
        messages.warning(request, 'Tenemos problemas de conexión.')
    return redirect('/panel')



def join_meeting(request, meetingID):
    # if request.user.is_authenticated:
    print("entro a la reunion")
    meeting = BBBMeeting.objects.get(meetingID=meetingID)
    full_name = '%s %s %s' % (
    request.user.usuario.nombres, request.user.usuario.apellido_paterno, request.user.usuario.apellido_materno)
    print("nombre:", full_name)
    password = getattr(meeting, 'moderatorPW')
    if len(meeting.salas.all()) > 0:
        if meeting.moderador.id == request.user.usuario.id:
            join_url = BBBMeeting.join_meeting(meetingID, password, full_name)
        else:
            join_url = BBBMeeting.join_meeting(meetingID, "estudiante", full_name)
    else:
        join_url = BBBMeeting.join_meeting(meetingID, password, full_name)
    return redirect(join_url)
    # else:
    #     return redirect("/")


def attjoin(request):


        meetingID = request.POST.get('meetingID')
        attname = request.POST.get('attname')
        attpassword = request.POST.get('attpassword')
        print(request.POST.get('meetingID'))
        join_url = BBBMeeting.join_meeting(meetingID, attpassword, attname)
        print(join_url)

        return redirect(join_url)



def end_meeting(request, meetingID):
    try:
        meeting = BBBMeeting.objects.get(meetingID=meetingID)
        password = getattr(meeting, 'moderatorPW')
        BBBMeeting.end_meeting(meetingID, password)
        messages.warning(request, 'La reunion fue detenida.')
    except:
        pass
    return redirect('/panel')


def info_meeting(request, meetingID):

    meeting = BBBMeeting.objects.get(meetingID=meetingID)
    password = getattr(meeting, 'moderatorPW')
    info = BBBMeeting.get_meeting_info(meetingID, password)


    return JsonResponse(info)


