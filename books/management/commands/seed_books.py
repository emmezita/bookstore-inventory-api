from django.core.management.base import BaseCommand
from books.models import Book
from decimal import Decimal


class Command(BaseCommand):
    help = 'Poblar la base de datos con 10 libros de ejemplo'

    def handle(self, *args, **options):
        books_data = [
            {
                'title': 'El Quijote',
                'author': 'Miguel de Cervantes',
                'isbn': '978-84-376-0494-7',
                'cost_usd': Decimal('15.99'),
                'stock_quantity': 25,
                'category': 'Literatura Clásica',
                'supplier_country': 'ES',
            },
            {
                'title': 'Cien años de soledad',
                'author': 'Gabriel García Márquez',
                'isbn': '978-0-06-088328-7',
                'cost_usd': Decimal('12.50'),
                'stock_quantity': 18,
                'category': 'Realismo Mágico',
                'supplier_country': 'CO',
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '978-0-452-28423-4',
                'cost_usd': Decimal('9.99'),
                'stock_quantity': 30,
                'category': 'Ciencia Ficción',
                'supplier_country': 'GB',
            },
            {
                'title': 'El Principito',
                'author': 'Antoine de Saint-Exupéry',
                'isbn': '978-0-15-601219-5',
                'cost_usd': Decimal('8.50'),
                'stock_quantity': 45,
                'category': 'Literatura Infantil',
                'supplier_country': 'FR',
            },
            {
                'title': 'Rayuela',
                'author': 'Julio Cortázar',
                'isbn': '978-84-376-0302-5',
                'cost_usd': Decimal('14.25'),
                'stock_quantity': 12,
                'category': 'Literatura Latinoamericana',
                'supplier_country': 'AR',
            },
            {
                'title': 'Pedro Páramo',
                'author': 'Juan Rulfo',
                'isbn': '978-84-376-0110-6',
                'cost_usd': Decimal('11.00'),
                'stock_quantity': 8,
                'category': 'Realismo Mágico',
                'supplier_country': 'MX',
            },
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '978-0-7432-7356-5',
                'cost_usd': Decimal('10.99'),
                'stock_quantity': 22,
                'category': 'Literatura Clásica',
                'supplier_country': 'US',
            },
            {
                'title': 'Dom Casmurro',
                'author': 'Machado de Assis',
                'isbn': '978-85-359-0277-2',
                'cost_usd': Decimal('13.75'),
                'stock_quantity': 5,
                'category': 'Literatura Brasileña',
                'supplier_country': 'BR',
            },
            {
                'title': 'La casa de los espíritus',
                'author': 'Isabel Allende',
                'isbn': '978-84-01-24235-4',
                'cost_usd': Decimal('16.50'),
                'stock_quantity': 15,
                'category': 'Realismo Mágico',
                'supplier_country': 'CL',
            },
            {
                'title': 'Conversación en La Catedral',
                'author': 'Mario Vargas Llosa',
                'isbn': '978-84-204-8393-1',
                'cost_usd': Decimal('18.99'),
                'stock_quantity': 3,
                'category': 'Literatura Latinoamericana',
                'supplier_country': 'PE',
            },
        ]

        created_count = 0
        skipped_count = 0

        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults=book_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {book.title}')
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Ya existe: {book.title}')
                )

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                f'Completado: {created_count} libros creados, {skipped_count} omitidos'
            )
        )
