/*
 * -----------------------------------------------------------------
 * Programmer(s): David Gardner, Cody J. Balos @ LLNL
 * -----------------------------------------------------------------
 * SUNDIALS Copyright Start
 * Copyright (c) 2002-2020, Lawrence Livermore National Security
 * and Southern Methodist University.
 * All rights reserved.
 *
 * See the top-level LICENSE and NOTICE files for details.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 * SUNDIALS Copyright End
 * -----------------------------------------------------------------
 */


#ifndef _NVECTOR_CUDA_ARRAY_KERNELS_CUH_
#define _NVECTOR_CUDA_ARRAY_KERNELS_CUH_

#include <limits>
#include <cuda_runtime.h>

#include "sundials_cuda_kernels.cuh"

using namespace sundials::cuda;

namespace sundials
{
namespace nvector_cuda
{

/* -----------------------------------------------------------------
 * The namespace for CUDA kernels
 *
 * Reduction CUDA kernels in nvector are based in part on "reduction"
 * example in NVIDIA Corporation CUDA Samples, and parallel reduction
 * examples in textbook by J. Cheng at al. "CUDA C Programming".
 * -----------------------------------------------------------------
 */

/*
 * -----------------------------------------------------------------------------
 * fused vector operation kernels
 * -----------------------------------------------------------------------------
 */

/*
 * Computes the linear combination of nv vectors
 */
template <typename T, typename I>
__global__ void
linearCombinationKernel(int nv, T* c, T** xd, T* zd, I n)
{
  GRID_STRIDE_XLOOP(I, i, n)
  {
    zd[i] = c[0]*xd[0][i];
    for (int j=1; j<nv; j++)
      zd[i] += c[j]*xd[j][i];
  }
}

/*
 * Computes the scaled sum of one vector with nv other vectors
 */
template <typename T, typename I>
__global__ void
scaleAddMultiKernel(int nv, T* c, T* xd, T** yd, T** zd, I n)
{
  GRID_STRIDE_XLOOP(I, i, n)
  {
    for (int j=0; j<nv; j++)
      zd[j][i] = c[j] * xd[i] + yd[j][i];
  }
}


/*
 * Dot product of one vector with nv other vectors.
 *
 */
template <typename T, typename I>
__global__ void
dotProdMultiKernel(int nv, const T* xd, T** yd, T* out, I n)
{
  // REQUIRES nv blocks (i.e. gridDim.x == nv)
  const I k = blockIdx.x;

  // Initialize to zero.
  T sum = 0.0;
  for (I i = threadIdx.x; i < n; i += blockDim.x)
  { // each thread computes n/blockDim.x elements
    sum += xd[i] * yd[k][i];
  }
  sum = blockReduce<T, RSUM>(sum, 0.0); 

  // Copy reduction result for each block to global memory
  if (threadIdx.x == 0) atomicAdd(&out[k], sum);
}


/*
 * -----------------------------------------------------------------------------
 * vector array operation kernels
 * -----------------------------------------------------------------------------
 */

 
/*
 * Computes the linear sum of multiple vectors
 */
template <typename T, typename I>
__global__ void
linearSumVectorArrayKernel(int nv, T a, T** xd, T b, T** yd, T** zd, I n)
{
  GRID_STRIDE_XLOOP(I, i, n)
  {
    for (int j=0; j<nv; j++)
      zd[j][i] = a * xd[j][i] + b * yd[j][i];
  }
}


/*
 * Scales multiple vectors
 */
template <typename T, typename I>
__global__ void
scaleVectorArrayKernel(int nv, T* c, T** xd, T** zd, I n)
{
  GRID_STRIDE_XLOOP(I, i, n)
  {
    for (int j=0; j<nv; j++)
      zd[j][i] = c[j] * xd[j][i];
  }
}


/*
 * Sets multiple vectors equal to a constant
 */
template <typename T, typename I>
__global__ void
constVectorArrayKernel(int nv, T c, T** zd, I n)
{
  GRID_STRIDE_XLOOP(I, i, n)
  {
    for (int j=0; j<nv; j++)
      zd[j][i] = c;
  }
}


/*
 * WRMS norm of nv vectors.
 *
 */
template <typename T, typename I>
__global__ void
wL2NormSquareVectorArrayKernel(int nv, T** xd, T** wd, T* out, I n)
{
  // REQUIRES nv blocks (i.e. gridDim.x == nv)
  const I k = blockIdx.x;

  // Initialize to zero.
  T sum = 0.0;
  for (I i = threadIdx.x; i < n; i += blockDim.x)
  { // each thread computes n/blockDim.x elements
    sum += xd[k][i] * wd[k][i] * xd[k][i] * wd[k][i];
  }
  sum = blockReduce<T, RSUM>(sum, 0.0);

  // Copy reduction result for each block to global memory
  if (threadIdx.x == 0) atomicAdd(&out[k], sum);
}


/*
 * Masked WRMS norm of nv vectors.
 *
 */
template <typename T, typename I>
__global__ void
wL2NormSquareMaskVectorArrayKernel(int nv, T** xd, T** wd, T* id, T* out, I n)
{
  // REQUIRES nv blocks (i.e. gridDim.x == nv)
  const I k = blockIdx.x;

  // Initialize to zero.
  T sum = 0.0;
  for (I i = threadIdx.x; i < n; i += blockDim.x)
  { // each thread computes n/blockDim.x elements
    if (id[i] > 0.0) sum += xd[k][i] * wd[k][i] * xd[k][i] * wd[k][i];
  }
  sum = blockReduce<T, RSUM>(sum, 0.0);

  // Copy reduction result for each block to global memory
  if (threadIdx.x == 0) atomicAdd(&out[k], sum);
}


/*
 * Computes the scaled sum of a vector array with multiple other vector arrays
 */
template <typename T, typename I>
__global__ void
scaleAddMultiVectorArrayKernel(int nv, int ns, T* c, T** xd, T** yd, T** zd, I n)
{
  GRID_STRIDE_XLOOP(I, i, n)
  {
    for (int k=0; k<nv; k++)
      for (int j=0; j<ns; j++)
        zd[k*ns+j][i] = c[j] * xd[k][i] + yd[k*ns+j][i];
  }
}


/*
 * Computes the scaled sum of a vector array with multiple other vector arrays
 */
template <typename T, typename I>
__global__ void
linearCombinationVectorArrayKernel(int nv, int ns, T* c, T** xd, T** zd, I n)
{
  GRID_STRIDE_XLOOP(I, i, n)
  {
    for (int k=0; k<nv; k++)
    {
      zd[k][i] = c[0]*xd[k*ns][i];
      for (int j=1; j<ns; j++)
        zd[k][i] += c[j]*xd[k*ns+j][i];
    }
  }
}

} // namespace nvector_cuda
} // namespace sundials

#endif // _NVECTOR_CUDA_ARRAY_KERNELS_CUH_
