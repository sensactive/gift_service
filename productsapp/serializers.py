from rest_framework import serializers

from productsapp.models import Products


class ProductSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    pics = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'type', 'category', 'description', 'brand', 'pics', 'price', 'name', 'links']
        read_only_fields = ("id",)


    def get_type(self, obj):
        return obj.type.title

    def get_brand(self, obj):
        return obj.brand.title

    def get_category(self, obj):
        return obj.category.title

    def get_pics(self, obj):
        return list(obj.pics.all().values('id', 'url'))

    def get_links(self, obj):
        return list(obj.links.all().values('id', 'url'))



