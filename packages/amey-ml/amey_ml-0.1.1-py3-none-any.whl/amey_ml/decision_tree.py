import numpy as np
import random

class TreeNode:
    """
    Represents a node in the decision tree.
    """
    def __init__(self):
        self.feature_index = None  # Index of the feature used for splitting at this node
        self.threshold = None    # Threshold value used for splitting at this node
        self.left = None         # TreeNode representing the left child
        self.right = None        # TreeNode representing the right child
        self.label = None        # Classification label for the node (if it's a leaf node)
        self.gain = 0            # Information gain achieved by splitting at this node

class RandomForestClassifer:
    """
    A class to represent the Random Forest classifier.
    """
    
    def __init__(self, number_trees):
        """
        Initializes a new instance of the RandomForest class.
        
        Args:
            n_trees (int): Number of trees to build in the forest.
        """
        self.n_trees = number_trees      # Number of trees
        self.trees = []             # List to store the individual decision trees

    def fit_forest(self, features, labels, pruning_threshold):
        """
        Builds the forest by training multiple decision trees.
        
        Args:
            features (np.ndarray): The feature data.
            labels (np.ndarray): The corresponding labels.
            pruning_threshold (int): Minimum number of samples below which a tree should not split further.
        """
        for _ in range(self.n_trees):
            tree = build_tree(features, labels, pruning_threshold, "random")
            self.trees.append(tree)
    
    def predict_single_instance(self, current_tree, features):
        """
        Makes a prediction for a single instance using a given decision tree.
        
        Args:
            tree (TreeNode): The decision tree.
            features (np.ndarray): The feature data of a single instance.
        
        Returns:
            int: Predicted label for the instance.
        """
        if current_tree.label is not None:
            return current_tree.label
        if features[current_tree.feature_index] < current_tree.threshold:
            return self.predict_single_instance(current_tree.left, features)
        else:
            return self.predict_single_instance(current_tree.right, features)

    def predict_class_label(self, features):
        """
        Predicts the class label for a given instance using majority voting among all trees in the forest.
        
        Args:
            features (np.ndarray): The feature data of a single instance.
        
        Returns:
            int: Predicted label for the instance.
        """
        votes = [self.predict_single_instance(tree, features) for tree in self.trees]
        return np.bincount(votes).argmax()
    
class DecisionTreeClassifer:
    """
    Represents a Decision Tree classifier.
    
    Attributes:
        tree (Node): The root of the decision tree.
    """
    
    def __init__(self):
        """Initializes an empty Decision Tree."""
        self.tree = None

    def construct_decision_tree(self, features, labels, pruning_threshold):
        """
        Constructs the decision tree using the given training data and a pruning threshold.
        
        Args:
            features (list of list of float): The feature values of training examples.
            labels (list of int): The labels corresponding to each training example.
            pruning_threshold (float): The threshold used for pruning the tree.
        """
        self.tree = build_tree(features, labels, pruning_threshold)

    def predict_single_instance(self, features):
        """
        Predicts the label of a single instance using the decision tree.
        
        Args:
            features (list of float): The feature values of the instance to be classified.
            
        Returns:
            int: The predicted label of the instance.
        """
        return self._predict_single_instance(self.tree, features)

    def _predict_single_instance(self, node, features):
        """
        Recursively traverses the tree from the given node to predict the label of the instance.
        
        Args:
            node (Node): The current node being checked.
            features (list of float): The feature values of the instance to be classified.
            
        Returns:
            int: The predicted label of the instance.
        """
        # Base case: if the current node is a leaf node (has a label), return the label.
        if node.label is not None:
            return node.label
        
        # Decide the traversal direction based on the feature value and the node's threshold.
        if features[node.feature_idx] < node.threshold:
            return self._predict_single_instance(node.left, features)  # Recurse on left subtree
        else:
            return self._predict_single_instance(node.right, features)  # Recurse on right subtree



    def predict(self, features):
    # If a single instance is passed, reshape it to be 2D
        if len(features.shape) == 1:
            features = features.reshape(1, -1)

        return [self.predict_single_instance(feat) for feat in features]

