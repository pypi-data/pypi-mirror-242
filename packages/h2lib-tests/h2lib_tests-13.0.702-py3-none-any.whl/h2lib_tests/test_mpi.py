import os
import time
from numpy import testing as npt
import pytest

import h2lib
from h2lib._h2lib import H2LibThread, H2LibProcess, MultiH2Lib
from h2lib.my_test_cls import MyTest
from h2lib.utils import ProcessClass, MultiProcessInterface
import numpy as np
from h2lib import mpi_utils
from h2lib_tests.test_files import tfp


def mpitest_mpi_MyTest():
    from h2lib.mpi_utils import MPIClassInterface

    N = 4
    try:
        with MPIClassInterface(MyTest, [(i,) for i in range(N)]) as m:

            time.sleep(.1)
            i = m.get_id()
            npt.assert_array_equal(i, np.arange(N))

            npt.assert_array_equal(m[1:3].get_id(), np.arange(1, 3))
            t = time.time()
            m.work(1)
            t = time.time() - t
            assert t < 1.1

            with pytest.raises(Exception, match='Cannot close SubsetMPIClassInterface. Please close all instances at once'):
                m[:3].close()
            with pytest.raises(Exception, match='Cannot make subset of SubsetMPIClassInterface'):
                m[:3][1]

            print("done, test_mpi_MyTest")
    except ChildProcessError:
        pass


def mpitest_mpi_ProcessClass():

    with ProcessClass(MyTest) as cls:
        myTest = cls(1)
        assert myTest.get_id() == 1
    print("done, test_mpi_ProcessClass")


def mpitest_mpi_H2LibProcess():
    with H2LibProcess(suppress_output=False) as h2:
        assert h2lib.__version__.replace("+", "-").startswith(h2.get_version().strip()
                                                              ), (h2.get_version().strip(), h2lib.__version__)
    print("done, test_mpi_H2LibProcess")


def mpitest_MultiH2Lib():
    with MultiH2Lib(3) as mh2:
        assert all([h2lib.__version__.replace("+", "-").startswith(v.strip()) for v in mh2.get_version()])
        assert len(mh2.get_version()) == 3
        if mpi_utils.size > 1:
            assert isinstance(mh2, mpi_utils.MPIClassInterface)
            _file__ = np.__file__
            if '/lib/' in _file__:
                lib_path = _file__[:_file__.index("/lib/") + 5]
            else:
                lib_path = "LibNotInLD_LIBRARY_PATH"
            if lib_path in os.environ.get('LD_LIBRARY_PATH', '') or os.path.relpath(
                    lib_path, os.getcwd()) in os.environ.get('LD_LIBRARY_PATH', ''):
                # assert mh2.cls == H2LibThread, mh2.cls
                assert mh2.cls == H2LibProcess, mh2.cls
            else:
                assert mh2.cls == H2LibProcess, mh2.cls
        else:
            assert isinstance(mh2, MultiProcessInterface)

        model_path = tfp + "minimal/"
        mh2.read_input('htc/minimal.htc', model_path)
        npt.assert_array_equal(mh2.model_path, [model_path] * 3)
        mh2.init_windfield(Nxyz=(128, 32, 16), dxyz=[(1, 2, 3), (4, 5, 6), (7, 8, 9)],
                           box_offset_yz=[0, 0], transport_speed=5)
        assert mh2.getState() == [0, 0, 0]
        mh2.setState([4, 5, 6])
        assert mh2.getState() == [4, 5, 6], mh2.getState()
        mh2[0].setState(10)
        assert mh2.getState() == [10, 5, 6]
        t = time.time()
        mh2.work(2)
        assert time.time() - t < 2.5
        with pytest.raises(Exception, match='Cannot close SubsetMPIClassInterface. Please close all instances at once'):
            mh2[:3].close()
        with pytest.raises(Exception, match='Cannot make subset of SubsetMPIClassInterface'):
            print(mh2[:3][1].getState())
        print('done, test_MPIH2Lib')


def mpitest_all():
    mpi_utils.exit_mpi_on_close = False
    from mpi4py import MPI
    rank = MPI.COMM_WORLD.Get_rank()
    from h2lib_tests.test_ellipsys_couplings import test_ellipsys_dummy_workflow
    from h2lib_tests.test_h2lib import test_parallel_context_manager, test_parallel
    from h2lib_tests.test_h2rotor import test_rotor_orientation_multi_instance

    for f in [mpitest_mpi_MyTest, mpitest_mpi_ProcessClass, mpitest_mpi_H2LibProcess,
              mpitest_MultiH2Lib,
              test_parallel, test_parallel_context_manager, test_ellipsys_dummy_workflow,
              test_rotor_orientation_multi_instance]:
        try:
            if rank == 0:
                print(f"Rank {rank} start {f.__name__}", flush=True)
            f()
        except ChildProcessError:
            pass
        finally:
            if rank == 0:
                print(f"Rank {rank} done {f.__name__}", flush=True)
    print(f"Rank {rank} Done test_all")
