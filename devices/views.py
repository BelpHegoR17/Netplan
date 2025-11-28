from django.shortcuts import render, redirect
from .models import Device
from .forms import DeviceForm

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