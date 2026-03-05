import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Cliente, Coche, Servicio, CocheServicio


# Create your views here.

def vista_cliente(request):
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "email").get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)

@csrf_exempt
def registrarCliente(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data["nombre"],
                telefono=data["telefono"],
                email=data["email"],
            )
            return JsonResponse({"mensaje": "Cliente registrado con exito", "cliente_id": cliente.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrarCoche(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data["cliente_id"])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data["marca"],
                modelo=data["modelo"],
                matricula=data["matricula"],
            )
            return JsonResponse({"mensaje": "Coche registrado con exito", "coche_id": coche.id})
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrarServicio(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data["coche_id"])
            servicio = Servicio.objects.create(
                nombre=data["nombre"],
                descripcion=data["descripcion"],
            )

            CocheServicio.objects.create(coche=coche, servicio=servicio)

            return JsonResponse({"mensaje": "Servicio registrado con exito", "servicio_id": servicio.id})
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)

    return JsonResponse({"error": "metodo no permitido"}, status=405)

@csrf_exempt
def buscarCochesByMarca(request, marca):
    try:
        coches = list(Coche.objects.filter(marca=marca).values("modelo"))
        return JsonResponse(coches, safe=False)

    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)

@csrf_exempt
def buscarCochesByMarcaAndCliente(request, marca, cliente_id):
    try:
        coches = list(Coche.objects.filter(marca=marca, cliente_id=cliente_id).values("marca", "modelo", "matricula"))
        return JsonResponse(coches, safe=False)

    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)