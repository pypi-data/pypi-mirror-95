%module (package="mfem._ser", directors="1") operators

%feature("autodoc", "1");

%{
#include <fstream>
#include <iostream>  
  
#include "io_stream.hpp"        
#include "pyoperator.hpp"
#include "numpy/arrayobject.h"
#include "linalg/operator.hpp"  
%}

%init %{
import_array();
%}
%include "exception.i"
%import "mem_manager.i"
%import "vector.i"
%import "array.i"
%import "../common/exception_director.i"

%import "../common/io_stream_typemap.i"
OSTREAM_TYPEMAP(std::ostream&)

/*
%feature("director:except") {
    if ($error != NULL) {
        throw Swig::DirectorMethodException();
    }
}
*/

%inline %{
void mfem::PyOperatorBase::Mult(const mfem::Vector &x, mfem::Vector &y) const
  {
    y = _EvalMult(x);
  }
void mfem::PyTimeDependentOperatorBase::Mult(const mfem::Vector &x, mfem::Vector &y) const
  {
    y = _EvalMult(x);
  }
%}

%feature("director") mfem::PyTimeDependentOperatorBase;
%feature("director") mfem::PyOperatorBase;
//%feature("noabstract") mfem::Operator;
//%feature("noabstract") mfem::TimeDependentOperator;
%feature("director") mfem::TimeDependentOperator;
%feature("director") mfem::Operator;
%feature("director") mfem::Solver;

//%feature("nodirector") mfem::Operator::GetGradient;
//%feature("nodirector") mfem::Operator::GetProlongation;
//%feature("nodirector") mfem::Operator::GetRestriction;
//%feature("nodirector") mfem::TimeDependentOperator::GetImplicitGradient;
//%feature("nodirector") mfem::TimeDependentOperator::GetExplicitGradient;

%include "linalg/operator.hpp"
%include "pyoperator.hpp"

%pythoncode %{
class PyOperator(PyOperatorBase):
   def __init__(self, *args):
       PyOperatorBase.__init__(self, *args)
   def _EvalMult(self, x):
       return self.EvalMult(x.GetDataArray())
   def EvalMult(self, x):
       raise NotImplementedError('you must specify this method')

class PyTimeDependentOperator(PyTimeDependentOperatorBase):
   def __init__(self, *args):  
       PyTimeDependentOperatorBase.__init__(self, *args)
   def _EvalMult(self, x):
       return self.EvalMult(x.GetDataArray())
   def EvalMult(self, x):
       raise NotImplementedError('you must specify this method')
			 
%}
  
/*
  void PrintMatlab(std::ostream & out, int n = 0, int m = 0) const;
*/
#ifndef SWIGIMPORTED
OSTREAM_ADD_DEFAULT_FILE(Operator, PrintMatlab)
#endif
