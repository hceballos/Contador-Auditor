#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import sqlite3
import re

class InputCCostos():

    TABLE_NAME = 'MovimientosTabla'

    TABLE_COLUMN_CUENTA = "CUENTA"
    TABLE_COLUMN_FECHA = "FECHA"
    TABLE_COLUMN_N_COMPROBANTE = "N_COMPROBANTE"
    TABLE_COLUMN_TIPO = "TIPO"
    TABLE_COLUMN_N_INTERNO = "N_INTERNO"
    TABLE_COLUMN_PRESUP_DE_CAJA = "PRESUP_DE_CAJA"
    TABLE_COLUMN_CENTRO_DE_COSTO = "CENTRO_DE_COSTO"
    TABLE_COLUMN_AUXILIAR = "AUXILIAR"
    TABLE_COLUMN_TIPO_DOC = "TIPO_DOC"
    TABLE_COLUMN_NUMERO_DOC = "NUMERO_DOC"
    TABLE_COLUMN_DETDE_GASTO_INSTFINANCIERO = "DETDE_GASTO_INSTFINANCIERO"
    TABLE_COLUMN_DEBE = "DEBE"
    TABLE_COLUMN_HABER = "HABER"
    TABLE_COLUMN_SALDO = "SALDO"
    TABLE_COLUMN_DESCRIPCION = "DESCRIPCION"

    def __init__(self, dataBaseFileName):
        self.dataBaseFileName = dataBaseFileName
        print "Base de Datos - Asignacion de nombre de base de datos FILE_DB = 'data.db'"

        self.conection = sqlite3.connect(self.dataBaseFileName)
        self.conection.text_factory = str

        self.cursor = self.conection.cursor()
        print "Base de Datos - conector con base de datos"

        self.cursor.execute(
            'DROP TABLE IF EXISTS {}'.format(
                self.TABLE_NAME
            )
        )

        self.cursor.execute(
            'CREATE TABLE {} ({} TEXT, {} TEXT, {} INTEGER, {} TEXT, {} INTEGER, {} INTEGER NULL, {} TEXT, {} TEXT, {} TEXT, {} INTEGER, {} INTEGER NULL, {} INTEGER, {} INTEGER, {} INTEGER, {} TEXT)'
                .format(
                    self.TABLE_NAME,
                    self.TABLE_COLUMN_CUENTA,
                    self.TABLE_COLUMN_FECHA,
                    self.TABLE_COLUMN_N_COMPROBANTE,
                    self.TABLE_COLUMN_TIPO,
                    self.TABLE_COLUMN_N_INTERNO,
                    self.TABLE_COLUMN_PRESUP_DE_CAJA,
                    self.TABLE_COLUMN_CENTRO_DE_COSTO,
                    self.TABLE_COLUMN_AUXILIAR,
                    self.TABLE_COLUMN_TIPO_DOC,
                    self.TABLE_COLUMN_NUMERO_DOC,
                    self.TABLE_COLUMN_DETDE_GASTO_INSTFINANCIERO,
                    self.TABLE_COLUMN_DEBE,
                    self.TABLE_COLUMN_HABER,
                    self.TABLE_COLUMN_SALDO,
                    self.TABLE_COLUMN_DESCRIPCION
            )
        )


        self.conection.commit()
        print "Base de Datos - Asignacion de columnas"
        self.saveRegisters()

    def saveRegisters(self):
        registers = []                                    
        print "Base de Datos - Lectura de Libro mayor y almacenando en registers"
        with codecs.open("2013_copia.csv", "r",encoding='utf-8', errors='ignore') as infile:
            for line in infile:
                line = line.strip()                         
                line = line.replace('"', '')   
                data = line.split(";")                  
                registers.append(data)


        for register in registers[11:]:

            if self._isRowUseful(register):
                #strip out spaces
                register = self._stripColumns(register)
                #normalize date
                register[1] = self._normalizeDate(register[1])

                register[0] = self._normalizeSlash(register[0])
                register[0] = self._normalizeGuionBajo(register[0])

                self.conection.execute(
                    'INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'.format(
                        self.TABLE_NAME
                    ),
                    register
                )

        self.conection.commit()
        print "Base de Datos - salvar los datos de 'registers' en base de datos"


    def _isRowUseful(self, row):
        firstColumn = row[0]

        emptyRegexp = re.compile('^\s*$|^SALDO')
        if emptyRegexp.match(firstColumn):
            return False

        return True

    def _stripColumns(self, row):
        return [column.strip() for column in row]

    def _normalizeDate(self, dateString):
        return re.sub('(\d{2}).(\d{2}).(\d{2})?(\d{2})', '20\g<4>-\g<2>-\g<1>', dateString)

    def _normalizeSlash(self, dateSLash):
        return re.sub("/", "-", dateSLash)

    def _normalizeGuionBajo(self, dateSLash):
        return re.sub("_", "", dateSLash)


if __name__ == '__main__':

    FILE_DB = 'data.db'

    InputCCostos = InputCCostos(FILE_DB)


