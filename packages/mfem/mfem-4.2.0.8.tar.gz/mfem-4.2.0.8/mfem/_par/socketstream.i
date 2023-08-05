%module(package="mfem._par") socketstream
%feature("autodoc", "1");

%{
#include <iostream>
#include "io_stream.hpp"      
#include "mesh/mesh_headers.hpp"
#include "fem/gridfunc.hpp"  
#include "general/socketstream.hpp"
#include "numpy/arrayobject.h"  
%}

%init %{
import_array();
%}
//%rename(sopen)  open(const char hostname[], int port);
%include "exception.i"
 //%include "../common/cpointers.i"
 //%import "cpointers.i"
%import "mesh.i"
%import "gridfunc.i"
%import "../common/exception.i"

%include "general/socketstream.hpp"

%extend mfem::socketstream{
  int precision(const int p)
   {
     return self->precision(p);     
   }
  int precision()
   { 
     return self->precision();
   }
  void send_solution(const mfem::Mesh &mesh,
 				    const mfem::GridFunction &gf) 
   {
     *self << "solution\n" << mesh << gf << std::flush;
   }
  void send_text(const char ostr[])
   { 
      *self << ostr << std::endl;
   }
  void flush()
   { 
     self->flush();
   }
  
  mfem::socketstream& __lshift__(const char ostr[])
   { 
      *self << ostr;
      return *self;
   }
  mfem::socketstream& __lshift__(const int x)
   { 
      *self << x;
      return *self;
   }
  mfem::socketstream& __lshift__(const mfem::Mesh &mesh)
   { 
      *self << mesh;
      return *self;
   }
  mfem::socketstream& __lshift__(const mfem::GridFunction &gf)
   { 
      *self << gf;
      return *self;
   }
  mfem::socketstream& endline()
   {
     *self << std::endl;
     return *self;
   } 
} 
