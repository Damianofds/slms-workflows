# -*- coding: utf-8 -*-

"""
***************************************************************************
    ogr2ogrtopostgislist_slms.py
    ---------------------
    Date                 : November 2012
    Copyright            : (C) 2012 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'November 2012'
__copyright__ = '(C) 2012, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'


from PyQt4.QtCore import QSettings

from processing.core.parameters import ParameterVector
from processing.core.parameters import ParameterString
from processing.core.parameters import ParameterCrs
from processing.core.parameters import ParameterSelection
from processing.core.parameters import ParameterBoolean
from processing.core.parameters import ParameterExtent
from processing.core.parameters import ParameterTableField

from processing.algs.gdal.GdalAlgorithm import GdalAlgorithm
from processing.algs.gdal.GdalUtils import GdalUtils

from processing.tools.system import isWindows
from processing.tools.vector import ogrConnectionString, ogrLayerName


class Ogr2OgrToPostGisListSLMS(GdalAlgorithm):

    DATABASE = 'DATABASE'
    INPUT_LAYER = 'INPUT_LAYER'
    GTYPE = 'GTYPE'
    GEOMTYPE = ['', 'NONE', 'GEOMETRY', 'POINT', 'LINESTRING', 'POLYGON', 'GEOMETRYCOLLECTION', 'MULTIPOINT', 'MULTIPOLYGON', 'MULTILINESTRING']
    S_SRS = 'S_SRS'
    T_SRS = 'T_SRS'
    A_SRS = 'A_SRS'
    HOST = 'HOST'
    PORT = 'PORT'
    USER = 'USER'
    DBNAME = 'DBNAME'
    PASSWORD = 'PASSWORD'
    SCHEMA = 'SCHEMA'
    TABLE = 'TABLE'
    PK = 'PK'
    PRIMARY_KEY = 'PRIMARY_KEY'
    GEOCOLUMN = 'GEOCOLUMN'
    DIM = 'DIM'
    DIMLIST = ['2', '3']
    SIMPLIFY = 'SIMPLIFY'
    SEGMENTIZE = 'SEGMENTIZE'
    SPAT = 'SPAT'
    CLIP = 'CLIP'
    WHERE = 'WHERE'
    GT = 'GT'
    OVERWRITE = 'OVERWRITE'
    APPEND = 'APPEND'
    ADDFIELDS = 'ADDFIELDS'
    LAUNDER = 'LAUNDER'
    INDEX = 'INDEX'
    SKIPFAILURES = 'SKIPFAILURES'
    PRECISION = 'PRECISION'
    PROMOTETOMULTI = 'PROMOTETOMULTI'
    OPTIONS = 'OPTIONS'

    def commandLineName(self):
        return "gdalogr:slms-shp2PostGIS-overwrite"

    def dbConnectionNames(self):
        settings = QSettings()
        settings.beginGroup('/PostgreSQL/connections/')
        return settings.childGroups()

    def defineCharacteristics(self):
        self.name, self.i18n_name = self.trAlgorithm('SLMS - Import Static Vector into PostGIS (OVERWRITE MODE)')
        self.group, self.i18n_group = self.trAlgorithm('[OGR] Miscellaneous')
        self.DB_CONNECTIONS = self.dbConnectionNames()
        self.addParameter(ParameterSelection(self.DATABASE,
                                             self.tr('Database (connection name)'), self.DB_CONNECTIONS))
        self.addParameter(ParameterVector(self.INPUT_LAYER,
                                          self.tr('Input layer'), [ParameterVector.VECTOR_TYPE_ANY], False))
        #self.addParameter(ParameterSelection(self.GTYPE,
        #                                     self.tr('Output geometry type'), self.GEOMTYPE, 0))
        #self.addParameter(ParameterCrs(self.A_SRS,
        #                               self.tr('Assign an output CRS'), '', optional=True))
        self.addParameter(ParameterCrs(self.T_SRS,
                                       self.tr('Reproject to this CRS on output '), '', optional=True))
        #self.addParameter(ParameterCrs(self.S_SRS,
        #                               self.tr('Override source CRS'), '', optional=True))
        self.addParameter(ParameterString(self.SCHEMA,
                                          self.tr('Schema name'), 'stg_geoserver'))
        self.addParameter(ParameterString(self.TABLE,
                                          self.tr('The output PostGIS table name'), False))
        self.addParameter(ParameterString(self.PK,
                                          self.tr('Primary key (new field)'), 'id', optional=True))
        self.addParameter(ParameterTableField(self.PRIMARY_KEY,
                                              self.tr('Primary key (existing field, used if the above option is left empty)'), self.INPUT_LAYER, optional=True))
        self.addParameter(ParameterString(self.GEOCOLUMN,
                                          self.tr('Geometry column name'), 'the_geom', optional=True))
        #self.addParameter(ParameterSelection(self.DIM,
        #                                     self.tr('Vector dimensions'), self.DIMLIST, 0))
        #self.addParameter(ParameterString(self.SIMPLIFY,
        #                                  self.tr('Distance tolerance for simplification'),
        #                                  '', optional=True))
        #self.addParameter(ParameterString(self.SEGMENTIZE,
        #                                  self.tr('Maximum distance between 2 nodes (densification)'),
        #                                  '', optional=True))
        #self.addParameter(ParameterExtent(self.SPAT,
        #                                  self.tr('Select features by extent (defined in input layer CRS)')))
        #self.addParameter(ParameterBoolean(self.CLIP,
        #                                   self.tr('Clip the input layer using the above (rectangle) extent'),
        #                                   False))
        #self.addParameter(ParameterString(self.WHERE,
        #                                  self.tr('Select features using a SQL "WHERE" statement (Ex: column=\'value\')'),
        #                                  '', optional=True))
        #self.addParameter(ParameterString(self.GT,
        #                                  self.tr('Group N features per transaction (Default: 20000)'),
        #                                  '', optional=True))
        #self.addParameter(ParameterBoolean(self.OVERWRITE,
        #                                   self.tr('Overwrite existing table'), True))
        #self.addParameter(ParameterBoolean(self.APPEND,
        #                                   self.tr('Append to existing table'), False))
        #self.addParameter(ParameterBoolean(self.ADDFIELDS,
        #                                   self.tr('Append and add new fields to existing table'), False))
        #self.addParameter(ParameterBoolean(self.LAUNDER,
        #                                   self.tr('Do not launder columns/table names'), False))
        #self.addParameter(ParameterBoolean(self.INDEX,
        #                                   self.tr('Do not create spatial index'), False))
        self.addParameter(ParameterBoolean(self.SKIPFAILURES,
                                           self.tr('Continue after a failure, skipping the failed feature'),
                                           False))
        #self.addParameter(ParameterBoolean(self.PROMOTETOMULTI,
        #                                   self.tr('Promote to Multipart'),
        #                                   True))
        #self.addParameter(ParameterBoolean(self.PRECISION,
        #                                   self.tr('Keep width and precision of input attributes'),
        #                                   True))
        #self.addParameter(ParameterString(self.OPTIONS,
        #                                  self.tr('Additional creation options'), '', optional=True))

    def getConsoleCommands(self):
        connection = self.DB_CONNECTIONS[self.getParameterValue(self.DATABASE)]
        settings = QSettings()
        mySettings = '/PostgreSQL/connections/' + connection
        dbname = settings.value(mySettings + '/database')
        user = settings.value(mySettings + '/username')
        host = settings.value(mySettings + '/host')
        port = settings.value(mySettings + '/port')
        password = settings.value(mySettings + '/password')
        inLayer = self.getParameterValue(self.INPUT_LAYER)
        ogrLayer = ogrConnectionString(inLayer)[1:-1]
        #ssrs = unicode(self.getParameterValue(self.S_SRS))
        tsrs = unicode(self.getParameterValue(self.T_SRS))
        #asrs = unicode(self.getParameterValue(self.A_SRS))
        schema = unicode(self.getParameterValue(self.SCHEMA))
        table = unicode(self.getParameterValue(self.TABLE))
        pk = unicode(self.getParameterValue(self.PK))
        pkstring = "-lco FID=" + pk
        primary_key = self.getParameterValue(self.PRIMARY_KEY)
        geocolumn = unicode(self.getParameterValue(self.GEOCOLUMN))
        geocolumnstring = "-lco GEOMETRY_NAME=" + geocolumn
        dim = "2" #self.DIMLIST[self.getParameterValue(self.DIM)]
        dimstring = "-lco DIM=" + dim
        simplify = "" #unicode(self.getParameterValue(self.SIMPLIFY))
        segmentize = "" #unicode(self.getParameterValue(self.SEGMENTIZE))
        spat = "" #self.getParameterValue(self.SPAT)
        clip = False #self.getParameterValue(self.CLIP)
        where = False #unicode(self.getParameterValue(self.WHERE))
        #wherestring = '-where "' + where + '"'
        #gt = unicode(self.getParameterValue(self.GT))
        overwrite = True #self.getParameterValue(self.OVERWRITE)
        append = False #self.getParameterValue(self.APPEND)
        addfields = False #self.getParameterValue(self.ADDFIELDS)
        launder = False #self.getParameterValue(self.LAUNDER)
        launderstring = "-lco LAUNDER=NO"
        index = False #self.getParameterValue(self.INDEX)
        indexstring = "-lco SPATIAL_INDEX=OFF"
        skipfailures = self.getParameterValue(self.SKIPFAILURES)
        promotetomulti = True #self.getParameterValue(self.PROMOTETOMULTI)
        precision = True #self.getParameterValue(self.PRECISION)
        #options = unicode(self.getParameterValue(self.OPTIONS))

        arguments = []
        arguments.append('-progress')
        arguments.append('--config PG_USE_COPY YES')
        arguments.append('-f')
        arguments.append('PostgreSQL')
        arguments.append('PG:"host=' + host)
        arguments.append('port=' + port)
        if len(dbname) > 0:
            arguments.append('dbname=' + dbname)
        if len(password) > 0:
            arguments.append('password=' + password)
        if len(schema) > 0:
            arguments.append('active_schema=' + schema)
        else:
            arguments.append('active_schema=public')
        arguments.append('user=' + user + '"')
        arguments.append(dimstring)
        arguments.append(ogrLayer)
        arguments.append(ogrLayerName(inLayer))
        if index:
            arguments.append(indexstring)
        if launder:
            arguments.append(launderstring)
        if append:
            arguments.append('-append')
        if addfields:
            arguments.append('-addfields')
        if overwrite:
            arguments.append('-overwrite')
        #if len(self.GEOMTYPE[self.getParameterValue(self.GTYPE)]) > 0:
        #    arguments.append('-nlt')
        #    arguments.append(self.GEOMTYPE[self.getParameterValue(self.GTYPE)])
        if len(geocolumn) > 0:
            arguments.append(geocolumnstring)
        if len(pk) > 0:
            arguments.append(pkstring)
        elif primary_key is not None:
            arguments.append("-lco FID=" + primary_key)
        if len(table) > 0:
            arguments.append('-nln')
            arguments.append(table)
        #if len(ssrs) > 0:
        #    arguments.append('-s_srs')
        #    arguments.append(ssrs)
        if len(tsrs) > 0:
            arguments.append('-t_srs')
            arguments.append(tsrs)
        #if len(asrs) > 0:
        #    arguments.append('-a_srs')
        #    arguments.append(asrs)
        if len(spat) > 0:
            regionCoords = spat.split(',')
            arguments.append('-spat')
            arguments.append(regionCoords[0])
            arguments.append(regionCoords[2])
            arguments.append(regionCoords[1])
            arguments.append(regionCoords[3])
            if clip:
                arguments.append('-clipsrc spat_extent')
        if skipfailures:
            arguments.append('-skipfailures')
        if where:
            arguments.append(wherestring)
        if len(simplify) > 0:
            arguments.append('-simplify')
            arguments.append(simplify)
        if len(segmentize) > 0:
            arguments.append('-segmentize')
            arguments.append(segmentize)
        #if len(gt) > 0:
        #    arguments.append('-gt')
        #    arguments.append(gt)
        if promotetomulti:
            arguments.append('-nlt PROMOTE_TO_MULTI')
        if precision is False:
            arguments.append('-lco PRECISION=NO')
        #if len(options) > 0:
        #    arguments.append(options)

        commands = []
        if isWindows():
            commands = ['cmd.exe', '/C ', 'ogr2ogr.exe',
                        GdalUtils.escapeAndJoin(arguments)]
        else:
            commands = ['ogr2ogr', GdalUtils.escapeAndJoin(arguments)]

        return commands

    def commandName(self):
        return "ogr2ogr"
