// Copyright (c) 2010-2020, Lawrence Livermore National Security, LLC. Produced
// at the Lawrence Livermore National Laboratory. All Rights reserved. See files
// LICENSE and NOTICE for details. LLNL-CODE-806117.
//
// This file is part of the MFEM library. For more information and source code
// availability visit https://mfem.org.
//
// MFEM is free software; you can redistribute it and/or modify it under the
// terms of the BSD-3 license. We welcome feedback and contributions, see file
// CONTRIBUTING.md for details.

#ifndef MFEM_LIBCEED_HPP
#define MFEM_LIBCEED_HPP

#include "../../config/config.hpp"

#include "../../general/device.hpp"
#include "../../linalg/vector.hpp"
#ifdef MFEM_USE_CEED
#include <ceed.h>
#include <ceed-hash.h>
#endif
#include <tuple>
#include <unordered_map>

namespace mfem
{

class Mesh;
class FiniteElementSpace;
class GridFunction;
class IntegrationRule;
class Coefficient;

#ifdef MFEM_USE_CEED
/// A structure used to pass additional data to f_build_diff and f_apply_diff
struct BuildContext { CeedInt dim, space_dim, vdim; CeedScalar coeff; };

enum class CeedCoeff { Const, Grid, Quad };

struct CeedConstCoeff
{
   double val;
};

struct CeedGridCoeff
{
   const GridFunction* coeff;
   CeedBasis basis;
   CeedElemRestriction restr;
   CeedVector coeffVector;
};

struct CeedQuadCoeff
{
   Vector coeff;
   CeedElemRestriction restr;
   CeedVector coeffVector;
};
#endif

struct CeedData
{
#ifdef MFEM_USE_CEED
   CeedOperator build_oper, oper;
   CeedBasis basis, mesh_basis;
   CeedElemRestriction restr, mesh_restr, restr_i, mesh_restr_i;
   CeedQFunction apply_qfunc, build_qfunc;
   CeedVector node_coords, rho;
   CeedCoeff coeff_type;
   void* coeff;
   CeedQFunctionContext build_ctx;
   BuildContext build_ctx_data;

   CeedVector u, v;

   CeedData()
      : build_oper(nullptr), oper(nullptr), basis(nullptr), mesh_basis(nullptr),
        restr(nullptr), mesh_restr(nullptr), restr_i(nullptr), mesh_restr_i(nullptr),
        apply_qfunc(nullptr), build_qfunc(nullptr), node_coords(nullptr),
        rho(nullptr), coeff(nullptr), build_ctx(nullptr) { }