def string_to_int_conversion(number):
    conversion_map = {"zero": 0,"one": 1,"two": 2,"three": 3,"four": 4,"five": 5,"six": 6,"seven": 7,"eight": 8,"nine": 9,"ten": 10
    }
    return conversion_map.get(number, number)




def count_entropy(labels):
    """
    Calculates the entropy of a set of labels.
    
    Args:
        labels (np.ndarray): Array of labels.
        
    Returns:
        float: The calculated entropy.
    """
    _, counts = np.unique(labels, return_counts=True)
    probs = counts / len(labels)
    return -np.sum(probs * np.log2(probs))

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

def calc_information_gain(current_labels, left_labels, right_labels):
    """
    Calculates the information gain for a given split in the decision tree.
    
    Args:
        current_labels (np.ndarray): Array of original labels before the split.
        left_labels (np.ndarray): Array of labels in the left branch after the split.
        right_labels (np.ndarray): Array of labels in the right branch after the split.
        
    Returns:
        float: The calculated information gain.
    """
    p_left = len(left_labels) / len(current_labels)
    p_right = 1 - p_left
    return count_entropy(current_labels) - p_left * count_entropy(left_labels) - p_right * count_entropy(right_labels)

def get_best_split(features, labels):
    """
    Finds the best feature and threshold to split the data to maximize information gain.
    
    Args:
        features (np.ndarray): Array of feature data.
        labels (np.ndarray): Corresponding array of labels.
        
    Returns:
        tuple: A tuple containing the index of the best feature, the best threshold value, and the maximum information gain.
    """
    max_gain = 0
    best_feature_idx = None
    best_threshold = None
    current_entropy = count_entropy(labels)
    
    for feature_idx in range(features.shape[1]):
        thresholds = np.unique(features[:, feature_idx])
        for threshold in thresholds:
            left_mask = features[:, feature_idx] < threshold
            left_labels = labels[left_mask]
            right_labels = labels[~left_mask]
            gain = calc_information_gain(labels, left_labels, right_labels)
            if gain > max_gain:
                max_gain = gain
                best_feature_idx = feature_idx
                best_threshold = threshold

    return best_feature_idx, best_threshold, max_gain
def print_tree_top(node, tree_id=1, node_id=1):
    """
    Recursively prints the structure of the decision tree from the top.
    
    Args:
        node (Node): The current node being examined.
        tree_id (int, optional): The ID of the current tree. Defaults to 1.
        node_id (int, optional): The ID of the current node. Defaults to 1.
    
    Displays:
        The structure of each node in the tree, including the tree ID, node ID, feature index, threshold, and gain.
    """
    
    # Base case: if it's a leaf node
    if node.label is not None:  
        display_result(f'tree={tree_id:2d}, node={node_id:3d}, feature=-1, thr=-1.00, gain=0.000000')
        return
    
    # Display information about the current node
    display_result(f'tree={tree_id:2d}, node={node_id:3d}, feature={node.feature_index+1:2d}, thr={node.threshold:6.2f}, gain={node.gain:.6f}')
    
    # Recursive calls for left and right children
    print_tree_top(node.left, tree_id, 2*node_id)
    print_tree_top(node.right, tree_id, 2*node_id+1)

def build_tree(features, labels, pruning_threshold, feature_selection="optimized"):
    """
    Recursively builds a decision tree using the given features and labels.
    
    Args:
        features (np.ndarray): The feature data.
        labels (np.ndarray): The corresponding labels.
        pruning_threshold (int): Minimum number of samples below which the tree should not split further.
        feature_selection (str, optional): Method for feature selection ("optimized" or "random"). Defaults to "optimized".
    
    Returns:
        TreeNode: The root of the constructed decision tree.
    """
    
    # Base case: if the node is pure or below the pruning threshold
    if len(np.unique(labels)) == 1 or len(labels) <= pruning_threshold:
        node = TreeNode()
        node.label = labels[0]
        return node
    
    # Determine the best feature and threshold for splitting
    if feature_selection == "optimized":
        feature_idx, current_threshold, information_gain = get_best_split(features, labels)
    else:
        feature_index = random.randint(0, features.shape[1] - 1)
        thresholds = np.unique(features[:, feature_index])
        current_threshold = random.choice(thresholds)
        left_mask = features[:, feature_index] < current_threshold
        left_class_labels = labels[left_mask]
        right_class_labels = labels[~left_mask]
        information_gain = calc_information_gain(labels, left_class_labels, right_class_labels)
    
    # If no gain is achieved with the split, create a leaf node
    if information_gain == 0:
        node = TreeNode()
        node.label = np.bincount(labels).argmax()
        return node
    
    # Recursively build the left and right sub-trees
    left_mask = features[:, feature_index] < current_threshold
    tree_left_node = build_tree(features[left_mask], labels[left_mask], pruning_threshold, feature_selection)
    tree_right_node = build_tree(features[~left_mask], labels[~left_mask], pruning_threshold, feature_selection)

    node = TreeNode()
    node.feature_index = feature_index
    node.threshold = current_threshold
    node.gain = information_gain
    node.left = tree_left_node
    node.right = tree_right_node

    return node

