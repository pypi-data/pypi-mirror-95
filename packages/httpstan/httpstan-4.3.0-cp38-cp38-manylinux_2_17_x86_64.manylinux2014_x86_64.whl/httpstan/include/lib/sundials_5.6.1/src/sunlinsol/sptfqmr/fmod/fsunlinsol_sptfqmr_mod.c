/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 4.0.0
 *
 * This file is not intended to be easily readable and contains a number of
 * coding conventions designed to improve portability and efficiency. Do not make
 * changes to this file unless you know what you are doing--modify the SWIG
 * interface file instead.
 * ----------------------------------------------------------------------------- */

/* ---------------------------------------------------------------
 * Programmer(s): Auto-generated by swig.
 * ---------------------------------------------------------------
 * SUNDIALS Copyright Start
 * Copyright (c) 2002-2020, Lawrence Livermore National Security
 * and Southern Methodist University.
 * All rights reserved.
 *
 * See the top-level LICENSE and NOTICE files for details.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 * SUNDIALS Copyright End
 * -------------------------------------------------------------*/

/* -----------------------------------------------------------------------------
 *  This section contains generic SWIG labels for method/variable
 *  declarations/attributes, and other compiler dependent labels.
 * ----------------------------------------------------------------------------- */

/* template workaround for compilers that cannot correctly implement the C++ standard */
#ifndef SWIGTEMPLATEDISAMBIGUATOR
# if defined(__SUNPRO_CC) && (__SUNPRO_CC <= 0x560)
#  define SWIGTEMPLATEDISAMBIGUATOR template
# elif defined(__HP_aCC)
/* Needed even with `aCC -AA' when `aCC -V' reports HP ANSI C++ B3910B A.03.55 */
/* If we find a maximum version that requires this, the test would be __HP_aCC <= 35500 for A.03.55 */
#  define SWIGTEMPLATEDISAMBIGUATOR template
# else
#  define SWIGTEMPLATEDISAMBIGUATOR
# endif
#endif

/* inline attribute */
#ifndef SWIGINLINE
# if defined(__cplusplus) || (defined(__GNUC__) && !defined(__STRICT_ANSI__))
#   define SWIGINLINE inline
# else
#   define SWIGINLINE
# endif
#endif

/* attribute recognised by some compilers to avoid 'unused' warnings */
#ifndef SWIGUNUSED
# if defined(__GNUC__)
#   if !(defined(__cplusplus)) || (__GNUC__ > 3 || (__GNUC__ == 3 && __GNUC_MINOR__ >= 4))
#     define SWIGUNUSED __attribute__ ((__unused__))
#   else
#     define SWIGUNUSED
#   endif
# elif defined(__ICC)
#   define SWIGUNUSED __attribute__ ((__unused__))
# else
#   define SWIGUNUSED
# endif
#endif

#ifndef SWIG_MSC_UNSUPPRESS_4505
# if defined(_MSC_VER)
#   pragma warning(disable : 4505) /* unreferenced local function has been removed */
# endif
#endif

#ifndef SWIGUNUSEDPARM
# ifdef __cplusplus
#   define SWIGUNUSEDPARM(p)
# else
#   define SWIGUNUSEDPARM(p) p SWIGUNUSED
# endif
#endif

/* internal SWIG method */
#ifndef SWIGINTERN
# define SWIGINTERN static SWIGUNUSED
#endif

/* internal inline SWIG method */
#ifndef SWIGINTERNINLINE
# define SWIGINTERNINLINE SWIGINTERN SWIGINLINE
#endif

/* qualifier for exported *const* global data variables*/
#ifndef SWIGEXTERN
# ifdef __cplusplus
#   define SWIGEXTERN extern
# else
#   define SWIGEXTERN
# endif
#endif

/* exporting methods */
#if defined(__GNUC__)
#  if (__GNUC__ >= 4) || (__GNUC__ == 3 && __GNUC_MINOR__ >= 4)
#    ifndef GCC_HASCLASSVISIBILITY
#      define GCC_HASCLASSVISIBILITY
#    endif
#  endif
#endif

#ifndef SWIGEXPORT
# if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#   if defined(STATIC_LINKED)
#     define SWIGEXPORT
#   else
#     define SWIGEXPORT __declspec(dllexport)
#   endif
# else
#   if defined(__GNUC__) && defined(GCC_HASCLASSVISIBILITY)
#     define SWIGEXPORT __attribute__ ((visibility("default")))
#   else
#     define SWIGEXPORT
#   endif
# endif
#endif

/* calling conventions for Windows */
#ifndef SWIGSTDCALL
# if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#   define SWIGSTDCALL __stdcall
# else
#   define SWIGSTDCALL
# endif
#endif

/* Deal with Microsoft's attempt at deprecating C standard runtime functions */
#if !defined(SWIG_NO_CRT_SECURE_NO_DEPRECATE) && defined(_MSC_VER) && !defined(_CRT_SECURE_NO_DEPRECATE)
# define _CRT_SECURE_NO_DEPRECATE
#endif

