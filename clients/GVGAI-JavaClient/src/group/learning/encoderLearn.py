import os
import sys
from pathlib import Path
from encoderGeneralFunctions import readJsonData, loadModel, loadModelWeights

from keras.models import Sequential
from keras.layers import Dense

# Arguments to be given:
# 1: the text file from which data is read
# 2: Number of epochs
# Example input: "0_1.txt" 1000
data = sys.argv[1]
epochs = int(sys.argv[2])

# Receive input/output data
DATAPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "res", "data", "preprocessed", data))
(inputObject, outputObject) = readJsonData(DATAPATH)

# Define paths and data
MODELPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "model"))
WEIGHTSPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "weights"))

# Define model representation
dimensions = [
    len(inputObject[0]),
    38,
    28,
    18,
    28,
    38,
    len(outputObject[0])
]
activations = ["sigmoid", "sigmoid", "sigmoid", "sigmoid", "sigmoid", "sigmoid"]
loss = "mean_squared_error"
optimizer = "adam"

modelRepresentation = ""
for i in range(0, len(dimensions)-1):
    modelRepresentation = modelRepresentation+str(dimensions[i])+activations[i][0]+"_"
modelRepresentation = modelRepresentation+str(dimensions[len(dimensions)-1])+"_"+loss+"_"+optimizer

# Read or create the model
if Path(os.path.join(MODELPATH, "model"+modelRepresentation+".json")).exists():
    model = loadModel(modelRepresentation)
else:
    model = Sequential()
    for i in range(1, len(dimensions)):
        if i == 1:
            model.add(Dense(dimensions[i], input_dim=dimensions[0], activation=activations[i-1]))
        else:
            model.add(Dense(dimensions[i], activation=activations[i-1]))

    model.compile(loss=loss, optimizer=optimizer, metrics=["accuracy"])

    model_json = model.to_json()
    with open(os.path.join(MODELPATH, "model"+modelRepresentation+".json"), "w") as json_file:
        json_file.write(model_json)

# Set weights if already existing
if Path(os.path.join(WEIGHTSPATH, "weights"+modelRepresentation+".h5")).exists():
    loadModelWeights(modelRepresentation, model)

if os.path.exists(DATAPATH) and data != "":
    model.compile(loss=loss, optimizer=optimizer, metrics=["accuracy"])

    model.fit(inputObject, outputObject, epochs=epochs, batch_size=1, verbose=1)

    model.save_weights(os.path.join(WEIGHTSPATH, "weights"+modelRepresentation+".h5"))
else:
    print("The given data does not exist in '\\res\\data\\preprocessed\\...'")