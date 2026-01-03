from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Book con validaciones."""
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'cost_usd',
            'selling_price_local', 'stock_quantity', 'category',
            'supplier_country', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_cost_usd(self, value):
        """Valida que el costo sea mayor a 0."""
        if value <= 0:
            raise serializers.ValidationError("El costo debe ser mayor a 0.")
        return value
    
    def validate_isbn(self, value):
        """Valida unicidad del ISBN en creación/actualización."""
        # Obtener la instancia actual si existe (para updates)
        instance = getattr(self, 'instance', None)
        
        # Verificar si ya existe otro libro con el mismo ISBN
        queryset = Book.objects.filter(isbn=value)
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        
        if queryset.exists():
            raise serializers.ValidationError("Ya existe un libro con este ISBN.")
        return value