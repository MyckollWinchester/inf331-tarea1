import unittest
import json
from api import app
from src.database import Database

class InventoryAPITestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # BD en memoria
        cls.client = app.test_client()

        with app.app_context():
            cls.db = Database()
            cls.db.create_if_not_exists()
    
    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            cls.db.close_connection()
            cls.db.drop_all_tables()
    
    # Crear productos con datos válidos
    def test_create_item_success(self):
        response = self.client.post('/api/products/', json={
            'nombre': 'Laptop Dell XPS 13',
            'descripcion': 'Ultrabook con pantalla táctil',
            'cantidad': 10,
            'precio': 699_900,
            'categoria': 'Electrónica'
        })
        self.assertEqual(response.status_code, 201)

    # Crear productos con datos faltantes
    def test_create_item_missing_fields(self):
        response = self.client.post('/api/products/', json={
            'descripcion': 'Ultrabook con pantalla táctil',
            'cantidad': 10,
            'precio': 699_900,
            'categoria': 'Electrónica'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('missing fields', str(response.data))

    # Crear productos con datos inválidos (fuera de rango)
    def test_create_item_invalid_data(self):
        response = self.client.post('/api/products/', json={
            'nombre': '',
            'descripcion': 'a nice description',
            'cantidad': 20,
            'precio': -100,
            'categoria': 'a great category'
        })
        self.assertEqual(response.status_code, 400)
    
    # Crear productos con el mismo nombre (unicidad)
    def test_create_item_already_exists(self):
        self.client.post('/api/products/', json={
            'nombre': 'producto#3',
            'descripcion': 'a nice description',
            'cantidad': 10,
            'precio': 100,
            'categoria': 'a great category'
        })
        response = self.client.post('/api/products/', json={
            'nombre': 'producto#3',
            'descripcion': 'a nice description',
            'cantidad': 10,
            'precio': 100,
            'categoria': 'a great category'
        })
        self.assertEqual(response.status_code, 403)
        self.assertIn('product already exists', str(response.data))

    # Obtener todos los productos
    def test_get_all_items(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Laptop Dell XPS 13', str(response.data))
        # producto#2 no existe porque no se creó correctamente en el test anterior
        self.assertIn('producto#3', str(response.data))
