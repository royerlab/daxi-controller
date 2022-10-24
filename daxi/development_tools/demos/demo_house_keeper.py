import daxi.development_tools.house_keeper as hk
import pptree
import os

# clean the tree first (housekeeping)
org0 = os.path.join('C:\\',
                    'Users',
                    'PiscesScope',
                    'xiyu_workbench',
                    'daxi-protocol',
                    'daxi')

org1 = os.path.join('C:\\',
                    'Users',
                    'PiscesScope',
                    'xiyu_workbench',
                    'daxi-protocol',
                    )

hk.pytmdaxi(option='clean', rootdir=org0, VERBOSE=True, fname_substr='scratch')

hk.pytmdaxi(option='clean', rootdir=org1, VERBOSE=True, fname_substr='scratch')

tree = hk.get_folders_Tree(path=org0,
                           VERBOSE=False,
                           origin_name='daxi_organized')

pptree.print_tree(tree)
