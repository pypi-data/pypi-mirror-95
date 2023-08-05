//  Copyright (c) 2014 Anton Bikineev
//  Use, modification and distribution are subject to the
//  Boost Software License, Version 1.0. (See accompanying file
//  LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//
//  Computes test data for the derivatives of the
//  various bessel functions. Results of derivatives
//  are generated by the relations between the derivatives
//  and Bessel functions, which actual implementation
//  doesn't use. Results are printed to ~ 50 digits.
//
#include <fstream>

#include <boost/multiprecision/mpfr.hpp>
#include <boost/math/tools/test_data.hpp>
#include <boost/test/included/prg_exec_monitor.hpp>

#include <boost/math/special_functions/bessel.hpp>

using namespace boost::math::tools;
using namespace boost::math;
using namespace std;
using namespace boost::multiprecision;

template <class T>
T bessel_j_derivative_bare(T v, T x)
{
   return (v / x) * boost::math::cyl_bessel_j(v, x) - boost::math::cyl_bessel_j(v+1, x);
}

template <class T>
T bessel_y_derivative_bare(T v, T x)
{
   return (v / x) * boost::math::cyl_neumann(v, x) - boost::math::cyl_neumann(v+1, x);
}

template <class T>
T bessel_i_derivative_bare(T v, T x)
{
   return (v / x) * boost::math::cyl_bessel_i(v, x) + boost::math::cyl_bessel_i(v+1, x);
}

template <class T>
T bessel_k_derivative_bare(T v, T x)
{
   return (v / x) * boost::math::cyl_bessel_k(v, x) - boost::math::cyl_bessel_k(v+1, x);
}

template <class T>
T sph_bessel_j_derivative_bare(T v, T x)
{
   if((v < 0) || (floor(v) != v))
      throw std::domain_error("");
   if(v == 0)
      return -boost::math::sph_bessel(1, x);
   return boost::math::sph_bessel(itrunc(v-1), x) - ((v + 1) / x) * boost::math::sph_bessel(itrunc(v), x);
}

template <class T>
T sph_bessel_y_derivative_bare(T v, T x)
{
   if((v < 0) || (floor(v) != v))
      throw std::domain_error("");
   if(v == 0)
      return -boost::math::sph_neumann(1, x);
   return boost::math::sph_neumann(itrunc(v-1), x) - ((v + 1) / x) * boost::math::sph_neumann(itrunc(v), x);
}

enum
{
   func_J = 0,
   func_Y,
   func_I,
   func_K,
   func_j,
   func_y
};

int cpp_main(int argc, char*argv [])
{
   typedef number<mpfr_float_backend<200> > bignum;

   parameter_info<bignum> arg1, arg2;
   test_data<bignum> data;

   int functype = 0;
   std::string letter = "J";

   if(argc == 2)
   {
      if(std::strcmp(argv[1], "--Y") == 0)
      {
         functype = func_Y;
         letter = "Y";
      }
      else if(std::strcmp(argv[1], "--I") == 0)
      {
         functype = func_I;
         letter = "I";
      }
      else if(std::strcmp(argv[1], "--K") == 0)
      {
         functype = func_K;
         letter = "K";
      }
      else if(std::strcmp(argv[1], "--j") == 0)
      {
         functype = func_j;
         letter = "j";
      }
      else if(std::strcmp(argv[1], "--y") == 0)
      {
         functype = func_y;
         letter = "y";
      }
      else
         BOOST_ASSERT(0);
   }

   bool cont;
   std::string line;

   std::cout << "Welcome.\n"
      "This program will generate spot tests for the Bessel " << letter << " function derivative\n\n";
   do{
      if(0 == get_user_parameter_info(arg1, "a"))
         return 1;
      if(0 == get_user_parameter_info(arg2, "b"))
         return 1;

      bignum (*fp)(bignum, bignum) = 0;
      if(functype == func_J)
         fp = bessel_j_derivative_bare;
      else if(functype == func_I)
         fp = bessel_i_derivative_bare;
      else if(functype == func_K)
         fp = bessel_k_derivative_bare;
      else if(functype == func_Y)
         fp = bessel_y_derivative_bare;
      else if(functype == func_j)
         fp = sph_bessel_j_derivative_bare;
      else if(functype == func_y)
         fp = sph_bessel_y_derivative_bare;
      else
         BOOST_ASSERT(0);

      data.insert(fp, arg2, arg1);

      std::cout << "Any more data [y/n]?";
      std::getline(std::cin, line);
      boost::algorithm::trim(line);
      cont = (line == "y");
   }while(cont);

   std::cout << "Enter name of test data file [default=bessel_j_derivative_data.ipp]";
   std::getline(std::cin, line);
   boost::algorithm::trim(line);
   if(line == "")
      line = "bessel_j_derivative_data.ipp";
   std::ofstream ofs(line.c_str());
   line.erase(line.find('.'));
   ofs << std::scientific << std::setprecision(50);
   write_code(ofs, data, line.c_str());

   return 0;
}