/* Deal with Microsoft's attempt at deprecating methods in the standard C++ library */
#if !defined(SWIG_NO_SCL_SECURE_NO_DEPRECATE) && defined(_MSC_VER) && !defined(_SCL_SECURE_NO_DEPRECATE)
# define _SCL_SECURE_NO_DEPRECATE
#endif

/* Deal with Apple's deprecated 'AssertMacros.h' from Carbon-framework */
#if defined(__APPLE__) && !defined(__ASSERT_MACROS_DEFINE_VERSIONS_WITHOUT_UNDERSCORES)
# define __ASSERT_MACROS_DEFINE_VERSIONS_WITHOUT_UNDERSCORES 0
#endif

/* Intel's compiler complains if a variable which was never initialised is
 * cast to void, which is a common idiom which we use to indicate that we
 * are aware a variable isn't used.  So we just silence that warning.
 * See: https://github.com/swig/swig/issues/192 for more discussion.
 */
#ifdef __INTEL_COMPILER
# pragma warning disable 592
#endif

/*  Errors in SWIG */
#define  SWIG_UnknownError    	   -1
#define  SWIG_IOError        	   -2
#define  SWIG_RuntimeError   	   -3
#define  SWIG_IndexError     	   -4
#define  SWIG_TypeError      	   -5
#define  SWIG_DivisionByZero 	   -6
#define  SWIG_OverflowError  	   -7
#define  SWIG_SyntaxError    	   -8
#define  SWIG_ValueError     	   -9
#define  SWIG_SystemError    	   -10
#define  SWIG_AttributeError 	   -11
#define  SWIG_MemoryError    	   -12
#define  SWIG_NullReferenceError   -13




#include <assert.h>
#define SWIG_exception_impl(DECL, CODE, MSG, RETURNNULL) \
 {STAN_SUNDIALS_PRINTF("In " DECL ": " MSG); assert(0); RETURNNULL; }


#include <stdio.h>
#if defined(_MSC_VER) || defined(__BORLANDC__) || defined(_WATCOM)
# ifndef snprintf
#  define snprintf _snprintf
# endif
#endif


/* Support for the `contract` feature.
 *
 * Note that RETURNNULL is first because it's inserted via a 'Replaceall' in
 * the fortran.cxx file.
 */
#define SWIG_contract_assert(RETURNNULL, EXPR, MSG) \
 if (!(EXPR)) { SWIG_exception_impl("$decl", SWIG_ValueError, MSG, RETURNNULL); } 


#define SWIGVERSION 0x040000 
#define SWIG_VERSION SWIGVERSION


#define SWIG_as_voidptr(a) (void *)((const void *)(a)) 
#define SWIG_as_voidptrptr(a) ((void)SWIG_as_voidptr(*a),(void**)(a)) 


#include "sundials/sundials_linearsolver.h"


#include "sunlinsol/sunlinsol_sptfqmr.h"

