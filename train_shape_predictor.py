import os
import sys
import glob

import dlib

# In this example we are going to train a face detector based on the small
# faces dataset in the examples/faces directory.  This means you need to supply
# the path to this faces folder as a command line argument so we will know
# where it is.
faces_folder = 'total'


def train_shape_predictor_param(oversampling_amount, nu):
    options = dlib.shape_predictor_training_options()
    # Now make the object responsible for training the model.
    # This algorithm has a bunch of parameters you can mess with.  The
    # documentation for the shape_predictor_trainer explains all of them.
    # You should also read Kazemi's paper which explains all the parameters
    # in great detail.  However, here I'm just setting three of them
    # differently than their default values.  I'm doing this because we
    # have a very small dataset.  In particular, setting the oversampling
    # to a high amount (300) effectively boosts the training set size, so
    # that helps this example.
    options.oversampling_amount = oversampling_amount
    # I'm also reducing the capacity of the model by explicitly increasing
    # the regularization (making nu smaller) and by using trees with
    # smaller depths.
    options.nu = nu
    options.tree_depth = 2
    options.be_verbose = True

    # dlib.train_shape_predictor() does the actual training.  It will save the
    # final predictor to predictor.dat.  The input is an XML file that lists the
    # images in the training dataset and also contains the positions of the face
    # parts.
    predictor_name = "predictor" + str(oversampling_amount) + "_" + str(nu) + ".dat"
    training_xml_path = os.path.join(faces_folder, "training_with_face_landmarks.xml")
    dlib.train_shape_predictor(training_xml_path, predictor_name, options)

    # Now that we have a model we can test it.  dlib.test_shape_predictor()
    # measures the average distance between a face landmark output by the
    # shape_predictor and where it should be according to the truth data.
    print("\nTraining accuracy: {}".format(
        dlib.test_shape_predictor(training_xml_path, predictor_name)))
    # The real test is to see how well it does on data it wasn't trained on.  We
    # trained it on a very small dataset so the accuracy is not extremely high, but
    # it's still doing quite good.  Moreover, if you train it on one of the large
    # face landmarking datasets you will obtain state-of-the-art results, as shown
    # in the Kazemi paper.
    testing_xml_path = os.path.join(faces_folder, "testing_with_face_landmarks.xml")
    test_acc = dlib.test_shape_predictor(testing_xml_path, predictor_name)
    print("Testing accuracy: {}".format(test_acc))
    print("oversampling_amount: ", oversampling_amount, "\nNu: ", nu, "\n", predictor_name + "completed")
    return -test_acc


if __name__ == '__main__':
    x,y = dlib.find_min_global(train_shape_predictor_param, 
                           [50, 0.05],  # Lower bound constraints on x0 and x1 respectively
                           [150, 0.1],    # Upper bound constraints on x0 and x1 respectively
                           20)         # The number of times find_min_global() will call holder_table()
    print("optimal inputs: {}".format(x))
    print("optimal output: {}".format(y))
