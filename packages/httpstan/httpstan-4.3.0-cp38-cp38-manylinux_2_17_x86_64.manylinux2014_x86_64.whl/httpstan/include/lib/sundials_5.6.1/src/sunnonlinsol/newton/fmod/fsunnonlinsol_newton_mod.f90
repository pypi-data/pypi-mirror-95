! This file was automatically generated by SWIG (http://www.swig.org).
! Version 4.0.0
!
! Do not make changes to this file unless you know what you are doing--modify
! the SWIG interface file instead.

! ---------------------------------------------------------------
! Programmer(s): Auto-generated by swig.
! ---------------------------------------------------------------
! SUNDIALS Copyright Start
! Copyright (c) 2002-2020, Lawrence Livermore National Security
! and Southern Methodist University.
! All rights reserved.
!
! See the top-level LICENSE and NOTICE files for details.
!
! SPDX-License-Identifier: BSD-3-Clause
! SUNDIALS Copyright End
! ---------------------------------------------------------------

module fsunnonlinsol_newton_mod
 use, intrinsic :: ISO_C_BINDING
 use fsundials_nvector_mod
 use fsundials_types_mod
 use fsundials_nonlinearsolver_mod
 use fsundials_nvector_mod
 use fsundials_types_mod
 implicit none
 private

 ! DECLARATION CONSTRUCTS
 public :: FSUNNonlinSol_Newton
 public :: FSUNNonlinSol_NewtonSens
 public :: FSUNNonlinSolGetType_Newton
 public :: FSUNNonlinSolInitialize_Newton
 public :: FSUNNonlinSolSolve_Newton
 public :: FSUNNonlinSolFree_Newton
 public :: FSUNNonlinSolSetSysFn_Newton
 public :: FSUNNonlinSolSetLSetupFn_Newton
 public :: FSUNNonlinSolSetLSolveFn_Newton
 public :: FSUNNonlinSolSetConvTestFn_Newton
 public :: FSUNNonlinSolSetMaxIters_Newton
 public :: FSUNNonlinSolGetNumIters_Newton
 public :: FSUNNonlinSolGetCurIter_Newton
 public :: FSUNNonlinSolGetNumConvFails_Newton
 public :: FSUNNonlinSolGetSysFn_Newton
 public :: FSUNNonlinSolSetInfoFile_Newton
 public :: FSUNNonlinSolSetPrintLevel_Newton

! WRAPPER DECLARATIONS
interface
function swigc_FSUNNonlinSol_Newton(farg1) &
bind(C, name="_wrap_FSUNNonlinSol_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_PTR) :: fresult
end function

function swigc_FSUNNonlinSol_NewtonSens(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSol_NewtonSens") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
integer(C_INT), intent(in) :: farg1
type(C_PTR), value :: farg2
type(C_PTR) :: fresult
end function

function swigc_FSUNNonlinSolGetType_Newton(farg1) &
bind(C, name="_wrap_FSUNNonlinSolGetType_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolInitialize_Newton(farg1) &
bind(C, name="_wrap_FSUNNonlinSolInitialize_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSolve_Newton(farg1, farg2, farg3, farg4, farg5, farg6, farg7) &
bind(C, name="_wrap_FSUNNonlinSolSolve_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_PTR), value :: farg2
type(C_PTR), value :: farg3
type(C_PTR), value :: farg4
real(C_DOUBLE), intent(in) :: farg5
integer(C_INT), intent(in) :: farg6
type(C_PTR), value :: farg7
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolFree_Newton(farg1) &
bind(C, name="_wrap_FSUNNonlinSolFree_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSetSysFn_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolSetSysFn_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_FUNPTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSetLSetupFn_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolSetLSetupFn_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_FUNPTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSetLSolveFn_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolSetLSolveFn_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_FUNPTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSetConvTestFn_Newton(farg1, farg2, farg3) &
bind(C, name="_wrap_FSUNNonlinSolSetConvTestFn_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_FUNPTR), value :: farg2
type(C_PTR), value :: farg3
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSetMaxIters_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolSetMaxIters_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
integer(C_INT), intent(in) :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolGetNumIters_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolGetNumIters_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_PTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolGetCurIter_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolGetCurIter_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_PTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolGetNumConvFails_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolGetNumConvFails_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_PTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolGetSysFn_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolGetSysFn_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_PTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSetInfoFile_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolSetInfoFile_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
type(C_PTR), value :: farg2
integer(C_INT) :: fresult
end function

function swigc_FSUNNonlinSolSetPrintLevel_Newton(farg1, farg2) &
bind(C, name="_wrap_FSUNNonlinSolSetPrintLevel_Newton") &
result(fresult)
use, intrinsic :: ISO_C_BINDING
type(C_PTR), value :: farg1
integer(C_INT), intent(in) :: farg2
integer(C_INT) :: fresult
end function

end interface


contains
 ! MODULE SUBPROGRAMS
function FSUNNonlinSol_Newton(y) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
type(SUNNonlinearSolver), pointer :: swig_result
type(N_Vector), target, intent(inout) :: y
type(C_PTR) :: fresult 
type(C_PTR) :: farg1 

farg1 = c_loc(y)
fresult = swigc_FSUNNonlinSol_Newton(farg1)
call c_f_pointer(fresult, swig_result)
end function

function FSUNNonlinSol_NewtonSens(count, y) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
type(SUNNonlinearSolver), pointer :: swig_result
integer(C_INT), intent(in) :: count
type(N_Vector), target, intent(inout) :: y
type(C_PTR) :: fresult 
integer(C_INT) :: farg1 
type(C_PTR) :: farg2 

farg1 = count
farg2 = c_loc(y)
fresult = swigc_FSUNNonlinSol_NewtonSens(farg1, farg2)
call c_f_pointer(fresult, swig_result)
end function

function FSUNNonlinSolGetType_Newton(nls) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(SUNNonlinearSolver_Type) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 

farg1 = c_loc(nls)
fresult = swigc_FSUNNonlinSolGetType_Newton(farg1)
swig_result = fresult
end function

function FSUNNonlinSolInitialize_Newton(nls) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 

farg1 = c_loc(nls)
fresult = swigc_FSUNNonlinSolInitialize_Newton(farg1)
swig_result = fresult
end function

function FSUNNonlinSolSolve_Newton(nls, y0, y, w, tol, calllsetup, mem) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
type(N_Vector), target, intent(inout) :: y0
type(N_Vector), target, intent(inout) :: y
type(N_Vector), target, intent(inout) :: w
real(C_DOUBLE), intent(in) :: tol
integer(C_INT), intent(in) :: calllsetup
type(C_PTR) :: mem
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_PTR) :: farg2 
type(C_PTR) :: farg3 
type(C_PTR) :: farg4 
real(C_DOUBLE) :: farg5 
integer(C_INT) :: farg6 
type(C_PTR) :: farg7 

farg1 = c_loc(nls)
farg2 = c_loc(y0)
farg3 = c_loc(y)
farg4 = c_loc(w)
farg5 = tol
farg6 = calllsetup
farg7 = mem
fresult = swigc_FSUNNonlinSolSolve_Newton(farg1, farg2, farg3, farg4, farg5, farg6, farg7)
swig_result = fresult
end function

function FSUNNonlinSolFree_Newton(nls) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 

farg1 = c_loc(nls)
fresult = swigc_FSUNNonlinSolFree_Newton(farg1)
swig_result = fresult
end function

function FSUNNonlinSolSetSysFn_Newton(nls, sysfn) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
type(C_FUNPTR), intent(in), value :: sysfn
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_FUNPTR) :: farg2 

farg1 = c_loc(nls)
farg2 = sysfn
fresult = swigc_FSUNNonlinSolSetSysFn_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolSetLSetupFn_Newton(nls, lsetupfn) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
type(C_FUNPTR), intent(in), value :: lsetupfn
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_FUNPTR) :: farg2 

farg1 = c_loc(nls)
farg2 = lsetupfn
fresult = swigc_FSUNNonlinSolSetLSetupFn_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolSetLSolveFn_Newton(nls, lsolvefn) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
type(C_FUNPTR), intent(in), value :: lsolvefn
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_FUNPTR) :: farg2 

farg1 = c_loc(nls)
farg2 = lsolvefn
fresult = swigc_FSUNNonlinSolSetLSolveFn_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolSetConvTestFn_Newton(nls, ctestfn, ctest_data) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
type(C_FUNPTR), intent(in), value :: ctestfn
type(C_PTR) :: ctest_data
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_FUNPTR) :: farg2 
type(C_PTR) :: farg3 

farg1 = c_loc(nls)
farg2 = ctestfn
farg3 = ctest_data
fresult = swigc_FSUNNonlinSolSetConvTestFn_Newton(farg1, farg2, farg3)
swig_result = fresult
end function

function FSUNNonlinSolSetMaxIters_Newton(nls, maxiters) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_INT), intent(in) :: maxiters
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
integer(C_INT) :: farg2 

farg1 = c_loc(nls)
farg2 = maxiters
fresult = swigc_FSUNNonlinSolSetMaxIters_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolGetNumIters_Newton(nls, niters) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_LONG), dimension(*), target, intent(inout) :: niters
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_PTR) :: farg2 

