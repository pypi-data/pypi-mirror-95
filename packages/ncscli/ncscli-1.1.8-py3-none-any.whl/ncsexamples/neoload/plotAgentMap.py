#!/usr/bin/env python3
"""
plots loadtest results produced by runBatchJMeter
"""
# standard library modules
import argparse
import csv
import json
import logging
import math
import os
import sys
import warnings
# third-party modules
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def getColumn(inputList,column):
    return [inputList[i][column] for i in range(0,len(inputList))]


if __name__ == "__main__":
    # configure logger formatting
    logFmt = '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'
    logDateFmt = '%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter(fmt=logFmt, datefmt=logDateFmt )
    logging.basicConfig(format=logFmt, datefmt=logDateFmt)

    # treat numpy deprecations as errors
    warnings.filterwarnings('error', category=np.VisibleDeprecationWarning)

    ap = argparse.ArgumentParser( description=__doc__, fromfile_prefix_chars='@', formatter_class=argparse.ArgumentDefaultsHelpFormatter )
    ap.add_argument( '--dataDirPath', required=True, help='the path to to directory for input and output data' )
    args = ap.parse_args()

    logger.info( 'plotting data in directory %s', os.path.realpath(args.dataDirPath)  )

    outputDir = args.dataDirPath
    launchedJsonFilePath = outputDir + "/startedAgents.json"
    print("launchedJsonFilePath = %s" % launchedJsonFilePath)

    if not os.path.isfile( launchedJsonFilePath ):
        logger.error( 'file not found: %s', launchedJsonFilePath )
        sys.exit( 1 )

    launchedInstances = []
    with open( launchedJsonFilePath, 'r') as jsonInFile:
        try:
            launchedInstances = json.load(jsonInFile)  # an array
        except Exception as exc:
            sys.exit( 'could not load json (%s) %s' % (type(exc), exc) )

    print("number of launchedInstances = %d" % len(launchedInstances))

    mappedFrameNumLocation = []
    mappedFrameNumLocationUnitedStates = []
    mappedFrameNumLocationRussia = []
    mappedFrameNumLocationOther = []
    
    for j in range(0,len(launchedInstances)):
        mappedFrameNumLocation.append([j,
            launchedInstances[j]["device-location"]["latitude"],
            launchedInstances[j]["device-location"]["longitude"],
            launchedInstances[j]["device-location"]["display-name"],
            launchedInstances[j]["device-location"]["country"]
            ])
        if launchedInstances[j]["device-location"]["country"] =="United States":
            mappedFrameNumLocationUnitedStates.append([j,
                launchedInstances[j]["device-location"]["latitude"],
                launchedInstances[j]["device-location"]["longitude"],
                launchedInstances[j]["device-location"]["display-name"],
                launchedInstances[j]["device-location"]["country"]
                ])
        elif launchedInstances[j]["device-location"]["country"] == "Russia":
            mappedFrameNumLocationRussia.append([j,
                launchedInstances[j]["device-location"]["latitude"],
                launchedInstances[j]["device-location"]["longitude"],
                launchedInstances[j]["device-location"]["display-name"],
                launchedInstances[j]["device-location"]["country"]
                ])
        else:
            mappedFrameNumLocationOther.append([j,
                launchedInstances[j]["device-location"]["latitude"],
                launchedInstances[j]["device-location"]["longitude"],
                launchedInstances[j]["device-location"]["display-name"],
                launchedInstances[j]["device-location"]["country"]
                ])

    print("\nLocations:")
    for i in range(0,len(mappedFrameNumLocation)):
        print("%s" % mappedFrameNumLocation[i][3])

    print("\nReading World Map data")
    mapFileName = "./WorldCountryBoundaries.csv"
    mapFile = open(mapFileName, "r")
    mapLines = mapFile.readlines()
    mapFile.close()
    mapNumLines = len(mapLines)    

    CountryData = []
    CountrySphericalData = []

    for i in range(1,mapNumLines) :
        firstSplitString = mapLines[i].split("\"")
        nonCoordinateString = firstSplitString[2]    
        noncoordinates = nonCoordinateString.split(",")
        countryString = noncoordinates[6]

        if firstSplitString[1].startswith('<Polygon><outerBoundaryIs><LinearRing><coordinates>') and firstSplitString[1].endswith('</coordinates></LinearRing></outerBoundaryIs></Polygon>'):
            coordinateString = firstSplitString[1].replace('<Polygon><outerBoundaryIs><LinearRing><coordinates>','').replace('</coordinates></LinearRing></outerBoundaryIs></Polygon>','').replace(',0 ',',0,')
            coordinates = [float(j) for j in coordinateString.split(",")]  
            coordinateList = np.zeros([int(len(coordinates)/3),2])
            for j in range(0,len(coordinateList)) :
                coordinateList[j,:] = coordinates[j*3:j*3+2]
            coordinateSphericalList = np.zeros([int(len(coordinates)/3),3])
            for j in range(0,len(coordinateSphericalList)) :
                r = 1
                phi = 2*math.pi*coordinates[j*3]/360
                theta = 2*math.pi*(90-coordinates[j*3+1])/360
                coordinateSphericalList[j,0] = r * np.sin(theta) * np.cos(phi)
                coordinateSphericalList[j,1] = r * np.sin(theta) * np.sin(phi)
                coordinateSphericalList[j,2] = r * np.cos(theta)

            CountryData.append([countryString,coordinateList])
            CountrySphericalData.append([countryString,coordinateSphericalList])
        else :
            reducedCoordinateString = firstSplitString[1].replace('<MultiGeometry>','').replace('</MultiGeometry>','').replace('<Polygon>','').replace('</Polygon>','').replace('<outerBoundaryIs>','').replace('</outerBoundaryIs>','').replace('<innerBoundaryIs>','').replace('</innerBoundaryIs>','').replace('<LinearRing>','').replace('</LinearRing>','').replace('</coordinates>','').replace(',0 ',',0,')
            coordinateStringSets = reducedCoordinateString.split("<coordinates>")
            coordinateSets= []
            for j in range(1,len(coordinateStringSets)) :
                coordinateSets.append([float(k) for k in coordinateStringSets[j].split(",")])
            coordinateList = []
            coordinateSphericalList = []
            for j in range(0,len(coordinateSets)) :
                coordinateList.append(np.zeros([int(len(coordinateSets[j])/3),2]))
                for k in range(0,len(coordinateList[j])) :
                    coordinateList[j][k,:] = coordinateSets[j][k*3:k*3+2]
                coordinateSphericalList.append(np.zeros([int(len(coordinateSets[j])/3),3]))
                for k in range(0,len(coordinateSphericalList[j])) :
                    r = 1
                    phi = 2*math.pi*coordinateSets[j][k*3]/360
                    theta = 2*math.pi*(90-coordinateSets[j][k*3+1])/360
                    coordinateSphericalList[j][k,0] = r * np.sin(theta) * np.cos(phi)
                    coordinateSphericalList[j][k,1] = r * np.sin(theta) * np.sin(phi)
                    coordinateSphericalList[j][k,2] = r * np.cos(theta)

            CountryData.append([countryString,coordinateList])
            CountrySphericalData.append([countryString,coordinateSphericalList])

    print("Plotting")
    figSize1 = (19.2, 10.8)
    fontFactor = 0.75
    mpl.rcParams.update({'font.size': 22})
    mpl.rcParams['axes.linewidth'] = 2 #set the value globally
    markerSize = 10

    # plot world map
    fig = plt.figure(3, figsize=figSize1)
    ax = fig.gca()
    # Turn off tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    colorValue = 0.85
    edgeColor = (colorValue*.85, colorValue*.85, colorValue*.85)

    for i in range(0,len(CountryData)) :
        if isinstance( CountryData[i][1], np.ndarray ):
            ax.add_artist(plt.Polygon(CountryData[i][1],edgecolor=edgeColor,
                facecolor=(colorValue,colorValue,colorValue),aa=True))
        else :
            for j in range(0,len(CountryData[i][1])) :
                ax.add_artist(plt.Polygon(CountryData[i][1][j],edgecolor=edgeColor,
                    facecolor=(colorValue,colorValue,colorValue),aa=True))

    plt.plot(getColumn(mappedFrameNumLocationUnitedStates,2),
        getColumn(mappedFrameNumLocationUnitedStates,1),
        linestyle='',color=(0.0, 0.5, 1.0),marker='o',markersize=markerSize)
    plt.plot(getColumn(mappedFrameNumLocationRussia,2),
        getColumn(mappedFrameNumLocationRussia,1),
        linestyle='', color=(1.0, 0.0, 0.0),marker='o',markersize=markerSize)
    plt.plot(getColumn(mappedFrameNumLocationOther,2),
        getColumn(mappedFrameNumLocationOther,1),
        linestyle='', color=(0.0, 0.9, 0.0),marker='o',markersize=markerSize)
    plt.xlim([-180,180])
    plt.ylim([-60,90])
    #plt.show()
    plt.savefig( outputDir+'/worldMap.png', bbox_inches='tight')
