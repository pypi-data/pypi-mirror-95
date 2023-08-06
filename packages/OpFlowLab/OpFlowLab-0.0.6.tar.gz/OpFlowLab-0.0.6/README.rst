================================
OpFlowLab
================================

OpFLowLab is a user-friendly motion estimation framework that seeks to help cell biologist try out optical flow algorithms on their own dataset.

Key Features
------------
- Graphical interface to assess CUDA optimized optical flow algorithms provided by OpenCV
- Post processing of velocities using FlowMatch, an object matching routine.
- Velocity field validation using artificial tracers and image warping
- Visualization of velocity pattern using pathlines
- Calculation of velocity field derivatives

Installing
----------
OpFLowLab can be installed with pip::

    $ python -m pip install OpFLowLab

Alternatively, the latest source code is available from GitLab::

    $ git clone git@gitlab.com:xianbin.yong13/OpFlowLab.git
    $ python setup.py install

Graphical user interface
------------------------
To start OpFlowLab::

    $ opflowlab

Documentation
-------------
Documentation for OpFlowLab can be found at https://opflowlab.readthedocs.io/en/latest/.

How to cite
-----------
If you use OpFlowLab, we would appreciate if you could cite the following paper:

License
--------
OpFlowLab is provided under the GPLv3 license.