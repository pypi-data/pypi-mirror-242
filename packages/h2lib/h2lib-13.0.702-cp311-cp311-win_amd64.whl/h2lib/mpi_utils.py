from h2lib._h2lib import H2LibThread, H2LibProcess
import numpy as np
import sys
import os
import subprocess

if 'SLURM_NTASKS' in os.environ:
    mpi = int(os.environ['SLURM_NTASKS']) > 1
elif any([k in os.environ for k in ['MPI_LOCALNRANKS', 'OMPI_COMM_WORLD_SIZE']]):
    mpi = True
else:
    mpi = subprocess.run("python -c 'from mpi4py import MPI'", shell=True,
                         check=False, stderr=subprocess.PIPE).returncode == 0

if mpi:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    size = MPI.COMM_WORLD.Get_size()
    rank = MPI.COMM_WORLD.Get_rank()
    name = MPI.Get_processor_name()
else:
    size = 1

MPIClassInterfaceAttributes = {'close', 'use_rank', 'cls', 'do_work', 'object', '__class__'}
exit_mpi_on_close = True


class MPIClassInterface():
    def __init__(self, cls, args_lst):
        if len(args_lst) > size:
            if rank == 0:
                raise Exception(f"Not enough mpi slots. Slots: {size}, Requested: {len(args_lst)}")
            return
        self.cls = cls
        if rank < len(args_lst):
            self.object = cls(*args_lst[rank])
        else:
            class Dummy():
                def close(self):
                    pass
            self.object = Dummy()

        if rank == 0:
            self.use_rank = np.array([True] * size)
            self.use_rank[len(args_lst):] = False
        else:
            self.do_work()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def do_work(self):
        # print (rank, name, 'start work')
        while True:
            method, args, kwargs = comm.scatter(None)
            # print (rank, 'do work', method, args, kwargs)
            if method == 'skip':
                res = None
            else:
                res = getattr(self.object, method)

            if hasattr(res, '__call__'):
                res = res(*args, **kwargs)
            # print (method, args, kwargs, res)
            comm.gather(res)
            if method == 'close':
                if exit_mpi_on_close:
                    comm.gather(f'Exit, rank {rank}')
                    sys.exit(0)
                else:
                    raise ChildProcessError('MPI worker done')

    def __getattribute__(self, name):
        if rank > 0:
            return object.__getattribute__(self, name)
        if name in MPIClassInterfaceAttributes:
            return object.__getattribute__(self, name)

        use_rank = self.use_rank
        N = np.sum(use_rank)

        def wrap(*args, **kwargs):
            def get_input(i):
                if use_rank[i]:
                    def get_arg(arg):
                        if isinstance(arg, list) and len(arg) == N:
                            return arg[np.where(use_rank)[0][i]]
                        else:
                            return arg
                    return (name, [get_arg(arg) for arg in args], {k: get_arg(v) for k, v in kwargs.items()})
                else:
                    return ('skip', [], {})
            inp = [get_input(i) for i in range(size)]
            comm.scatter(inp, root=0)
            if rank == 0:
                method, args, kwargs = inp[0]
                # print (rank, 'do work', method, args, kwargs)
                if method == 'skip':
                    res = None
                else:
                    res = getattr(self.object, method)

                if hasattr(res, '__call__'):
                    res = res(*args, **kwargs)

                # print (method, args, kwargs, res)
            else:
                res = None

            res = [res for i, res in enumerate(comm.gather(res, root=0)) if use_rank[i]]
            if isinstance(self, SubsetMPIClassInterface) and len(res) == 1:
                return res[0]
            return res
        if hasattr(getattr(self.cls, name), '__call__'):
            return wrap
        else:
            return wrap()

    def __getitem__(self, slice):
        use_rank = np.full_like(self.use_rank, False)
        use_rank[slice] = True
        return SubsetMPIClassInterface(self.cls, self.object, use_rank)

    def close(self):
        comm.scatter([('close', [], {}) for _ in range(size)], root=0)
        (comm.gather(self.object.close(), root=0))
        if exit_mpi_on_close:
            (comm.gather(f'Exit, rank {rank}', root=0))


class SubsetMPIClassInterface(MPIClassInterface):
    def __init__(self, cls, object, use_rank):
        self.use_rank = use_rank
        self.cls = cls
        self.object = object

    def __getitem__(self, slice):
        raise Exception('Cannot make subset of SubsetMPIClassInterface')

    def close(self):
        raise Exception('Cannot close SubsetMPIClassInterface. Please close all instances at once')
