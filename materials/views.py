from math import radians, cos, sin, asin, sqrt
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from .models import Material
from .serializers import MaterialSerializer, MaterialContactSerializer, MaterialMapSerializer
from .permissions import IsBuyer


class MaterialListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        materials = Material.objects.filter(user=request.user)
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Material, pk=pk)

    def get(self, request, pk):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    def put(self, request, pk):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data)  # <== to'g'ri
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        material = self.get_object(pk)
        material.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MaterialRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Material, pk=pk, is_active=True)

    def get(self, request, pk):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data)

    def put(self, request, pk):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        material = self.get_object(pk)
        material.is_active = False
        material.save()
        return Response({'detail': 'E’lon o‘chirildi (faol emas)'}, status=status.HTTP_204_NO_CONTENT)


# Buyer part

class MaterialsMapView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_role = getattr(request.user, 'role', None)
        if user_role not in ['user', 'buyer']:
            return Response({'detail': 'Access denied. You are not authorized to view materials map.'},
                            status=status.HTTP_403_FORBIDDEN)

        materials = Material.objects.all()
        serializer = MaterialMapSerializer(materials, many=True)
        return Response(serializer.data)


class MaterialContactInfoView(APIView):
    permission_classes = [IsBuyer]

    def get(self, request, pk):
        user = request.user

        # Faqat buyerlar ko'rsin
        if user.role != 'buyer':
            return Response({'detail': 'Only buyers can access this information.'},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            material = Material.objects.get(pk=pk)
        except Material.DoesNotExist:
            return Response({'detail': 'Material not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = MaterialContactSerializer(material)
        return Response(serializer.data)



class FilterByMaterialTypeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Foydalanuvchi faqat 'buyer' bo‘lsa ruxsat beramiz
        if request.user.role != 'buyer':
            return Response({'detail': 'Only buyers can access this.'}, status=403)

        # So‘rovdan 'type' query parameterni olish
        material_type = request.query_params.get('type')
        if not material_type:
            return Response({'detail': 'Query parameter "type" is required.'}, status=400)

        # Filtrlash (to‘g‘ri field: type)
        materials = Material.objects.filter(type=material_type, is_active=True)
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)



def haversine(lat1, lon1, lat2, lon2):
    # Yer radiusi (km)
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    return R * c

class FilterByLocationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            lat = float(request.query_params.get('lat'))
            lon = float(request.query_params.get('lon'))
            radius = float(request.query_params.get('radius', 5))  # default 5 km
        except (TypeError, ValueError):
            return Response({"detail": "Invalid or missing lat/lon/radius"}, status=400)

        all_materials = Material.objects.filter(is_active=True)
        nearby_materials = []

        for material in all_materials:
            if material.latitude and material.longitude:
                distance = haversine(lat, lon, material.latitude, material.longitude)
                if distance <= radius:
                    nearby_materials.append(material)

        serializer = MaterialSerializer(nearby_materials, many=True)
        return Response(serializer.data)



class FilterByQuantityAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Faqat buyerlarga ruxsat
        if request.user.role != 'buyer':
            return Response({'detail': 'Only buyers can access this.'}, status=403)

        # Query parametrlardan min/max miqdorni olish
        min_quantity = request.query_params.get('min_quantity')
        max_quantity = request.query_params.get('max_quantity')

        # Asosiy filter
        materials = Material.objects.filter(is_active=True)

        # Agar miqdorlar ko‘rsatilgan bo‘lsa, filtrlash
        if min_quantity is not None:
            try:
                min_quantity = int(min_quantity)
                materials = materials.filter(quantity__gte=min_quantity)
            except ValueError:
                return Response({'detail': 'min_quantity must be an integer'}, status=400)

        if max_quantity is not None:
            try:
                max_quantity = int(max_quantity)
                materials = materials.filter(quantity__lte=max_quantity)
            except ValueError:
                return Response({'detail': 'max_quantity must be an integer'}, status=400)

        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data)