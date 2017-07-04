from django.db import models

class Game(models.Model):
    HEARTHSTONE = 1
    WOW = 2
    HOTS = 3
    BOOK_TYPES = (
        (HEARTHSTONE, 'Hearthstone'),
        (WOW, 'WOW'),
        (HOTS, 'HOTS'),
    )
    
    title = models.CharField(max_length=50)
    publication_date = models.DateField(null=True)
    author = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pages = models.IntegerField(blank=True, null=True)
    book_type = models.PositiveSmallIntegerField(choices=BOOK_TYPES)