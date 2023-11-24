from rest_framework import serializers, viewsets

class AutoApiSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = "__all__"

class AutoApiViewset(viewsets.ModelViewSet):
    serializer_class = AutoApiSerializer
    queryset = None

