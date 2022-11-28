import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def vis():

    # NOTE:
    # Directly below is the calculations for counts of training
    #  and test sets. I just directly input the values to a list
    #  but you could un-comment and replace the dataframes below
    #  with the training and tests sets if you wish.

    # -------------------------------------
    # training = pd.read_csv('comments_kanye.csv')
    # test = pd.read_csv('comments_askScience.csv')
    #
    # # Get 0 and 1 count of training set
    # training_one = training['mod_deleted'].sum()
    # training_zero = len(training) - training_one
    #
    # # Get 0 and 1 count of test set
    # test_one = test['mod_deleted'].sum()
    # test_zero = len(test) - test_one
    # --------------------------------------

    # NOTE:
    # Below are values for subreddit-specific train and test
    #  set mod_deleted counts
    #  It follows this format:
    #  zero = [training_0_count, test_0_count]
    #  one = [training_1_count, test_1_count]

    # KANYE
    # # training and test set zero count
    # zero = [28899, 10611]
    # # training and test set one count
    # one = [466, 384]

    # SCIENCE
    # # training and test set zero count
    # zero = [3416, 1705]
    # # training and test set one count
    # one = [809, 721]

    # POLITICAL
    # # training and test set zero count
    # zero = [16739, 10353]
    # # training and test set one count
    # one = [559, 277]

    # SOCIALISM
    # training and test set zero count
    zero = [1524, 859]
    # training and test set one count
    one = [141, 87]

    labels = ['Training set', 'Test set']   # labels for x-ticks
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, zero, width, label='not deleted')
    rects2 = ax.bar(x + width / 2, one, width, label='deleted')

    # Formatting
    ax.set_ylabel('Count')
    ax.set_title('r/socialism mod_deleted')
    ax.legend()
    plt.xticks(x, labels)
    fig.tight_layout()

    plt.show()
    return

def main():
    vis()
    plt.show()


if __name__ == '__main__':
    main()
