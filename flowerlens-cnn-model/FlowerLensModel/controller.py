#import FlowerModel
import dataPipeline
import modelTrain
import prediction
import performance

dataSplit = None

# this entire .py file is only for the few cases where you want to do some manual testing of the model
# without using postman etc.
while True:

    # Get user input as an integer
    number = int(input("Enter a number (1, 2, 3, 4, 5 or 6): "))

    # Call different functions based on the input number (used to test functions in different orders)
    if number == 1:
        dataPipeline.getTrainingData()
    elif number == 2:
        dataSplit = dataPipeline.splitData()
    elif number == 3:
        if dataSplit != None:
            modelTrain.createModel(dataSplit, '1.0')
    elif number == 4:
        print ("hey")
        flower,prediction_confindence, heatmap = prediction.makePrediction('1.0','test_flower.jpg')
        print ('flower is: ' + flower + ' and confindence is: ' + str(prediction_confindence))
    elif number == 5:
        dataSplit = dataPipeline.splitData()
        if dataSplit != None:
            modelTrain.createModel(dataSplit, '1.0')
            X_train, y_train, X_validate, X_test, y_validate, y_test = dataSplit
            performance_analysis, confusion_matrix = performance.performance('1.0', X_test, y_test)
    elif number == 6:
        dataSplit = dataPipeline.DirectImageDataSplit()
        if dataSplit != None:
            modelTrain.createModel(dataSplit, '2.0')
            X_train, y_train, X_validate, X_test, y_validate, y_test = dataSplit
            performance_analysis, confusion_matrix = performance.performance('1.0', X_test, y_test)
    else:
        print("Invalid number. Please enter 1, 2, 3, 4, 5 or 6.")


    # break condition to exit the loop
    break_condition = input("Do you want to exit? (yes/no): ")
    if break_condition.lower() == "yes":
        break