SWIGEXPORT SUNLinearSolver _wrap_FSUNLinSol_SPTFQMR(N_Vector farg1, int const *farg2, int const *farg3) {
  SUNLinearSolver fresult ;
  N_Vector arg1 = (N_Vector) 0 ;
  int arg2 ;
  int arg3 ;
  SUNLinearSolver result;
  
  arg1 = (N_Vector)(farg1);
  arg2 = (int)(*farg2);
  arg3 = (int)(*farg3);
  result = (SUNLinearSolver)SUNLinSol_SPTFQMR(arg1,arg2,arg3);
  fresult = result;
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSol_SPTFQMRSetPrecType(SUNLinearSolver farg1, int const *farg2) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int arg2 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (int)(*farg2);
  result = (int)SUNLinSol_SPTFQMRSetPrecType(arg1,arg2);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSol_SPTFQMRSetMaxl(SUNLinearSolver farg1, int const *farg2) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int arg2 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (int)(*farg2);
  result = (int)SUNLinSol_SPTFQMRSetMaxl(arg1,arg2);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT SUNLinearSolver _wrap_FSUNSPTFQMR(N_Vector farg1, int const *farg2, int const *farg3) {
  SUNLinearSolver fresult ;
  N_Vector arg1 = (N_Vector) 0 ;
  int arg2 ;
  int arg3 ;
  SUNLinearSolver result;
  
  arg1 = (N_Vector)(farg1);
  arg2 = (int)(*farg2);
  arg3 = (int)(*farg3);
  result = (SUNLinearSolver)SUNSPTFQMR(arg1,arg2,arg3);
  fresult = result;
  return fresult;
}


SWIGEXPORT int _wrap_FSUNSPTFQMRSetPrecType(SUNLinearSolver farg1, int const *farg2) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int arg2 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (int)(*farg2);
  result = (int)SUNSPTFQMRSetPrecType(arg1,arg2);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNSPTFQMRSetMaxl(SUNLinearSolver farg1, int const *farg2) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int arg2 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (int)(*farg2);
  result = (int)SUNSPTFQMRSetMaxl(arg1,arg2);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolGetType_SPTFQMR(SUNLinearSolver farg1) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  SUNLinearSolver_Type result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = (SUNLinearSolver_Type)SUNLinSolGetType_SPTFQMR(arg1);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolGetID_SPTFQMR(SUNLinearSolver farg1) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  SUNLinearSolver_ID result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = (SUNLinearSolver_ID)SUNLinSolGetID_SPTFQMR(arg1);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolInitialize_SPTFQMR(SUNLinearSolver farg1) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = (int)SUNLinSolInitialize_SPTFQMR(arg1);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSetATimes_SPTFQMR(SUNLinearSolver farg1, void *farg2, ATimesFn farg3) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  void *arg2 = (void *) 0 ;
  ATimesFn arg3 = (ATimesFn) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (void *)(farg2);
  arg3 = (ATimesFn)(farg3);
  result = (int)SUNLinSolSetATimes_SPTFQMR(arg1,arg2,arg3);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSetPreconditioner_SPTFQMR(SUNLinearSolver farg1, void *farg2, PSetupFn farg3, PSolveFn farg4) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  void *arg2 = (void *) 0 ;
  PSetupFn arg3 = (PSetupFn) 0 ;
  PSolveFn arg4 = (PSolveFn) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (void *)(farg2);
  arg3 = (PSetupFn)(farg3);
  arg4 = (PSolveFn)(farg4);
  result = (int)SUNLinSolSetPreconditioner_SPTFQMR(arg1,arg2,arg3,arg4);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSetScalingVectors_SPTFQMR(SUNLinearSolver farg1, N_Vector farg2, N_Vector farg3) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  N_Vector arg2 = (N_Vector) 0 ;
  N_Vector arg3 = (N_Vector) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (N_Vector)(farg2);
  arg3 = (N_Vector)(farg3);
  result = (int)SUNLinSolSetScalingVectors_SPTFQMR(arg1,arg2,arg3);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSetup_SPTFQMR(SUNLinearSolver farg1, SUNMatrix farg2) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  SUNMatrix arg2 = (SUNMatrix) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (SUNMatrix)(farg2);
  result = (int)SUNLinSolSetup_SPTFQMR(arg1,arg2);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSolve_SPTFQMR(SUNLinearSolver farg1, SUNMatrix farg2, N_Vector farg3, N_Vector farg4, double const *farg5) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  SUNMatrix arg2 = (SUNMatrix) 0 ;
  N_Vector arg3 = (N_Vector) 0 ;
  N_Vector arg4 = (N_Vector) 0 ;
  realtype arg5 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (SUNMatrix)(farg2);
  arg3 = (N_Vector)(farg3);
  arg4 = (N_Vector)(farg4);
  arg5 = (realtype)(*farg5);
  result = (int)SUNLinSolSolve_SPTFQMR(arg1,arg2,arg3,arg4,arg5);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolNumIters_SPTFQMR(SUNLinearSolver farg1) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = (int)SUNLinSolNumIters_SPTFQMR(arg1);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT double _wrap_FSUNLinSolResNorm_SPTFQMR(SUNLinearSolver farg1) {
  double fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  realtype result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = (realtype)SUNLinSolResNorm_SPTFQMR(arg1);
  fresult = (realtype)(result);
  return fresult;
}


SWIGEXPORT N_Vector _wrap_FSUNLinSolResid_SPTFQMR(SUNLinearSolver farg1) {
  N_Vector fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  N_Vector result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = (N_Vector)SUNLinSolResid_SPTFQMR(arg1);
  fresult = result;
  return fresult;
}


SWIGEXPORT int64_t _wrap_FSUNLinSolLastFlag_SPTFQMR(SUNLinearSolver farg1) {
  int64_t fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  sunindextype result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = SUNLinSolLastFlag_SPTFQMR(arg1);
  fresult = (sunindextype)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSpace_SPTFQMR(SUNLinearSolver farg1, long *farg2, long *farg3) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  long *arg2 = (long *) 0 ;
  long *arg3 = (long *) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (long *)(farg2);
  arg3 = (long *)(farg3);
  result = (int)SUNLinSolSpace_SPTFQMR(arg1,arg2,arg3);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolFree_SPTFQMR(SUNLinearSolver farg1) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  result = (int)SUNLinSolFree_SPTFQMR(arg1);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSetInfoFile_SPTFQMR(SUNLinearSolver farg1, void *farg2) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  FILE *arg2 = (FILE *) 0 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (FILE *)(farg2);
  result = (int)SUNLinSolSetInfoFile_SPTFQMR(arg1,arg2);
  fresult = (int)(result);
  return fresult;
}


SWIGEXPORT int _wrap_FSUNLinSolSetPrintLevel_SPTFQMR(SUNLinearSolver farg1, int const *farg2) {
  int fresult ;
  SUNLinearSolver arg1 = (SUNLinearSolver) 0 ;
  int arg2 ;
  int result;
  
  arg1 = (SUNLinearSolver)(farg1);
  arg2 = (int)(*farg2);
  result = (int)SUNLinSolSetPrintLevel_SPTFQMR(arg1,arg2);
  fresult = (int)(result);
  return fresult;
}



