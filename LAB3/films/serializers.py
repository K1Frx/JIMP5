from rest_framework import serializers
from .models import Movie, Category

class MovieGetRequestSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128, required=False)
    director = serializers.CharField(max_length=64, required=False)
    category = serializers.CharField(max_length=64, required=False)
    year = serializers.IntegerField(required=False)
    page = serializers.IntegerField(required=False)
    per_page = serializers.IntegerField(required=False)
    
class MovieGetResponseSerializer(serializers.Serializer):
    class __MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = '__all__'
            
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    num_pages = serializers.IntegerField()
    total = serializers.IntegerField()
    offset = serializers.IntegerField()
    items = __MovieSerializer(many=True)

class MoviePostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class MoviePostResponseSerializer(MovieGetResponseSerializer):
    pass

class MoviePatchRequestSerializer(MoviePostRequestSerializer):
    pass

class MoviePatchResponseSerializer(MoviePatchRequestSerializer):
    pass

class CategoryGetRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64, required=False)
    page = serializers.IntegerField(required=False)
    per_page = serializers.IntegerField(required=False)
    
class CategoryGetResponseSerializer(serializers.Serializer):
    class __CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = '__all__'
    
    page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    num_pages = serializers.IntegerField()
    total = serializers.IntegerField()
    offset = serializers.IntegerField()
    items = __CategorySerializer(many=True)
    

class CategoryPostRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryPostResponseSerializer(CategoryGetResponseSerializer):
    pass

class CategoryPatchRequestSerializer(CategoryPostRequestSerializer):
    pass

class CategoryPatchResponseSerializer(CategoryGetResponseSerializer):
    pass

class TopMoviesGetResponseSerializer(MovieGetResponseSerializer):
    pass
