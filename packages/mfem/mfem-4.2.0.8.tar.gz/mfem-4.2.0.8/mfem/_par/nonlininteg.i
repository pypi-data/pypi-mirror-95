%module(package="mfem._par", directors="1") nonlininteg
%{
#include "fem/nonlininteg.hpp"
#include "fem/linearform.hpp"      
#include "pycoefficient.hpp"
#include "pyoperator.hpp"               
%}
/*
%init %{
import_array();
%}
*/

%exception {
    try { $action }
    catch (Swig::DirectorException &e) { SWIG_fail; }    
    //catch (...){
    //  SWIG_fail;
    //}
    //    catch (Swig::DirectorMethodException &e) { SWIG_fail; }
    //    catch (std::exception &e) { SWIG_fail; }    
}
%feature("director:except") {
    if ($error != NULL) {
        throw Swig::DirectorMethodException();
    }
}

%import vector.i
%import operators.i
%import fespace.i
%import eltrans.i

%feature("director") mfem::NonlinearFormIntegrator;

%include "fem/nonlininteg.hpp"
