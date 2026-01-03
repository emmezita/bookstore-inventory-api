from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de libros.
    
    Endpoints:
    - GET /books/ - Listar todos los libros (paginado)
    - POST /books/ - Crear un nuevo libro
    - GET /books/{id}/ - Obtener un libro por ID
    - PUT /books/{id}/ - Actualizar un libro
    - DELETE /books/{id}/ - Eliminar un libro
    - GET /books/search/?category={category} - Buscar por categoría
    - GET /books/low-stock/?threshold={n} - Libros con stock bajo
    """
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'author', 'category', 'isbn']
    ordering_fields = ['title', 'cost_usd', 'stock_quantity', 'created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'], url_path='search')
    def search_by_category(self, request):
        """
        GET /books/search/?category={category}
        Buscar libros por categoría.
        """
        category = request.query_params.get('category', None)
        
        if not category:
            return Response(
                {"error": "El parámetro 'category' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = self.queryset.filter(category__icontains=category)
        page = self.paginate_queryset(books)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        """
        GET /books/low-stock/?threshold={n}
        Obtener libros con stock bajo.
        """
        try:
            threshold = int(request.query_params.get('threshold', 10))
        except ValueError:
            return Response(
                {"error": "El parámetro 'threshold' debe ser un número entero."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        books = self.queryset.filter(stock_quantity__lte=threshold)
        page = self.paginate_queryset(books)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)