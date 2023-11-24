import numpy as np
import random
from collections import Counter
from scipy.stats import zscore


def string_to_int_conversion(number):
    conversion_map = {"zero": 0,"one": 1,"two": 2,"three": 3,"four": 4,"five": 5,"six": 6,"seven": 7,"eight": 8,"nine": 9,"ten": 10
    }
    return conversion_map.get(number, number)

def extract_data(file_path):
    """
    Loads data from a file, where each row consists of feature values followed by a label.
    
    Args:
        file_path (str): Path to the file containing data.
        
    Returns:
        tuple: A tuple containing two numpy arrays: features and labels.
    """
    
    features = []
    labels = []
    
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split()
            
            # Extract label from the last value in the line
            label_str = values[-1]
            if label_str.isdigit():
                label = int(label_str)
            elif label_str.startswith("class"):
                label = int(label_str.replace("class", ""))
            else:
                label = string_to_int_conversion(label_str)  # Assumes a function that maps strings to integers

            # Extract features from the remaining values in the line
            try:
                # Determine if the features are represented as floats or integers
                float(values[0])
                row_features = [float(val) for val in values[:-1]]
            except ValueError:
                row_features = [int(val) for val in values[:-1]]
            
            features.append(row_features)
            labels.append(label)
    
    # Convert feature and label lists to numpy arrays
    features_np = np.array(features)
    labels_np = np.array(labels)

    return features_np, labels_np


def output(training_file, test_file, k):
    """
    Perform K-nearest neighbors classification on a given test dataset based on a provided training dataset.
    
    Args:
        training_file (str): The file path for the training data.
        test_file (str): The file path for the test data.
        k (int): The number of nearest neighbors to consider for the voting process in KNN.
        
    The function assumes that the input files are in a text format where each line represents a data point.
    Each line should consist of a list of features followed by a single label, all separated by spaces.
    The labels can be numeric or string values, and the function will handle the conversion to integers
    for the KNN algorithm. String labels are expected to be words for numbers (e.g., "two" for 2) or 
    'class' followed by a number (e.g., "class1" for 1).
    
    The features are normalized using z-score normalization before classification.
    
    For each data point in the test set, the function prints out the data point ID, the predicted label,
    the true label, and the classification accuracy for that point.
    
    After all predictions are made, the function prints out the overall classification accuracy of the 
    model on the test set.
    
    The function handles ties in the voting process by randomly selecting a class from the tied classes.
    If there is no tie, the class with the most votes is selected.
    
    Returns:
        None: This function does not return any value. It prints the classification results directly.
    """

    X_train,y_train = extract_data(training_file)
    X_test,y_test = extract_data(test_file)
    
    
    # Normalize the features
    means = np.mean(X_train, axis=0)
    stds = np.std(X_train, axis=0, ddof=1)
    stds[stds == 0] = 1  # Avoid division by zero
    X_train = (X_train - means) / stds
    X_test = (X_test - means) / stds
    
    # Classification
    accuracies = []
    for i, test_instance in enumerate(X_test):
        # Compute distances
        distances = np.linalg.norm(X_train - test_instance, axis=1)
        
        # Find the k nearest neighbors
        nearest_neighbor_ids = np.argsort(distances)[:k]
        nearest_neighbor_classes = y_train[nearest_neighbor_ids]
        
        # Vote for the classes
        class_counter = Counter(nearest_neighbor_classes)
        top_classes = class_counter.most_common()
        
        # Handle ties
        if len(top_classes) > 1 and top_classes[0][1] == top_classes[1][1]:
            # Tie, choose a winner randomly
            predicted_class = random.choice(top_classes)[0]
            accuracy = 1 / len([count for _, count in top_classes if count == top_classes[0][1]])
        else:
            # No tie, choose the class with the most votes
            predicted_class = top_classes[0][0]
            accuracy = 1 if predicted_class == y_test[i] else 0
        
        accuracies.append(accuracy)
        print('ID=%5d, predicted=%10s, true=%10s, accuracy=%4.2f' % (i+1, predicted_class, y_test[i], accuracy))
    
    # Print overall classification accuracy
    classification_accuracy = np.mean(accuracies)
    print('classification accuracy=%6.4f' % classification_accuracy)