   ~CeedData()
   {
      CeedOperatorDestroy(&build_oper);
      CeedOperatorDestroy(&oper);
      CeedQFunctionDestroy(&apply_qfunc);
      CeedQFunctionDestroy(&build_qfunc);
      CeedQFunctionContextDestroy(&build_ctx);
      CeedVectorDestroy(&node_coords);
      CeedVectorDestroy(&rho);
      if (coeff_type==CeedCoeff::Const)
      {
         delete static_cast<CeedConstCoeff*>(coeff);
      }
      else if (coeff_type==CeedCoeff::Grid)
      {
         CeedGridCoeff* c = static_cast<CeedGridCoeff*>(coeff);
         CeedVectorDestroy(&c->coeffVector);
         delete c;
      }
      else if (coeff_type==CeedCoeff::Quad)
      {
         CeedQuadCoeff* c = static_cast<CeedQuadCoeff*>(coeff);
         CeedVectorDestroy(&c->coeffVector);
         delete c;
      }
      CeedVectorDestroy(&u);
      CeedVectorDestroy(&v);
   }
#endif
};

/** This structure contains the data to assemble a PA operator with libCEED.
    See libceed/mass.cpp or libceed/diffusion.cpp for examples. */
struct CeedPAOperator
{
#ifdef MFEM_USE_CEED
   /** The finite element space for the trial and test functions. */
   const FiniteElementSpace &fes;
   /** The Integration Rule to use to compute the operator. */
   const IntegrationRule &ir;
   /** The number of quadrature data at each quadrature point. */
   int qdatasize;
   /** The path to the header containing the functions for libCEED. */
   std::string header;
   /** The name of the Qfunction to build the quadrature data with a constant
       coefficient.*/
   std::string const_func;
   /** The Qfunction to build the quadrature data with constant coefficient. */
   CeedQFunctionUser const_qf;
   /** The name of the Qfunction to build the quadrature data with a coefficient
       evaluated at quadrature points. */
   std::string quad_func;
   /** The Qfunction to build the quad. data with a coefficient. */
   CeedQFunctionUser quad_qf;
   /** The name of the Qfunction to apply the operator. */
   std::string apply_func;
   /** The Qfunction to apply the operator. */
   CeedQFunctionUser apply_qf;
   /** The evaluation mode to apply to the trial function (CEED_EVAL_INTERP,
       CEED_EVAL_GRAD, etc.) */
   CeedEvalMode trial_op;
   /** The evaluation mode to apply to the test function ( CEED_EVAL_INTERP,
       CEED_EVAL_GRAD, etc.)*/
   CeedEvalMode test_op;
#endif
};

struct CeedMFOperator
{
#ifdef MFEM_USE_CEED
   /** The finite element space for the trial and test functions. */
   const FiniteElementSpace &fes;
   /** The Integration Rule to use to compote the operator. */
   const IntegrationRule &ir;
   /** The path to the header containing the functions for libCEED. */
   std::string header;
   /** The name of the Qfunction to apply the quadrature data with a constant
       coefficient.*/
   std::string const_func;
   /** The Qfunction to apply the quadrature data with constant coefficient. */
   CeedQFunctionUser const_qf;
   /** The name of the Qfunction to apply the quadrature data with a coefficient
       evaluated at quadrature point. */
   std::string quad_func;
   /** The Qfunction to apply the quad. data with a coefficient evaluated at
       quadrature point. */
   CeedQFunctionUser quad_qf;
   /** The evaluation mode to apply to the trial function (CEED_EVAL_INTERP,
       CEED_EVAL_GRAD, etc.) */
   CeedEvalMode trial_op;
   /** The evaluation mode to apply to the test function ( CEED_EVAL_INTERP,
       CEED_EVAL_GRAD, etc.)*/
   CeedEvalMode test_op;
#endif
};

/** @brief Identifies the type of coefficient of the Integrator to initialize
    accordingly the CeedData. */
void InitCeedCoeff(Coefficient* Q, Mesh &mesh, const IntegrationRule &ir,
                   CeedData* ptr);

/** This function initializes an arbitrary linear operator using the partial
    assembly decomposition in libCEED. The operator details are described by the
    struct CEEDPAOperator input. */
void CeedPAAssemble(const CeedPAOperator& op,
                    CeedData& ceedData);

/** This function initializes an arbitrary linear operator using a fully matrix
    free decomposition. The operator details are described by the
    struct CEEDPAOperator input. */
void CeedMFAssemble(const CeedMFOperator& op,
                    CeedData& ceedData);

/** @brief Function that applies a libCEED operator. */
void CeedAddMult(const CeedData *ceedDataPtr,
                 const Vector &x,
                 Vector &y);

/** @brief Function that assembles a libCEED operator diagonal. */
void CeedAssembleDiagonal(const CeedData *ceedDataPtr,
                          Vector &diag);

/** @brief Function that determines if a CEED kernel should be used, based on
    the current mfem::Device configuration. */
inline bool DeviceCanUseCeed()
{
   return Device::Allows(Backend::CEED_MASK);
}

/** @brief Remove from ceed_basis_map and ceed_restr_map the entries associated
    with the given @a fes. */
void RemoveCeedBasisAndRestriction(const FiniteElementSpace *fes);

#ifdef MFEM_USE_CEED
/// Initialize a CeedVector from a Vector
void InitCeedVector(const Vector &v, CeedVector &cv);

/// Initialize a strided CeedElemRestriction
void InitCeedStridedRestriction(const FiniteElementSpace &fes,
                                CeedInt nelem, CeedInt nqpts, CeedInt qdatasize,
                                const CeedInt *strides,
                                CeedElemRestriction *restr);

/// Initialize a CeedBasis and a CeedElemRestriction
void InitCeedBasisAndRestriction(const FiniteElementSpace &fes,
                                 const IntegrationRule &ir,
                                 Ceed ceed, CeedBasis *basis,
                                 CeedElemRestriction *restr);

/// Return the path to the libCEED q-function headers.
const std::string &GetCeedPath();

// Hash table for CeedBasis
using CeedBasisKey =
   std::tuple<const FiniteElementSpace*, const IntegrationRule*, int, int, int>;
struct CeedBasisHash
{
   std::size_t operator()(const CeedBasisKey& k) const
   {
      return CeedHashCombine(
                CeedHashCombine(
                   CeedHashInt(reinterpret_cast<CeedHash64_t>(std::get<0>(k))),
                   CeedHashInt(reinterpret_cast<CeedHash64_t>(std::get<1>(k)))),
                CeedHashCombine(
                   CeedHashCombine(CeedHashInt(std::get<2>(k)),
                                   CeedHashInt(std::get<3>(k))),
                   CeedHashInt(std::get<4>(k))));
   }
};
using CeedBasisMap =
   std::unordered_map<const CeedBasisKey, CeedBasis, CeedBasisHash>;

// Hash table for CeedElemRestriction
using CeedRestrKey = std::tuple<const FiniteElementSpace*, int, int, int>;
struct CeedRestrHash
{
   std::size_t operator()(const CeedRestrKey& k) const
   {
      return CeedHashCombine(
                CeedHashCombine(
                   CeedHashInt(reinterpret_cast<CeedHash64_t>(std::get<0>(k))),
                   CeedHashInt(std::get<1>(k))),
                CeedHashCombine(CeedHashInt(std::get<2>(k)),
                                CeedHashInt(std::get<3>(k))));
   }
};
using CeedRestrMap =
   std::unordered_map<const CeedRestrKey, CeedElemRestriction, CeedRestrHash>;

namespace internal
{
extern Ceed ceed; // defined in device.cpp
extern CeedBasisMap basis_map;
extern CeedRestrMap restr_map;
}

#endif // MFEM_USE_CEED

} // namespace mfem

#endif // MFEM_LIBCEED_HPP
