%module(package="mfem._ser", directors="1")  linearform
%{
#include "fem/fem.hpp"
#include "fem/fe_coll.hpp"
#include "fem/fespace.hpp"
#include "fem/eltrans.hpp"
#include "fem/coefficient.hpp"
#include "fem/linearform.hpp"  
#include "fem/intrules.hpp"  
#include <iostream>
#include <sstream>
#include <fstream>
#include <limits>
#include <cmath>
#include <cstring>
#include <ctime>
#include "numpy/arrayobject.h"
#include "pyoperator.hpp"         
%}

%init %{
import_array();
%}

%include "exception.i"
%include "../common/cpointers.i"
%import "coefficient.i"
%import "array.i"
%import "mesh.i"
%import "intrules.i"
%import "fe.i"
%import "fe_coll.i"
%import "densemat.i"
%import "sparsemat.i"
%import "vector.i"
%import "eltrans.i"
%import "lininteg.i"
%include "../common/exception_director.i"
 //%import "fem/fespace.hpp

 //%include "fem/coefficient.hpp"
namespace mfem { 
%pythonprepend LinearForm::AddDomainIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(lfi)
    lfi.thisown=0 
   %}
%pythonprepend LinearForm::AddBoundaryIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    lfi = args[0]	     
    self._integrators.append(lfi)
    lfi.thisown=0
   %} 
%pythonprepend LinearForm::AddBdrFaceIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    lfi = args[0]
    self._integrators.append(lfi)
    lfi.thisown=0 
   %}    
}

%include "../common/deprecation.i"
DEPRECATED_METHOD(mfem::LinearForm::GetFES())

%include "fem/linearform.hpp"


