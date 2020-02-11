from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from setting.models import Vehicle
from vendor.models import Driver
from django.contrib import messages
from django.core import serializers
from .models import User
import json,requests

# Get Vehicle list for vendor DataTable
def get_vehicle_list(request):
    vendor_id = request.POST.get('vendor_id')
    draw = int(request.GET.get("draw", 0))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 7))

    all_objects = Vehicle.objects.filter(vendor_id=vendor_id)
    filtered_count = all_objects.count()
    total_count = Vehicle.objects.count()
    data = serializers.serialize('json', all_objects)

    json_objects = json.loads(data)
    list_objects = []
    for index in range(len(json_objects)):
        json_objects[index]['fields']['id'] = all_objects[index].id
        json_objects[index]['fields']['status_id'] = all_objects[index].status
        result = json_objects[index]['fields']['status']
        if(result == 1):
            json_objects[index]['fields']['status'] = 'Active'
        elif(result == 0):
            json_objects[index]['fields']['status'] = 'Inactive'
        elif(result == 2):
            json_objects[index]['fields']['status'] = 'Booked'
        else:
            json_objects[index]['fields']['status'] = 'Deleted'
        list_objects.append(json_objects[index]['fields'])

    return HttpResponse(json.dumps(list_objects), content_type='application/json;charset=utf-8')

# Delete Functionality for vehicle Listing on vendor
def delete_vehicle(request):
    result = {}
    if request.method == 'POST' and request.is_ajax():
        try:
            vehicleId = request.POST.get('id', '')
            response = Vehicle.objects.filter(pk=vehicleId).update(status=3)
            if (response == True):
                result['status'] = True
                result['msg'] = 'Vehicle Deleted Successfully successfully!'
                return JsonResponse(result)
            else:
                result['status'] = False
                result['msg'] = 'Something went wrong!'
                return JsonResponse(result)
        except Http404:
            return HttpResponseRedirect("/vendor/vendor/view/")
    else:
        return HttpResponse('Invalid request passed')

# Driver Listing for Vendor Section
def get_driver_list(request):
    vendor_id = request.POST.get('vendor_id')
    print(vendor_id)
    draw = int(request.GET.get("draw", 0))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 7))

    all_objects = Driver.objects.filter(vendor_id=vendor_id)
    filtered_count = all_objects.count()
    total_count = Driver.objects.count()
    data = serializers.serialize('json', all_objects)

    json_objects = json.loads(data)
    list_objects = []
    for index in range(len(json_objects)):
        json_objects[index]['fields']['id'] = all_objects[index].id
        json_objects[index]['fields']['status_id'] = all_objects[index].status
        result = json_objects[index]['fields']['status']
        if(result == 1):
            json_objects[index]['fields']['status'] = 'Active'
        elif(result == 0):
            json_objects[index]['fields']['status'] = 'Inactive'
        elif(result == 2):
            json_objects[index]['fields']['status'] = 'Booked'
        else:
            json_objects[index]['fields']['status'] = 'Deleted'
        list_objects.append(json_objects[index]['fields'])

    return HttpResponse(json.dumps(list_objects), content_type='application/json;charset=utf-8')

def GetUserDataByType(request):
    userData = User.objects.filter(type=request.POST.get('user_type')).filter(status = 1).values('id','first_name','last_name','email')
    result = {}
    if not userData:
        result['status'] = False
        result['data'] = 'Data Not Found'
    else:
        result['status'] = True
        result['data'] = list(userData)
   
    return JsonResponse(result)

def GetVehicleDetailById(request):
    vehicleData = Vehicle.objects.filter(id=request.POST.get('vehicleId')).filter(status = 1).values('vehicle_no','chassis_no','mileage','vehicle_category')
    result = {}
    if not vehicleData:
        result['status'] = False
        result['data'] = 'Data Not Found'
    else:
        result['status'] = True
        result['data'] = list(vehicleData)
    return JsonResponse(result)

def GetLatLongByAddress(request):
    api_key = "AIzaSyAjRK7OqmoYM-KJki3hji4vZo6SiMl_nWA"
    origin_address=request.POST.get('origin')
    destination_address=request.POST.get('destination')
    origin_api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(origin_address, api_key))
    destination_api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(destination_address, api_key))
    origin_api_response_dict = origin_api_response.json()
    destination_api_response_dict = destination_api_response.json()
    response = {}
    if origin_api_response_dict['results'] and destination_api_response_dict['results']:
        origin_geocode = origin_api_response_dict['results'][0]['geometry']['location']['lat'] + ',' + origin_api_response_dict['results'][0]['geometry']['location']['lng']
        destination_geocode = destination_api_response_dict['results'][0]['geometry']['location']['lat'] + ',' + destination_api_response_dict['results'][0]['geometry']['location']['lng']
        response = {
            'status' : True,
            'origin' : origin_geocode,
            'destination': destination_geocode
        }
    else:
        response = {
            'status' : False,
            'origin' : '28.5052605,77.0827607',
            'destination' : '28.4616027,77.036577'
        }
        
    return JsonResponse(response, safe=False)