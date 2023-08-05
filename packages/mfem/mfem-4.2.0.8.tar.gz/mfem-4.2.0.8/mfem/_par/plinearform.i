%module(package="mfem._par") plinearform
%{
#include "config/config.hpp"
#include "fem/gridfunc.hpp"
#include "fem/pgridfunc.hpp"  
#include "fem/plinearform.hpp"
#include "numpy/arrayobject.h"
%}

%include "../common/mfem_config.i"

#ifdef MFEM_USE_MPI
%include mpi4py/mpi4py.i
%mpi4py_typemap(Comm, MPI_Comm);
#endif

%init %{
import_array();
%}

%include "exception.i"
%import "linearform.i"
%import "pfespace.i"
%import "pgridfunc.i"
%import "hypre.i"
%import "../common/exception.i"

%newobject mfem::ParLinearForm::ParallelAssemble;
%pointer_class(int, intp);
%include "fem/plinearform.hpp"

