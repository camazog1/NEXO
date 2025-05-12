from django.test import TestCase, Client
from django.urls import reverse
from .models import Product

# Create your tests here.

class ProductModelTest(TestCase):
    """Test para el modelo Product."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear un producto de prueba
        self.product = Product.objects.create(
            title='Producto de prueba',
            reference='TEST001',
            description='Descripción de prueba',
            price=1000,
            price_dolar=10.50,
            is_popular=True,
            is_new=True,
            discontinued=False
        )
    
    def test_product_creation(self):
        """Test para verificar que un producto se crea correctamente."""
        self.assertEqual(self.product.title, 'Producto de prueba')
        self.assertEqual(self.product.reference, 'TEST001')
        self.assertEqual(self.product.price, 1000)
        self.assertTrue(self.product.is_popular)
        self.assertTrue(self.product.is_new)
        self.assertFalse(self.product.discontinued)
        
class ProductViewTest(TestCase):
    """Test para las vistas de Product."""
    
    def setUp(self):
        """Configuración inicial para las pruebas."""
        # Crear productos de prueba
        self.product1 = Product.objects.create(
            title='Producto 1',
            reference='REF001',
            description='Descripción 1',
            price=1000,
            price_dolar=10.50,
            is_popular=True,
            is_new=True,
            discontinued=False
        )
        
        self.product2 = Product.objects.create(
            title='Producto 2',
            reference='REF002',
            description='Descripción 2',
            price=2000,
            price_dolar=20.50,
            is_popular=False,
            is_new=False,
            discontinued=False
        )
        
        # Cliente para hacer peticiones
        self.client = Client()
        
    def test_product_index_view(self):
        """Test para verificar que la vista product_index funciona correctamente."""
        # Hacer una petición GET a la vista
        response = self.client.get(reverse('product_index'))
        
        # Verificar que la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)
        
        # Verificar que los productos están en el contexto
        self.assertTrue('products' in response.context)
        
        # Verificar que se muestran los dos productos
        products = response.context['products']
        self.assertEqual(products.count(), 2)
        
        # Verificar la búsqueda
        response = self.client.get(reverse('product_index') + '?q=Producto 1')
        products = response.context['products']
        self.assertEqual(products.count(), 1)
        self.assertEqual(products[0].title, 'Producto 1')
