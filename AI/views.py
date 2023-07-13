from django.shortcuts import redirect
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DetectionCreationSerializer, DetectionValidationSerializer, DetectionStatusSerializer
from .models import Detection
from .apps import prediction_models_manager
from .utils import predict

class DiseaseDetectionCreationView(APIView):
    

    def post(self, request, format=None):

        user = request.user
        serializer = DetectionCreationSerializer(data=request.data,
                                                 context={'user': user})
        if serializer.is_valid(raise_exception=True):
            detection = serializer.save()
            models = prediction_models_manager.prediction_models

            if settings.DETECTION_IN_BACKGROUND:
                #Add detection thread to queue/anyother
                return Response(detection.uuid, status=status.HTTP_200_OK)
            else:
                predict(models, detection)
                return redirect(f'/detection/info?uuid={detection.uuid}')

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetectionInformation(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        serializer = DetectionValidationSerializer(data=request.GET,
                                               context={'user': user})
        
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        detection = Detection.objects.get(uuid=serializer.data.get('uuid'))
        serializer = DetectionStatusSerializer(detection)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ListDetectionsForUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        profile = request.user.profile
        skip = int(request.GET.get('skip')) if request.GET.get('skip') else 0
        amount = int(request.GET.get('amount')) if request.GET.get('amount') else settings.DETECTIONS_PER_PAGE

        detections = Detection.objects.filter(profile=profile).order_by('start_time')[skip:skip+amount]
        serializer = DetectionStatusSerializer(detections, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ListDetectionModels(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        models = prediction_models_manager.prediction_models.keys()
        return Response({"models":models}, status=status.HTTP_200_OK)