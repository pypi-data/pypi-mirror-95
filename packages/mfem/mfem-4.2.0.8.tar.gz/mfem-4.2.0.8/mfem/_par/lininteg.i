%module(package="mfem._par", directors="1")  lininteg
%{
#include "fem/lininteg.hpp"  
#include <iostream>
#include <sstream>
#include <fstream>
#include <limits>
#include <cmath>
#include <cstring>
#include <ctime>
#include "pycoefficient.hpp"
#include "numpy/arrayobject.h"        
%}

%init %{
import_array();
%}

 //%include "fem/coefficient.hpp"
%import "fe.i"
%import "vector.i"
%import "eltrans.i"
%import "intrules.i"
%import "coefficient.i"


%exception {
    try { $action }
    catch (Swig::DirectorException &e) { SWIG_fail; }    
    //catch (...){
    //  SWIG_fail;
    //}
    //    catch (Swig::DirectorMethodException &e) { SWIG_fail; }
    //    catch (std::exception &e) { SWIG_fail; }    
}

%include "../common/lininteg_ext.i"

%include "fem/lininteg.hpp"


