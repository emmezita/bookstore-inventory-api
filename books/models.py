import re
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


def validate_isbn(value):
    """Valida que el ISBN tenga formato válido (10 o 13 dígitos)."""
    # Remover guiones y espacios
    clean_isbn = re.sub(r'[-\s]', '', value)
    
    if len(clean_isbn) not in (10, 13):
        raise ValidationError(
            'ISBN debe tener 10 o 13 dígitos (sin contar guiones).'
        )
    
    if not clean_isbn.replace('X', '0').isdigit():
        raise ValidationError('ISBN contiene caracteres inválidos.')


class Book(models.Model):
    """Modelo para representar un libro en el inventario."""
    
    title = models.CharField(max_length=255, verbose_name='Título')
    author = models.CharField(max_length=255, verbose_name='Autor')
    isbn = models.CharField(
        max_length=17,  # ISBN-13 con guiones: xxx-xx-xxx-xxxx-x
        unique=True,
        validators=[validate_isbn],
        verbose_name='ISBN'
    )
    cost_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='El costo debe ser mayor a 0.')],
        verbose_name='Costo USD'
    )
    selling_price_local = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Precio de venta local'
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='Cantidad en stock'
    )
    category = models.CharField(max_length=100, verbose_name='Categoría')
    supplier_country = models.CharField(
        max_length=2,
        verbose_name='País del proveedor',
        help_text='Código ISO de 2 letras (ej: ES, US, MX)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return f"{self.title} - {self.author}"