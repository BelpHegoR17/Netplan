from django.shortcuts import get_object_or_404, render, redirect
from .models import Device
from .forms import DeviceForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serialisers import DeviceSerializer

# Create your views here.

def home(request):
    devices = Device.objects.order_by("ip_address")
    count = Device.objects.count()
    ucount = Device.objects.filter(status = "UP").count()
    dcount = Device.objects.filter(status="DOWN").count()
    return render(request, "home.html", {'devices':devices, 'count': count,'ucount':ucount, 'dcount':dcount})

def add_devices(request):
    if request.method=="POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = DeviceForm()

    return render(request, "add_devices.html", {"form": form})

def online_devices(request):
    devices = Device.objects.all()
    return render(request,"online_devices.html", {"devices":devices})

def delete(request,id):
    device = Device.objects.get(id=id)
    device.delete()
    return redirect("home")

def edit_device(request,id):
    device = get_object_or_404(Device,id=id)

    if request.method=="POST":
        form=DeviceForm(request.POST,instance=device)
        if form.is_valid():
            form.save()
            return redirect("home")
        
    else:
        form=DeviceForm(instance=device)

    return render(request,"edit_device.html",{"form":form,"device":device})


@api_view(["GET"])
def device_list_api(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)