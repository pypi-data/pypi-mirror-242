import numpy as np


def load_data(file_path):
    """
    This function loads a dataset from the given file path. The data is expected to be either one-dimensional or 
    multi-dimensional.

    If the data is one-dimensional:
        - The entire data array is treated as the target variable 'y'.
        - 'X' is generated as an array of indices corresponding to 'y'.

    If the data is multi-dimensional:
        - The last column of the data is extracted as the target variable 'y'.
        - The remaining columns are treated as the feature matrix 'X'.

    Parameters:
    file_path (str): The path to the file containing the dataset.

    Returns:
    X (np.ndarray): The feature matrix.
    y (np.ndarray): The target variable.
    """
    data = np.genfromtxt(file_path, delimiter=None, dtype=float)

    # Check if data is 1-dimensional
    if len(data.shape) == 1:
        # If data is 1-dimensional, treat the whole array as y (target) and create X as an array of indices.
        X = np.arange(len(data)).reshape(-1, 1)
        y = data
    else:
        # If data is multi-dimensional, extract features X and target y
        X = data[:, :-1]
        y = data[:, -1]

    return X, y


def phi(X, degree):
    """
    This function performs feature expansion on the input data matrix X to a specified polynomial degree.

    It adds a column of ones to the input matrix X as a bias term and subsequently appends additional
    columns representing each feature in X raised to the power of 2 up to the specified degree.

    :param X: numpy.ndarray, input data matrix where each row represents a sample and each column a feature.
    :param degree: int, the degree of the polynomial for feature expansion.

    :return: numpy.ndarray, the transformed data matrix after feature expansion.
    """
    # If degree is 1, simply add a column of ones for the bias term
    if degree == 1:
        return np.column_stack([np.ones(X.shape[0]), X])

    # Initialize the phi matrix with a column of ones and the original features
    phi = np.column_stack([np.ones(X.shape[0]), X])

    # Add additional polynomial features up to the specified degree
    for d in range(2, degree + 1):
        phi = np.column_stack([phi, X**d])

    return phi


def output(training_file, test_file, degree, lambda1):
    """
    This function performs linear regression with regularization on the given training and test data.

    It loads the training and test data from the specified files, performs feature expansion, calculates
    the weights using regularized linear regression, makes predictions on both the training and test data,
    and calculates the mean squared error for both.

    :param training_file: str, path to the training file.
    :param test_file: str, path to the test file.
    :param degree: int, the degree of the polynomial for feature expansion.
    :param lambda1: int, the regularization parameter.

    :return: 0, indicating successful completion.
    """
    # Load data
    X_train, y_train = load_data(training_file)
    X_test, y_test = load_data(test_file)
    file_name = training_file.split('/')[-1]

    # Feature expansion
    phi_train_matrix = phi(X_train, degree)
    phi_test_matrix = phi(X_test, degree)

    # Regularized Linear Regression
    lambda_matrix = lambda1 * np.eye(phi_train_matrix.shape[1])
    weights = np.linalg.pinv(phi_train_matrix.T @ phi_train_matrix +
                             lambda_matrix) @ phi_train_matrix.T @ y_train  # Using pseudo-inverse

    # Prediction
    predictions_train = phi_train_matrix @ weights
    predictions_test = phi_test_matrix @ weights

    # Mean squared error
    mse_train = ((y_train - predictions_train)**2).mean()
    mse_test = ((y_test - predictions_test)**2).mean()

    # Prepare the output file name
    output_file = file_name.split('.')[0]
    output_file = output_file.split('_')[0]
    output_file += "_" + (str(degree) + "_" + str(lambda1))
    output_file += "_actual.txt"

    # Write weights, predictions, and squared errors to the console.
    for idx, weight in enumerate(weights):
        print(f'w{idx}={weight:.4f}')

        # Print test results
    for index, (predicted, actual) in enumerate(zip(predictions_test, y_test)):
        squared_error = (predicted - actual)**2
        print(f'ID={index + 1:5d}, output={predicted:14.4f}, target value = {actual:10.4f}, squared error = {squared_error:.4f}')

    return 0
