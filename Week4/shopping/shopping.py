import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Administrative[0],Administrative_Duration[1],Informational[2],Informational_Duration[3],ProductRelated[4],ProductRelated_Duration[5],BounceRates[6],ExitRates[7],PageValues[8],SpecialDay[9],Month[10],OperatingSystems[11],Browser[12],Region[13],TrafficType[14],VisitorType[15],Weekend[16],Revenue[17]

    # Dictionary mapping month names to numerical representations.
    months_to_numbers = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
    "Jul": 6, "Aug": 7, "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }   

    # Initializes empty lists for storing processed data.
    evidence = []
    labels = []

    # Opens and reads the CSV file, skipping the header row.
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        # Iterates through each row in the CSV, converting and processing data as needed.
        for row in reader:
            # Converts VisitorType to binary, Weekend to binary, and Month to a numerical index.
            row[15] = 1 if row[15] == 'New_Visitor' else 0
            row[16] = 1 if row[16] == 'TRUE' else 0
            row[10] = months_to_numbers[row[10]]
            # Same with Revenue
            row[-1] = 1 if row[-1] == 'TRUE' else 0
            # Converts specified fields to floats for numerical analysis.
            row[1] = float(row[1])
            row[3] = float(row[3])
            row[5] = float(row[5])
            row[6] = float(row[6])
            row[7] = float(row[7])
            row[8] = float(row[8])
            row[9] = float(row[9])

            # Appends processed evidence to the evidence list and label to the labels list.
            evidence.append(row[:-1])
            labels.append(row[-1])

    #Convert data to numeric values
    evidence = [[float(item) if isinstance(item, str) and item.replace('.', '', 1).isdigit() else item for item in row] for row in evidence]
    
    # Returns a tuple of processed evidence and labels.
    result_tuple = (evidence, labels)

    return (result_tuple)
 


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Initialize the classifier.
    clf = KNeighborsClassifier(n_neighbors=1)

    # Fits the model to the data and returns it.
    return (clf.fit(evidence, labels))


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    #labels - rzeczywiste, 
    #predictions - predykcja,
    #return(sensitivity, specificity)
    #sensitivity - float 0-1 (true positivie rate): the proportion of actual positive labels that were accurately identified

    # Initializes counters for true positives, false negatives, true negatives, and false positives.
    true_positives = 0
    false_negatives = 0

    # Calculates sensitivity: the proportion of actual positives correctly identified.
    for actual, predicted in zip(labels, predictions):
        if actual == 1 and predicted == 1:
            true_positives += 1
        elif actual == 1 and predicted == 0:
            false_negatives += 1

    sensitivity = float(true_positives / (true_positives + false_negatives)) if (true_positives + false_negatives) > 0 else 0

    # Same for specificity
    true_negatives = 0
    false_positives = 0

    for actual, predicted in zip(labels, predictions):
        if actual == 0 and predicted == 0:
            true_negatives += 1
        elif actual == 0 and predicted == 1:
            false_positives += 1
    
    specificity = float(true_negatives / (true_negatives + false_positives)) if (true_negatives + false_positives) > 0 else 0

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
