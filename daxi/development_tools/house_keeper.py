# TODO transfer the function of this house keeper from the bash scripts into python

import os
import shutil
import pptree


def pytmdaxi(option='clean', rootdir='.', VERBOSE=True, fname_substr='scratch'):
    # todo add documentation of this function, add to examples, add to tm.daxi for the task monitor scripts.
    # this function will clean all the files that has the file name matches with the patterns, and the folders that has
    # a substring that matches with any of the the pattern.
    if VERBOSE:
        print("pytmdaxi -  clean the repositories...\n")
    paths = []
    files = []
    if option == 'clean':
        patterns= ['.DS_Store',
                   '.idea',
                   '__pycache__',
                   '*.pyc',
                   '.ipynb_checkpoints',
                   'pycache',
                   '.pytest_cache']
        if VERBOSE:
            print('patterns to be cleaned:')
            print(patterns)
            print("")

    if option == 'fname_substr':
        patterns = [fname_substr]
        if VERBOSE:
            print('patterns to be cleaned:')
            print(patterns)
            print("")

    if VERBOSE:
        print('rootdir is:')
        print(rootdir + '\n')

    for root, ds, fs in os.walk(rootdir):
        for pattern in patterns:

            for item in ds:
                # the file paths will be cleaned as long as it contains a
                # substring that equals to the pattern sctring.
                if pattern in item:
                    target = os.path.join(root, item)
                    paths.append(target)
                    if VERBOSE:
                        print(target)

            for item in fs:
                # the filename has to match with the pattern string exactly
                if item == pattern:
                    target = os.path.join(root, item)
                    files.append(target)
                    if VERBOSE:
                        print(target)
    if VERBOSE:
        print('removing the following files and paths:')

    for p in paths:
        if os.path.isdir(p):
            shutil.rmtree(p)

        if VERBOSE:
            print('removing' + p)

    for f in files:
        os.remove(f)
        if VERBOSE:
            print('removing' + f)

    if VERBOSE:
        print('cleaning completed.')
        print('')


def printer_folders_tree():
    """

    :return:

    """
    shame = pptree.Node("shame")

    conscience = pptree.Node("conscience", shame)
    selfdisgust = pptree.Node("selfdisgust", shame)
    embarrassment = pptree.Node("embarrassment", shame)

    selfconsciousness = pptree.Node("selfconsciousness", embarrassment)
    shamefacedness = pptree.Node("shamefacedness", embarrassment)
    chagrin = pptree.Node("chagrin", embarrassment)
    discomfiture = pptree.Node("discomfiture", embarrassment)
    abashment = pptree.Node("abashment", embarrassment)
    confusion = pptree.Node("confusion", embarrassment)

    pptree.print_tree(shame)
    return 0


def get_folders_tree(path='..', VERBOSE=False, origin_name='Current'):
    print('current directory: '+path)
    origin_node=pptree.Node(origin_name)

    p1nodes = []
    p2nodes = []
    p3nodes = []
    p4nodes = []

    p1_node_i = 0
    p2_node_i = 0
    p3_node_i = 0
    p4_node_i = 0

    paths1 = [x1 for x1 in os.listdir(path) if os.path.isdir(os.path.join(path, x1))]
    ml1 = max([len(l) for l in paths1])  # maximum lenghth of the filename

    if VERBOSE:
        print('len(paths1)= ' + str(len(paths1)))

    for p1 in paths1:
        if VERBOSE:
            print('current p1 is ' + p1)
        p1nodes.append(pptree.Node(p1, origin_node))

        curpathp1 = os.path.join(path, p1)
        if VERBOSE:
            print('inside p1 loop, current path is '+curpathp1)

        paths2 = [x2 for x2 in os.listdir(curpathp1) if os.path.isdir(os.path.join(curpathp1, x2))]
        if len(paths2)>0:
            ml2 = max([len(l) for l in paths2])  # maximum lenghth of the filename

        if VERBOSE:
            print("len(paths2) is "+str(len(paths2)))

        for p2 in paths2:
            if VERBOSE:
                print('current p2 is ' + p2)

            p2nodes.append(pptree.Node(p2, p1nodes[p1_node_i]))

            curpathp2 = os.path.join(curpathp1, p2)
            if VERBOSE:
                print('inside p2 loop, current path is ' + curpathp2)

            paths3 = [x3 for x3 in os.listdir(curpathp2) if os.path.isdir(os.path.join(curpathp2, x3))]
            if VERBOSE:
                print("len(paths3) is " + str(len(paths3)))

            for p3 in paths3:
                p3nodes.append(pptree.Node(p3, p2nodes[p2_node_i]))
                curpathp3 = os.path.join(curpathp2, p3)
                if VERBOSE:
                    print('inside p3 loop, current path is ' + curpathp3)
                paths4 = [x4 for x4 in os.listdir(curpathp3) if os.path.isdir(os.path.join(curpathp3, x4))]
                if VERBOSE:
                    print("len(paths4) is " + str(len(paths4)))

                for p4 in paths4:
                    p4nodes.append(pptree.Node(p4, p3nodes[p3_node_i]))
                    curpathp4 = os.path.join(curpathp3, p4)
                    if VERBOSE:
                        print('inside p4 loop, current path is ' + curpathp4)

                    paths5 = [x5 for x5 in os.listdir(curpathp4) if os.path.isdir(os.path.join(curpathp4, x5))]
                    for p5 in paths5:
                        pptree.Node(p5, p4nodes[p4_node_i])
                    p4_node_i+=1
                p3_node_i+=1
            p2_node_i+=1
        p1_node_i+=1

    return origin_node


def replace_files(fname_ori, fname_end, verbose = True, rootdir='..', option='check'):
    files = []
    # file all the files to be changed:
    for root, ds, fs in os.walk(rootdir):
        for item in fs:
            # loop over all files
            if item == fname_ori:
                target = [os.path.join(root, fname_ori),os.path.join(root, fname_end)]
                files.append(target)

    # change all the files
    if option == 'execute':
        print('now performing the file renaming action:')
        for f in files:
            os.rename(f[0], f[1])
    else:
        print('no file is changed.')

    if verbose:
        print('list of files to be changed')
        for f in files:
            print(f[0] + ', change to:  ' + f[1])
