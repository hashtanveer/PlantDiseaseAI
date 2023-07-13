from rest_framework import serializers
from .models import Detection, Plant, Profile

class DetectionCreationSerializer(serializers.ModelSerializer):
    plant_type = serializers.CharField(max_length=255)
    img_path = serializers.ImageField()

    class Meta:
        model = Detection
        fields = ['plant_type', 'img_path']
    
    def create(self, validated_data):
        user = self.context.get('user')

        #try:
        #    profile = user.profile
        #except:
        #    raise serializers.ValidationError("Anonymous User")
        profile = user.profile
        
        plant_type_name = validated_data.pop('plant_type')
        try:
            plant = Plant.objects.get(name=plant_type_name)
        except Plant.DoesNotExist:
            raise serializers.ValidationError("Invalid plant_type")
        
        validated_data['profile'] = profile
        validated_data['plant_type'] = plant
        detection = Detection.objects.create(**validated_data)
        return detection

class DetectionValidationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()

    class Meta:
        model = Detection
        fields = ['uuid']

    def validate(self, attrs):
        uuid = attrs.get('uuid')
        if not Detection.objects.filter(uuid=uuid).exists():
            raise serializers.ValidationError("UUID not found")
        
        user = self.context.get('user')
        try:
            profile = user.profile
        except:
            raise serializers.ValidationError("Anonymous User")
        
        if not Detection.objects.filter(uuid=uuid, profile=profile).exists():
            raise serializers.ValidationError("You are not authorized for this UUID")
        
        return attrs

class DetectionStatusSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    plant = serializers.CharField(source='plant_type.name')

    class Meta:
        model = Detection
        exclude = ['img_path', 'profile','plant_type']