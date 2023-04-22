# Borja :)

import sys
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input File")
    parser.add_argument("-o", "--output", help="Output File")
    parser.add_argument("-k", "--k", help="K argument", type=int)
    parser.add_argument("-nf", "--features", help="FeaturesSize", type=int)
    parser.add_argument(
        "-c", "--clasS", help="Class index in the dataset", type=int)
    args = parser.parse_args()

    featuresValuesMax = []
    featuresValuesMin = []

    if args.file and args.output and args.k and args.features and (args.clasS == 0 or args.clasS != 0):
        print("All data avaible")
    else:
        print("Use --help for more info")
        sys.exit()
    contLine = 0
    featureCont = 0

    with open(args.output, "w") as outputFile:
        with open(args.file, "r") as inputFile:
            for line in inputFile:
                print(contLine)
                # HEAD: Column names row
                if contLine == 0:
                    outputFile.write(line)
                # BODY: Numeric data
                else:
                    # iterate through every numeric value of each column
                    for feature in line.split(","):
                        try:
                            Ffeature = float(feature)
                        except ValueError:
                            Ffeature = 1
                        if contLine == 1:
                            featuresValuesMax.append(Ffeature)
                            featuresValuesMin.append(Ffeature)
                        else:
                            if args.clasS == 1:
                                resta = 1
                            else:
                                resta = 0
                            if featuresValuesMax[featureCont-resta] < Ffeature:
                                featuresValuesMax[featureCont-resta] = Ffeature
                            if featuresValuesMin[featureCont-resta] > Ffeature:
                                featuresValuesMin[featureCont-resta] = Ffeature
                        featureCont = featureCont+1
                featureCont = 0
                contLine = contLine + 1

        w = list((i-j)/args.k for (i, j)
                 in zip(featuresValuesMax, featuresValuesMin))

        contLine = 0
        with open(args.file, "r") as inputFile:
            for line in inputFile:
                print(contLine)
                if contLine > 0:
                    lineaInteres = []
                    for feature in line.split(","):

                        try:
                            if featureCont == 0:
                                Ffeature = feature
                            else:
                                Ffeature = float(feature)
                        except ValueError:
                            Ffeature = feature
                        if args.clasS == 1:
                            resta = 1
                        else:
                            resta = 0
                        # if (w[featureCont-resta] != float(0)):
                        if (featureCont != args.clasS):
                            try:
                                Ffeature = float(feature)
                                lineaInteres.append(
                                    str(int((Ffeature-featuresValuesMin[featureCont-resta])/w[featureCont-resta])))
                            except ValueError:
                                lineaInteres.append(str(Ffeature))
                        else:
                            lineaInteres.append(str(Ffeature))
                        featureCont = featureCont+1

                    featureCont = 0
                    write = ",".join(lineaInteres)
                    write = write.strip()+"\n"
                    outputFile.write(write)
                contLine = contLine + 1

    print("Finish properlly")
