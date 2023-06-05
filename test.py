from datetime import datetime
import unittest
from Reports import ReportsManager

class pruebas(unittest.TestCase):

    def test_fechaValida(self):
        rep=ReportsManager()
        date=datetime.strptime("04/06/2023 5:20:34","%d/%m/%Y %H:%M:%S")
        self.assertEqual(rep.fechaValida(date,1),True)

if __name__=="__main__":
    unittest.main()