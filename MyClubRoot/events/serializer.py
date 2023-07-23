class Serializer(serializers.Serializer):
    title = serializers.TextField('title')
    
    def create(self, validated_data)
        return Event(**validated_data)
