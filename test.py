from datetime import datetime
from datetime import timedelta
import unittest
from Reports import ReportsManager

class pruebas(unittest.TestCase):

    def test_fechaValida(self):
        rep=ReportsManager()
        #Probando dia antes
        testdate=datetime.strptime('2023-06-05 3:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        testdate=datetime.strptime('2023-06-05 12:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        testdate=datetime.strptime('2023-06-05 20:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        testdate=datetime.strptime('2023-06-06 01:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        testdate=datetime.strptime('2023-06-06 02:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        testdate=datetime.strptime('2023-06-06 02:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),False)
        testdate=datetime.strptime('2023-06-06 02:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),False)
        testdate=datetime.strptime('2023-06-06 02:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),False)
        testdate=datetime.strptime('2023-06-06 02:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,5),False)
        #probando 2 dias antes
        testdate=datetime.strptime('2023-06-04 3:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),True)
        testdate=datetime.strptime('2023-06-04 12:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),True)
        testdate=datetime.strptime('2023-06-04 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),True)
        testdate=datetime.strptime('2023-06-04 3:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),False)
        testdate=datetime.strptime('2023-06-04 12:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),False)
        testdate=datetime.strptime('2023-06-04 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,5),False)
        #3 dias antes
        testdate=datetime.strptime('2023-06-03 3:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),True)
        testdate=datetime.strptime('2023-06-03 12:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),True)
        testdate=datetime.strptime('2023-06-03 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),True)
        testdate=datetime.strptime('2023-06-03 3:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),False)
        testdate=datetime.strptime('2023-06-03 12:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),False)
        testdate=datetime.strptime('2023-06-03 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),False)
        #4 dias antes
        testdate=datetime.strptime('2023-06-02 3:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),True)
        testdate=datetime.strptime('2023-06-02 12:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),True)
        testdate=datetime.strptime('2023-06-02 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),True)
        testdate=datetime.strptime('2023-06-02 3:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),False)
        testdate=datetime.strptime('2023-06-02 12:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),False)
        testdate=datetime.strptime('2023-06-02 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),False)
        #Cambio de mes primer dia
        testdate=datetime.strptime('2023-05-01 2:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        #Cambio de mes 1 dia antes
        testdate=datetime.strptime('2023-04-30 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        #Cambio de mes 2 dia antes
        testdate=datetime.strptime('2023-04-29 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),True)
        #Cambio de mes 3 dia antes
        testdate=datetime.strptime('2023-04-28 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),True)
        #Cambio de mes 4 dia antes
        testdate=datetime.strptime('2023-04-27 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),True)
        #cambio de año primer dia
        testdate=datetime.strptime('2023-01-01 2:59:59','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        #cambio de año 1 dia antes
        testdate=datetime.strptime('2022-12-31 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,1),True)
        #cambio de año 2 dia antes
        testdate=datetime.strptime('2022-12-30 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,2),True)
        #cambio de año 3 dia antes
        testdate=datetime.strptime('2022-12-29 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,3),True)
        #cambio de año 4 dia antes
        testdate=datetime.strptime('2022-12-28 17:00:00','%Y-%m-%d %H:%M:%S')
        self.assertEqual(rep.fechaValida(testdate,4),True)

    def test_conceptosjerarquias(self):
        rep=ReportsManager()
        #buscando concepto jearquia
        print(rep.buscarconceptoJer(6,False,False))
        print(rep.buscarconceptoJer(6,True,False))
        print(rep.buscarconceptoJer("disc",False,True))
        print(rep.buscarconceptoJer(13,False,True))

    
        



if __name__=="__main__":
    unittest.main()