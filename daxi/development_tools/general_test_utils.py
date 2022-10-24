import pytest
import os
import inspect
from deepdiff import DeepDiff


def sys_msg(msg='', verbose=True):
    """
    display system output messages based on a verbose option
    Parameters
    ----------
    msg
    verbose: option to display the message.

    Returns
    -------

    """
    if verbose:
        os.system(msg)


def extract_object_members(obj=None):
    """
    This function extracts the members of the obj.
    Parameters
    ----------
    obj: object of an arbitrary class.

    Returns
    -------

    """
    # first extract all the attributes of the object
    obj_mbr = {}
    for member in inspect.getmembers(obj):
        if not member[0].startswith('_'):
            if inspect.ismethod(member[1]):
                obj_mbr[member[0]] = 'method'
            if not inspect.ismethod(member[1]):
                obj_mbr[member[0]] = 'attribute'

    return obj_mbr


def compare_object_structure(verbose=True, obj=None, obj_mbr_std=None):
    """
    This function compares the structure of the object "obj" to
    a standard "obj_mbr_std".
    It will go through all the memberes of the obj, and check if
    this member matches with the standard provided by the obj_mbr_std

    if there is a mismatch, this funciton will print out the
    missing/extra members, and whether they are methods or attributes.

    Parameters
    ----------
    verbose: option for output messages.
    obj: object of arbitrary class.
    obj_mbr_std: dictionary of the object members we want to compare to.

    Returns
    -------
    True or False.

    """
    # first, extract the object members from the input object.
    sys_msg(msg='extract object members ...', verbose=verbose)
    obj_mbr = extract_object_members(obj=obj)

    sys_msg(msg='now compare object members ...', verbose=verbose)
    diff = DeepDiff(obj_mbr_std, obj_mbr)

    return diff
