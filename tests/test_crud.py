import unittest
from gestor_inversiones.crud import registrar_compra, consultar_registros, borrar_transaccion

class TestCrud(unittest.TestCase):
    def test_registro_consulta(self):
        # Prueba de registro
        registrar_compra("BTC", "CRYPTO", 0.1, 35000, 3500, 1000)
        df = consultar_registros()
        self.assertGreater(len(df), 0)
        
        # Prueba de borrado
        ultimo_id = df.iloc[-1]['id']
        self.assertTrue(borrar_transaccion(ultimo_id))

if __name__ == '__main__':
    unittest.main()