def display_result(*args, **kwargs):
    print(*args, **kwargs)  
    with open("output.txt", "a") as f: 
        print(*args, file=f, **kwargs)

def output(train_path, test_path, model_type, threshold):
    """
    Train and test a decision tree or random forest classifier based on the specified model type.
    
    Args:
        train_path (str): The path to the training dataset file.
        test_path (str): The path to the test dataset file.
        model_type (str): Type of model to train - "optimized" for decision tree or any other value for random forest.
        threshold (float): The threshold value used for pruning (for decision trees) or other purpose (for random forest).
    
    Displays:
        The structure of the trained trees and the classification results on the test dataset.
    """
    
    # Load training and test datasets
    train_data, train_labels = extract_data(train_path)
    test_data, test_labels = extract_data(test_path)
    
    # List to store the classifiers (either decision tree or random forest)
    classifiers = []
    
    # Train the specified classifier type
    if model_type == "optimized":
        decision_tree_classifier = DecisionTreeClassifer()
        decision_tree_classifier.construct_decision_tree(train_data, train_labels, threshold)
        classifiers.append(decision_tree_classifier)
    else:
        forest_model_classifier = RandomForestClassifer(model_type)
        forest_model_classifier.fit_forest(train_data, train_labels, threshold)
        classifiers.append(forest_model_classifier)
    
    # Display the structure of the trained trees
    for index, classifier in enumerate(classifiers, 1):
        if isinstance(classifier, DecisionTreeClassifer):
            print_tree_top(classifier.tree, tree_id=index)
        else:
            for t_index, subtree in enumerate(classifier.trees, 1):
                print_tree_top(subtree, tree_id=t_index)
    
    # List to store prediction accuracies for all test instances
    accuracies = []
    
    # Predict labels for the test dataset and display results
    for idx, (input_data, actual_label) in enumerate(zip(test_data, test_labels), 1):
        # Make predictions using the trained classifier
        predictions = [classifiers[0].predict_class_label(input_data)]
        
        # Evaluate the predictions
        pred_label, pred_accuracy = calculate_prediction_single_instance(predictions, actual_label)
        
        # Display the results for each test instance
        display_result(f'ID={idx:5d}, predicted={pred_label:3d}, true={actual_label:3d}, accuracy={pred_accuracy:4.2f}')
        
        # Store the accuracy for the current prediction
        accuracies.append(pred_accuracy)
    
    # Display the overall classification accuracy
    display_result(f'classification accuracy={np.mean(accuracies):6.4f}')


def calculate_prediction_single_instance(predictions, actual_label):
    """
    Evaluate the prediction for a single instance, considering ties in the prediction.
    
    Args:
        predictions (list of int): List of predicted labels.
        true_label (int): The actual label of the instance.
    
    Returns:
        tuple: The predicted class and the corresponding accuracy.
    """
    
    predictions = np.array(predictions).flatten()
    counts = np.bincount(predictions)
    max_count = counts.max()
    same_classes = np.where(counts == max_count)[0]
    
    # Randomly choose from the tied classes
    predicted_class = np.random.choice(same_classes)
    
    # Determine the accuracy based on the predicted class
    if predicted_class == actual_label:
        if len(same_classes) == 1:
            return predicted_class, 1.0
        else:
            return predicted_class, 1.0 / len(same_classes)
    else:
        return predicted_class, 0.0


