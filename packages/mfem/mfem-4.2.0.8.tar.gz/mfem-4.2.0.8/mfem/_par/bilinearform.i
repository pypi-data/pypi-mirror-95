%module(package="mfem._par", directors="1")  bilinearform
%{
#include "fem/bilinearform.hpp"
#include "numpy/arrayobject.h"
#include "pyoperator.hpp"           
%}

%init %{
import_array();
%}
%include "exception.i"
 //%import "cpointers.i"

%import "globals.i"
%import "array.i"
%import "mem_manager.i"

%import "fespace.i"
%import "fe_coll.i"
%import "intrules.i"
%import "matrix.i"
%import "vector.i"
%import "densemat.i"
%import "sparsemat.i"
%import "lininteg.i"
%import "eltrans.i"
%import "bilininteg.i"
%import "linearform.i"
%import "gridfunc.i"
%include "../common/exception_director.i"

%pointer_class(int, intp);

%ignore mfem::MixedBilinearForm::AddBoundaryDomainIntegrator;
%feature("director") mfem::BilinearForm;

namespace mfem { 
%pythonprepend BilinearForm::AddDomainIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(bfi)
    bfi.thisown=0 
   %}
%pythonprepend BilinearForm::AddBoundaryIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    bfi = args[0]	     	     
    self._integrators.append(bfi)
    bfi.thisown=0 
   %} 
%pythonprepend BilinearForm::AddBdrFaceIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    bfi = args[0]
    self._integrators.append(bfi)
    bfi.thisown=0 
   %} 
%pythonprepend BilinearForm::AddInteriorFaceIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(bfi)
    bfi.thisown=0 
   %}
%pythonappend BilinearForm::SpMat %{
    if not hasattr(self, "_spmat"): self._spmat = []
    self._spmat.append(val)
    val.thisown=0 
   %}
%pythonappend BilinearForm::EnableHybridization %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(constr_integ)
    constr_integ.thisown = 0
   %} 
%pythonprepend MixedBilinearForm::AddDomainIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(bfi)
    bfi.thisown=0 
   %}
%pythonprepend MixedBilinearForm::AddBoundaryIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(bfi)
    bfi.thisown=0 
   %} 
%pythonprepend MixedBilinearForm::AddTraceFaceIntegrator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(bfi)
    bfi.thisown=0 
   %} 
%pythonappend MixedBilinearForm::SpMat %{
    if not hasattr(self, "_spmat"): self._spmat = []
    self._spmat.append(val)
    val.thisown=0 
   %}

%pythonprepend DiscreteLinearOperator::AddDomainInterpolator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(di)
    di.thisown=0 
   %} 
%pythonprepend DiscreteLinearOperator::AddTraceFaceInterpolator %{
    if not hasattr(self, "_integrators"): self._integrators = []
    self._integrators.append(di)
    di.thisown=0 
   %}
  
} //end of namespace

%include "fem/bilinearform.hpp"

// instatitate template methods 
%define FORM_SYSTEM_MATRIX_WRAP(OsType)
%template(FormLinearSystem) mfem::BilinearForm::FormLinearSystem<OsType>;
%template(FormSystemMatrix) mfem::BilinearForm::FormSystemMatrix<OsType>;
%enddef

FORM_SYSTEM_MATRIX_WRAP(mfem::SparseMatrix)
  
#ifdef MFEM_USE_MPI
  FORM_SYSTEM_MATRIX_WRAP(mfem::HypreParMatrix)
#endif
  
#ifdef MFEM_USE_PETSC
  FORM_SYSTEM_MATRIX_WRAP(mfem::PetscParMatrix)
#endif  

