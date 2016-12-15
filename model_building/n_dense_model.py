import time
import numpy as np
import os
import tensorflow as tf
import random as rng

x_filename = '/home/valentin/Working/phd_project/dataset/x_mfcc_twoclass_S1_9_200ms_100ms_inc_16kHz_25000.txt'
y_filename = '/home/valentin/Working/phd_project/dataset/y_mfcc_twoclass_S1_9_200ms_100ms_inc_16kHz_25000.txt'

# x_filename = 'debug_x.txt'
# y_filename = 'debug_y.txt'


def gen_debug_data():

    t_start = time.time()

    n_train_samples = 20000
    n_input_sz = 250
    n_classes = 1

    n_total_samples = n_train_samples
    inputs = np.zeros([n_total_samples, n_input_sz], dtype=float, order='C')
    outputs = np.zeros([n_total_samples, n_classes], dtype=float, order='C')

    for i in range(n_total_samples):
        id_class = rng.randint(0, 1)
        outputs[i] = id_class

        for j in range(n_input_sz):
            inputs[i][j] = id_class + 1 / rng.randint(1, 64)

    t_stop = time.time()
    print("Data Generating Time (seconds): ", str(t_stop - t_start))

    return [inputs, outputs]


def main(_):

    # os.environ["CUDA_VISIBLE_DEVICES"] = ""

    ###########################################################################
    # Generate Debug Data
    ###########################################################################

    [inputs_t, outputs_t] = gen_debug_data()

    ###########################################################################
    # Load Train / Test Data
    ###########################################################################

    t_start = time.time()

    # Load Input Files
    # inputs_t = np.loadtxt(x_filename)
    # outputs_t = np.loadtxt(y_filename)

    # Experiment Parameters
    n_classes = 1       # outputs.shape[1]
    n_batches = 200
    n_steps = 1
    sz_set = inputs_t.shape[0]

    sz_validate = int(sz_set * 0.05)
    sz_inference = int(sz_set * 0.1)
    sz_train = int(sz_set - sz_validate - sz_inference)
    sz_batch = int(sz_train / n_batches)
    sz_input = inputs_t.shape[1]

    # Trick python into knowing the size of _y tensor
    inputs = np.zeros([sz_set, sz_input], dtype=float, order='C')
    outputs = np.zeros([sz_set, n_classes], dtype=float, order='C')
    for i in range(sz_set):
        outputs[i][0] = outputs_t[i]
        for j in range(sz_input):
            inputs[i][j] = inputs_t[i][j]

    # Debug Code - Alter Inputs
    # for i in range(sz_set):
    #    if outputs[i] == 1:
    #        for j in range(sz_input):
    #            inputs[i][j] /= 32
    #            inputs[i][j] += 1

    t_stop = time.time()
    print("Input prepare time   : ", str(t_stop - t_start))

    # Debug Messages
    print("Total inputs         : ", str(sz_set))
    print("Input length         : ", str(sz_input))
    print("Number of classes    : ", str(n_classes))
    print("Used for training    : ", str(sz_train))
    print("Used for inference   : ", str(sz_inference))
    print("Used for validation  : ", str(sz_validate))
    print("Batch size           : ", str(sz_batch))

    ###########################################################################
    # Split Data into Train, Test and Validate
    ###########################################################################

    x_train = inputs[0:sz_train][:]
    x_inference = inputs[sz_train:sz_train+sz_inference][:]
    x_validate = inputs[sz_train+sz_inference:sz_set][:]
    y_train = outputs[0:sz_train]
    y_inference = outputs[sz_train:sz_train+sz_inference]
    y_validate = outputs[sz_train+sz_inference:sz_set]

    ###########################################################################
    # Build Model Graph
    ###########################################################################

    # Data Layer
    x_ = tf.placeholder(tf.float32, [None, sz_input])

    ###########################################################################
    # Debug NN Architecture
    ###########################################################################

    # w0 = tf.Variable(tf.random_normal([sz_input, 1], mean=0.0), dtype=tf.float32)
    # b0 = tf.Variable(tf.random_normal([n_classes], mean=0.0), dtype=tf.float32)
    # y = tf.sigmoid(tf.matmul(x_, w0) + b0)

    ###########################################################################
    # Targeted NN Architecture
    ###########################################################################

    n_dense_layers = 5
    n_layer_size = sz_input
    v_activations = []
    v_weights = []
    v_biases = []

    v_activations.append(x_)
    for i in range(1, n_dense_layers):
        w_temp = tf.Variable(tf.random_normal([n_layer_size, n_layer_size], mean=0.0), dtype=tf.float32)
        b_temp = tf.Variable(tf.random_normal([n_layer_size]), dtype=tf.float32)
        x_temp = tf.sigmoid(tf.matmul(v_activations[i - 1], w_temp) + b_temp)

        v_weights.append(w_temp)
        v_biases.append(b_temp)
        v_activations.append(x_temp)

    w_final = tf.Variable(tf.random_normal([n_layer_size, n_classes], mean=0.0), dtype=tf.float32)
    b_final = tf.Variable(tf.random_normal([n_classes]), dtype=tf.float32)
    y = tf.sigmoid(tf.matmul(v_activations[n_dense_layers - 1], w_final) + b_final)

    ###########################################################################
    # Run Training
    ###########################################################################

    # Training parameters
    f_learning_rate = 0.1

    # Create Training Method
    y_ = tf.placeholder(tf.float32, [None, 1])
    cost_function = tf.reduce_mean(tf.abs(y - y_))
    train_step = tf.train.GradientDescentOptimizer(f_learning_rate).minimize(cost_function)

    # Create Validation Method
    t_pos = tf.logical_and(tf.cast(tf.round(y), tf.bool), tf.cast(y_, tf.bool))
    f_pos = tf.logical_and(tf.cast(tf.round(y), tf.bool), tf.logical_not(tf.cast(y_, tf.bool)))
    t_neg = tf.logical_and(tf.logical_not(tf.cast(tf.round(y), tf.bool)), tf.logical_not(tf.cast(y_, tf.bool)))
    f_neg = tf.logical_and(tf.logical_not(tf.cast(tf.round(y), tf.bool)), tf.cast(y_, tf.bool))

    r_t_pos = tf.reduce_mean(tf.cast(t_pos, tf.float32))
    r_f_pos = tf.reduce_mean(tf.cast(f_pos, tf.float32))
    r_t_neg = tf.reduce_mean(tf.cast(t_neg, tf.float32))
    r_f_neg = tf.reduce_mean(tf.cast(f_neg, tf.float32))

    correct_prediction = tf.equal(tf.round(y), y_)
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Create Session
    sess = tf.InteractiveSession()

    # Run Training
    tf.initialize_all_variables().run()

    t_start = time.time()

    for s in range(n_steps):
        for i in range(n_batches):

            # Get a random batch
            n_batch = rng.randint(0, n_batches - 1)

            batch_xs = x_train[(n_batch * sz_batch):((n_batch + 1) * sz_batch)][:]
            batch_ys = y_train[(n_batch * sz_batch):((n_batch + 1) * sz_batch)]
            sess.run(train_step, feed_dict={x_: batch_xs, y_: batch_ys})

            f_t_pos = sess.run(r_t_pos, feed_dict={x_: x_validate, y_: y_validate})
            f_f_pos = sess.run(r_f_pos, feed_dict={x_: x_validate, y_: y_validate})
            f_t_neg = sess.run(r_t_neg, feed_dict={x_: x_validate, y_: y_validate})
            f_f_neg = sess.run(r_f_neg, feed_dict={x_: x_validate, y_: y_validate})
            f_acc = sess.run(accuracy, feed_dict={x_: x_validate, y_: y_validate})

            print("Iter.: %d; Accuracy: %.3f" % (i, f_acc))
            print("**************************")
            print("    A:1    A:0")
            print("P:1 %.3f  %.3f" % (f_t_pos, f_f_pos))
            print("P:0 %.3f  %.3f" % (f_f_neg, f_t_neg))
            print("**************************")

            if (f_t_pos + f_t_neg) > 0.95:
                break

    t_stop = time.time()
    print("Training time        : " + str(t_stop - t_start))

    ###########################################################################
    # Run Inference
    ###########################################################################

    f_model_accuracy = sess.run(accuracy, feed_dict={x_: x_inference, y_: y_inference})
    print("Inference accuracy   : " + str(f_model_accuracy))


if __name__ == '__main__':

    tf.app.run()