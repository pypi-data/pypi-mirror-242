import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def load_data(directory, dataset, train=True):
    """
    Load dataset from a specified directory.
    
    Parameters:
    - directory (str): Path to the directory containing the dataset files.
    - dataset (str): Name of the dataset.
    - train (bool, optional): If True, loads the training dataset, otherwise loads the test dataset. Default is True.
    
    Returns:
    - X (numpy.ndarray): Features from the dataset.
    - unique_classes (numpy.ndarray): Integer labels corresponding to the unique classes.
    - list(y) (list): List of unique class names.
    
    Note:
    - The dataset file should be in the format: "datasetname_training.txt" for training data and 
      "datasetname_test.txt" for test data.
    - The last column of the dataset should contain the labels.
    """
    print("1. loading data....\n")
    filepath = f"{directory}/{dataset}_{ 'training' if train else 'test' }.txt"
    data = np.loadtxt(filepath, dtype=str)
    X = data[:, :-1].astype(float)
    y, unique_classes = np.unique(data[:, -1], return_inverse=True)
    print("2. data loaded...\n")
    return X, unique_classes, list(y)

def evaluate_predictions(predictions, y_test, classes):
    """
    Evaluate predictions against true labels and calculate accuracy.
    
    Parameters:
    - predictions (numpy.ndarray): Predictions from the model.
    - y_test (numpy.ndarray): True labels.
    - classes (list): List of unique class names.
    
    Returns:
    - classification_accuracy (float): Overall classification accuracy.
    """
    total_accuracy = 0
    for object_id, (pred, true) in enumerate(zip(predictions, y_test), start=1):
        pred_classes = np.where(pred == np.max(pred))[0]
        predicted_class = np.random.choice(pred_classes)
        true_class = classes[true]
        accuracy = 1/len(pred_classes) if true in pred_classes else 0
        print('ID=%5d, predicted=%10s, true=%10s, accuracy=%4.2f' % 
              (object_id, classes[predicted_class], true_class, accuracy))
        total_accuracy += accuracy

    classification_accuracy = total_accuracy / len(y_test)
    return classification_accuracy

def output(directory, dataset, layers, units_per_layer, epochs):
    """
    Train and evaluate a neural network classifier using Keras.
    
    Parameters:
    - directory (str): Path to the directory containing the dataset files.
    - dataset (str): Name of the dataset.
    - layers (int): Number of layers in the neural network.
    - units_per_layer (int): Number of units in each hidden layer.
    - epochs (int): Number of epochs for training.
    
    Outputs:
    - Prints the training progress, predictions on the test data, and the overall classification accuracy.
    
    Note:
    - The function first loads and preprocesses the data, then constructs the neural network model based on the 
      specified parameters, trains the model, and finally evaluates its performance on the test data.
    """
    # Load training and test datasets
    X_train, y_train, classes = load_data(directory, dataset, train=True)
    X_test, y_test, _ = load_data(directory, dataset, train=False)

    print("3. normalizing datasets....\n")
    # Normalize the datasets
    max_abs_val = np.max(np.abs(X_train))
    X_train /= max_abs_val
    X_test /= max_abs_val
    print("4. normalizing datasets completed")

    print("5. Building model....\n")
    # Build the model
    model = Sequential()
    model.add(Dense(units_per_layer, activation='sigmoid', input_dim=X_train.shape[1]))
    for _ in range(2, layers):
        model.add(Dense(units_per_layer, activation='sigmoid'))
    model.add(Dense(len(classes), activation='sigmoid'))
    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(),
                  metrics=['accuracy'])
    
    print("6. Model build completed...\n")
    
    print("7. Training model.....\n")
    # Train the model
    model.fit(X_train, y_train, epochs=epochs, verbose=1)
    print("8. model training complete....\n")

    print("9. Predict Data ...\n")
    # Predict on test data
    predictions = model.predict(X_test)
    
    total_accuracy = 0
    classification_accuracy = evaluate_predictions(predictions, y_test, classes)
    print('classification accuracy=%6.4f\n' % (classification_accuracy))


