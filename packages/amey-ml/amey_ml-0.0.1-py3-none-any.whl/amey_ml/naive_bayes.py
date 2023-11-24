import numpy as np

def load_data(filename):
    with open(filename, 'r') as file:
        data = [list(map(float, line.strip().split())) for line in file]
    
    data = np.array(data)
    X = data[:, :-1]
    y = data[:, -1]
    return X, y

def get_classes_from_file(filename):
    classes = []
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split()  # Splitting the data by spaces
            classes.append(float(data[-1]))  # Adding the last element of each line to the classes list
    return list(set(classes))  # Using set to get unique classes and then converting it back to a list

def get_data_for_class(filename, target_class=5.0):
    data_for_class = []

    # Read the file and filter rows for the target class
    with open(filename, 'r') as file:
        for line in file:
            row = [float(x) for x in line.strip().split()]
            if row[-1] == target_class:  # Checking if the last column matches the target class
                data_for_class.append(row)

    return data_for_class

def get_mean_for_class(filename, target_class=1.0):
    # Initialize lists to store data
    data_for_class = []

    # Read the file and filter data
    with open(filename, 'r') as file:
        for line in file:
            row = [float(x) for x in line.strip().split()]
            if row[-1] == target_class:  # Checking if the last column matches the target class
                data_for_class.append(row[:-1])  # Exclude the last column (class label)

    # Convert to a 2D list for easier manipulation
    data_matrix = [list(i) for i in zip(*data_for_class)]

    # Compute mean for each column and format to ensure two decimal places
    means = ["{:.2f}".format(sum(column) / len(column)) for column in data_matrix]

    return means

def get_std_for_class(filename, target_class=1.0):
    # Initialize lists to store data
    data_for_class = []

    # Read the file and filter data
    with open(filename, 'r') as file:
        for line in file:
            row = [float(x) for x in line.strip().split()]
            if row[-1] == target_class:  # Checking if the last column matches the target class
                data_for_class.append(row[:-1])  # Exclude the last column (class label)

    # Convert to a 2D list for easier manipulation
    data_matrix = [list(i) for i in zip(*data_for_class)]

    # Compute mean for each column
    means = [sum(column) / len(column) for column in data_matrix]

    # Compute variance for each column
    variances = []
    for i, column in enumerate(data_matrix):
        mean = means[i]
        variance = sum([(x - mean)**2 for x in column]) / (len(column)-1)
        variances.append(variance)
    
    # Compute standard deviation from variance, 
    # replace values less than 0.01 with 0.01 and format to ensure two decimal places
    std_devs = []
    for variance in variances:
        std_dev = max(variance**0.5, 0.01)
        std_devs.append("{:.2f}".format(std_dev))

    return std_devs

def classify(X_test, mean_dict, std_dict, class_probs):
    results = []
    all_probs = []
    
    for x in X_test:
        probs = {}
        for c in class_probs:
            prob_x_given_c = 1
            
            for i in range(len(x)):
                # Convert mean and std from string to float
                mean_val = float(mean_dict[c][i])
                std_val = float(std_dict[c][i])
                
                exponent = -((x[i] - mean_val)**2) / (2 * (std_val**2))
                base = np.e
                prob = (base**exponent) / ((2 * np.pi)**0.5 * std_val)
                prob_x_given_c *= prob
                
            probs[c] = prob_x_given_c * class_probs[c]
        
        total_prob = sum(probs.values())
        probs = {key: val/total_prob for key, val in probs.items()}
        
        predicted_class = max(probs, key=probs.get)
        predicted_prob = probs[predicted_class]
        results.append((predicted_class, predicted_prob))
        all_probs.append(probs)
    
    return results, all_probs


def output(training_file, test_file):
    # Load data
    X_train, y_train = load_data(training_file)
    X_test, y_test = load_data(test_file)

    class_list = get_classes_from_file(training_file)
    mean_dict = {}
    std_dict = {}
    for cls in class_list:
        mean_dict[cls] = get_mean_for_class(training_file, cls)
    for cls in class_list:
        std_dict[cls] = get_std_for_class(training_file, cls)

    class_probs = {}
    for cls in class_list:
        class_data = [y for y in y_train if y == cls]
        class_probs[cls] = len(class_data) / len(y_train)
    
    # Classify
    results, all_instance_probs = classify(X_test, mean_dict, std_dict, class_probs)

    
    #print training results
    for cls, means in mean_dict.items():
            int_class = int(cls)  # Convert the class value to an integer
            stds = std_dict[cls]
            for index, (mean, std) in enumerate(zip(means, stds)):
                line = f"Class {int_class}, attribute {index + 1}, mean = {mean}, std = {std}\n"
                print(line, end="")  # Print to console
                


        # Print classification results
    accuracies = []
    for i, ((predicted_class, predicted_prob), true_class) in enumerate(zip(results, y_test)):
            if predicted_class == true_class:
                accuracy = 1.0
            else:
                tied_classes = [c for c, p in all_instance_probs[i].items() if p == predicted_prob]
                if true_class in tied_classes:
                    accuracy = 1.0 / len(tied_classes)
                else:
                    accuracy = 0.0
            accuracies.append(accuracy)
          
            print(f"ID={i+1:5d}, predicted={int(predicted_class):3d}, probability = {predicted_prob:.4f}, true={int(true_class):3d}, accuracy={accuracy:.2f}")
        # Print overall accuracy
    print(f"classification accuracy={np.mean(accuracies):.4f}")

