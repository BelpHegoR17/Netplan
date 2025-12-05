from django.shortcuts import get_object_or_404, render, redirect
from .models import Device
from .forms import DeviceForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serialisers import DeviceSerializer
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from devices.permissions import SunilcanEditOnly

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
    print("TRACE: Entered function device_list_api - FBV", "user:", getattr(request, "user", None), "auth:", getattr(request, "user", "Anonymous"))
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def device_detail_api(request, id):
    try:
        device = Device.objects.get(id=id)
    except Device.DoesNotExist:
        return Response({"error":"Device not found"}, status=404)
    
    serialiser = DeviceSerializer(device)
    return Response(serialiser.data)

@api_view(["POST"])
def add_device_api(request):
    serialiser = DeviceSerializer(data=request.data)

    if serialiser.is_valid():
        serialiser.save()
        return Response(serialiser.data, status=201)
    
    return Response(serialiser.errors, status=400)

@api_view(["PUT","PATCH"])
def update_api(request,id):
    try:
        device = Device.objects.get(id=id)
    except Device.DoesNotExist:
        return Response({"error":"Device not found"}, status = 201)
    
    partial = True if request.method=="PATCH" else False
    serialiser = DeviceSerializer(device, data=request.data, partial=partial)

    if serialiser.is_valid():
        serialiser.save()
        return Response({"message":"Device updated", "data":serialiser.data})
    
    return Response(serialiser.errors, status=400)

@api_view(["DELETE"])
def delete_device_api(request,id):
    try:
        device = Device.objects.get(id=id)
    except Device.DoesNotExist:
        return Response({"error":"Device not found"}, status=404)
    
    device.delete()
    return Response({"message":"Device deleted successfully"}, status=204)

# ALLOWED_SORT_FIELDS = ['name','-name','id','-id','status','-stauts']
# @api_view(["GET"])
# def device_list_api(request):
#     devices = Device.objects.all()

#     status = request.GET.get("status")
#     device_type = request.GET.get("device_type")
#     location = request.GET.get("location")
#     search = request.GET.get("search")

#     if status:
#         devices = devices.filter(status = status)
#     if device_type:
#         devices = devices.filter(device_type=device_type)
#     if location:
#         devices = devices.filter(location=location)
#     if search:
#         devices = devices.filter(status__icontains=search)
    
#     serialiser = DeviceSerializer(devices, many=True)
#     return Response(serialiser.data)


# def device_list_api(request):
#     device = Device.objects.all()

#     order = request.query_params.get("ordering")

#     if order in ALLOWED_SORT_FIELDS:
#         device = device.order_by(order)

#     return Response(DeviceSerializer(device, many = True).data)

# class DeviceList(ListAPIView):
#     queryset = Device.objects.all()
#     serializer_class = DeviceSerializer
#     filter_backends = [OrderingFilter]
#     ordering_fields = ['name','status','location','id']
#     ordering = ['id']

class DeviceViewset(ModelViewSet):

    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [SunilcanEditOnly]


    @action(detail=True, methods=['POST'])
    def reboot(self, request, pk=None):
        device = self.get_object()
        return Response({"message": f"{device.name} rebooted successfully"})