farg1 = c_loc(nls)
farg2 = c_loc(niters(1))
fresult = swigc_FSUNNonlinSolGetNumIters_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolGetCurIter_Newton(nls, iter) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_INT), dimension(*), target, intent(inout) :: iter
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_PTR) :: farg2 

farg1 = c_loc(nls)
farg2 = c_loc(iter(1))
fresult = swigc_FSUNNonlinSolGetCurIter_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolGetNumConvFails_Newton(nls, nconvfails) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_LONG), dimension(*), target, intent(inout) :: nconvfails
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_PTR) :: farg2 

farg1 = c_loc(nls)
farg2 = c_loc(nconvfails(1))
fresult = swigc_FSUNNonlinSolGetNumConvFails_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolGetSysFn_Newton(nls, sysfn) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
type(C_FUNPTR), target, intent(inout) :: sysfn
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_PTR) :: farg2 

farg1 = c_loc(nls)
farg2 = c_loc(sysfn)
fresult = swigc_FSUNNonlinSolGetSysFn_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolSetInfoFile_Newton(nls, info_file) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
type(C_PTR) :: info_file
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
type(C_PTR) :: farg2 

farg1 = c_loc(nls)
farg2 = info_file
fresult = swigc_FSUNNonlinSolSetInfoFile_Newton(farg1, farg2)
swig_result = fresult
end function

function FSUNNonlinSolSetPrintLevel_Newton(nls, print_level) &
result(swig_result)
use, intrinsic :: ISO_C_BINDING
integer(C_INT) :: swig_result
type(SUNNonlinearSolver), target, intent(inout) :: nls
integer(C_INT), intent(in) :: print_level
integer(C_INT) :: fresult 
type(C_PTR) :: farg1 
integer(C_INT) :: farg2 

farg1 = c_loc(nls)
farg2 = print_level
fresult = swigc_FSUNNonlinSolSetPrintLevel_Newton(farg1, farg2)
swig_result = fresult
end function


end module
