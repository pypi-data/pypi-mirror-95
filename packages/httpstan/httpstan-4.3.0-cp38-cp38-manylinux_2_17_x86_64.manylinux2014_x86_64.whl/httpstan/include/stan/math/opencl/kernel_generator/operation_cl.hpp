#ifndef STAN_MATH_OPENCL_KERNEL_GENERATOR_OPERATION_CL_HPP
#define STAN_MATH_OPENCL_KERNEL_GENERATOR_OPERATION_CL_HPP
#ifdef STAN_OPENCL

#include <stan/math/prim/meta.hpp>
#include <stan/math/prim/err/check_nonnegative.hpp>
#include <stan/math/opencl/kernel_generator/type_str.hpp>
#include <stan/math/opencl/kernel_generator/name_generator.hpp>
#include <stan/math/opencl/matrix_cl_view.hpp>
#include <stan/math/opencl/matrix_cl.hpp>
#include <stan/math/opencl/kernel_cl.hpp>
#include <CL/cl2.hpp>
#include <algorithm>
#include <string>
#include <utility>
#include <tuple>
#include <map>
#include <array>
#include <numeric>
#include <vector>

namespace stan {
namespace math {

/** \addtogroup opencl_kernel_generator
 *  @{
 */
/**
 * Parts of an OpenCL kernel, generated by an expression
 */
struct kernel_parts {
  std::string includes;  // any function definitions - as if they were includet
                         // at the start of kernel source
  std::string declarations;    // declarations of any local variables
  std::string initialization;  // the code for initializations done by all
                               // threads, even if they have no work
  std::string body_prefix;     // the code that should be placed at the start of
                            // the kernel body (before the code for arguments of
                            // an operation)
  std::string body;  // the body of the kernel - code executing operations
  std::string body_suffix;  // the code that should be placed at the end of
                            // the kernel body
  std::string reduction;    // the code for reductions within work group by all
                            // threads, even if they have no work
  std::string args;         // kernel arguments

  kernel_parts operator+(const kernel_parts& other) {
    return {includes + other.includes,
            declarations += other.declarations,
            initialization + other.initialization,
            body_prefix + other.body_prefix,
            body + other.body,
            body_suffix + other.body_suffix,
            reduction + other.reduction,
            args + other.args};
  }

  kernel_parts operator+=(const kernel_parts& other) {
    includes += other.includes;
    declarations += other.declarations;
    initialization += other.initialization;
    body_prefix += other.body_prefix;
    body += other.body;
    body_suffix += other.body_suffix;
    reduction += other.reduction;
    args += other.args;
    return *this;
  }
};

/**
 * Base for all kernel generator operations.
 * @tparam Derived derived type
 * @tparam Scalar scalar type of the result
 * @tparam Args types of arguments to this operation
 */
template <typename Derived, typename Scalar, typename... Args>
class operation_cl : public operation_cl_base {
  static_assert(
      conjunction<std::is_base_of<operation_cl_base,
                                  std::remove_reference_t<Args>>...>::value,
      "operation_cl: all arguments to operation must be operations!");

 protected:
  std::tuple<Args...> arguments_;
  mutable std::string var_name_;  // name of the variable that holds result of
                                  // this operation in the kernel

 public:
  /**
   * Casts the instance into its derived type.
   * @return \c this cast into derived type
   */
  inline Derived& derived() { return *static_cast<Derived*>(this); }

  /**
   * Casts the instance into its derived type.
   * @return \c this cast into derived type
   */
  inline const Derived& derived() const {
    return *static_cast<const Derived*>(this);
  }

  using Deriv = Derived;
  using ArgsTuple = std::tuple<Args...>;
  static const bool require_specific_local_size;
  // number of arguments this operation has
  static constexpr int N = sizeof...(Args);
  using view_transitivity = std::tuple<std::is_same<Args, void>...>;
  // value representing a not yet determined size
  static const int dynamic = -1;

  /**
    Returns an argument to this operation
    @tparam N index of the argument
    */
  template <size_t N>
  const auto& get_arg() const {
    return std::get<N>(arguments_);
  }

  /**
   * Constructor
   * @param arguments Arguments of this expression that are also valid
   * expressions
   */
  explicit operation_cl(Args&&... arguments)
      : arguments_(std::forward<Args>(arguments)...) {}

  /**
   * Evaluates the expression.
   * @return Result of the expression.
   */
  matrix_cl<Scalar> eval() const {
    int rows = derived().rows();
    int cols = derived().cols();
    const char* function = "operation_cl.eval()";
    if (rows < 0) {
      invalid_argument(function, "Number of rows of expression", rows,
                       " must be nonnegative, but is ",
                       " (broadcasted expressions can not be evaluated)");
    }
    if (cols < 0) {
      invalid_argument(function, "Number of columns of expression", cols,
                       " must be nonnegative, but is ",
                       " (broadcasted expressions can not be evaluated)");
    }
    matrix_cl<Scalar> res(rows, cols, derived().view());
    if (res.size() > 0) {
      this->evaluate_into(res);
    }
    return res;
  }

  /**
   * Evaluates \c this expression into given left-hand-side expression.
   * If the kernel for this expression is not cached it is generated and then
   * executed.
   * @tparam T_lhs type of the left-hand-side expression
   * @param lhs Left-hand-side expression
   */
  template <typename T_lhs>
  inline void evaluate_into(T_lhs& lhs) const;

  /**
   * Generates kernel source for evaluating \c this expression into given
   * left-hand-side expression.
   * @tparam T_lhs type of the left-hand-side expression
   * @param lhs Left-hand-side expression
   * @return kernel source
   */
  template <typename T_lhs>
  inline std::string get_kernel_source_for_evaluating_into(
      const T_lhs& lhs) const;

  /**
   * Generates kernel code for assigning this expression into result expression.
   * @param[in,out] generated map from (pointer to) already generated local
   * operations to variable names
   * @param[in,out] generated_all map from (pointer to) already generated all
   * operations to variable names
   * @param ng name generator for this kernel
   * @param row_index_name row index variable name
   * @param col_index_name column index variable name
   * @param result expression into which result is to be assigned
   * @return part of kernel with code for this and nested expressions
   */
  template <typename T_result>
  kernel_parts get_whole_kernel_parts(
      std::map<const void*, const char*>& generated,
      std::map<const void*, const char*>& generated_all, name_generator& ng,
      const std::string& row_index_name, const std::string& col_index_name,
      const T_result& result) const {
    kernel_parts parts = derived().get_kernel_parts(
        generated, generated_all, ng, row_index_name, col_index_name, false);
    kernel_parts out_parts = result.get_kernel_parts_lhs(
        generated, generated_all, ng, row_index_name, col_index_name);
    out_parts.body += " = " + derived().var_name_ + ";\n";
    parts += out_parts;
    return parts;
  }

  /**
   * Generates kernel code for this and nested expressions.
   * @param[in,out] generated map from (pointer to) already generated local
   * operations to variable names
   * @param[in,out] generated_all map from (pointer to) already generated all
   * operations to variable names
   * @param name_gen name generator for this kernel
   * @param row_index_name row index variable name
   * @param col_index_name column index variable name
   * @param view_handled whether caller already handled matrix view
   * @return part of kernel with code for this and nested expressions
   */
  inline kernel_parts get_kernel_parts(
      std::map<const void*, const char*>& generated,
      std::map<const void*, const char*>& generated_all,
      name_generator& name_gen, const std::string& row_index_name,
      const std::string& col_index_name, bool view_handled) const {
    kernel_parts res{};
    if (generated.count(this) == 0) {
      this->var_name_ = name_gen.generate();
      generated[this] = "";
      std::string row_index_name_arg = row_index_name;
      std::string col_index_name_arg = col_index_name;
      derived().modify_argument_indices(row_index_name_arg, col_index_name_arg);
      std::array<kernel_parts, N> args_parts = index_apply<N>([&](auto... Is) {
        std::map<const void*, const char*> generated2;
        return std::array<kernel_parts, N>{this->get_arg<Is>().get_kernel_parts(
            &Derived::modify_argument_indices
                    == &operation_cl::modify_argument_indices
                ? generated
                : generated2,
            generated_all, name_gen, row_index_name_arg, col_index_name_arg,
            view_handled
                && std::tuple_element_t<
                       Is, typename Deriv::view_transitivity>::value)...};
      });
      res = std::accumulate(args_parts.begin(), args_parts.end(),
                            kernel_parts{});
      kernel_parts my_part = index_apply<N>([&](auto... Is) {
        return this->derived().generate(row_index_name, col_index_name,
                                        view_handled,
                                        this->get_arg<Is>().var_name_...);
      });
      res += my_part;
      res.body = res.body_prefix + res.body;
      res.body_prefix = "";
    }
    return res;
  }

  /**
   * Generates kernel code for this expression.
   * @param row_index_name row index variable name
   * @param col_index_name column index variable name
   * @param view_handled whether caller already handled matrix view
   * @param var_name_arg variable name of the nested expression
   * @return part of kernel with code for this expression
   */
  inline kernel_parts generate(const std::string& row_index_name,
                               const std::string& col_index_name,
                               const bool view_handled,
                               const std::string& var_name_arg) const {
    var_name_ = var_name_arg;
    return {};
  }

  /**
   * Does nothing. Derived classes can override this to modify how indices are
   * passed to its argument expressions. On input arguments \c row_index_name
   * and \c col_index_name are expressions for indices of this operation. On
   * output they are expressions for indices of argument operations.
   * @param[in, out] row_index_name row index
   * @param[in, out] col_index_name column index
   */
  inline void modify_argument_indices(std::string& row_index_name,
                                      std::string& col_index_name) const {}

  /**
   * Sets kernel arguments for nested expressions.
   * @param[in,out] generated map from (pointer to) already generated local
   * operations to variable names
   * @param[in,out] generated_all map from (pointer to) already generated all
   * operations to variable names
   * @param kernel kernel to set arguments on
   * @param[in,out] arg_num consecutive number of the first argument to set.
   * This is incremented for each argument set by this function.
   */
  inline void set_args(std::map<const void*, const char*>& generated,
                       std::map<const void*, const char*>& generated_all,
                       cl::Kernel& kernel, int& arg_num) const {
    if (generated.count(this) == 0) {
      generated[this] = "";
      // parameter pack expansion returns a comma-separated list of values,
      // which can not be used as an expression. We work around that by using
      // comma operator to get a list of ints, which we use to construct an
      // initializer_list from. Cast to voids avoids warnings about unused
      // expression.
      index_apply<N>([&](auto... Is) {
        std::map<const void*, const char*> generated2;
        static_cast<void>(std::initializer_list<int>{
            (this->get_arg<Is>().set_args(
                 &Derived::modify_argument_indices
                         == &operation_cl::modify_argument_indices
                     ? generated
                     : generated2,
                 generated_all, kernel, arg_num),
             0)...});
      });
    }
  }

  /**
   * Adds read event to any matrices used by nested expressions.
   * @param e the event to add
   */
  inline void add_read_event(cl::Event& e) const {
    index_apply<N>([&](auto... Is) {
      static_cast<void>(std::initializer_list<int>{
          (this->get_arg<Is>().add_read_event(e), 0)...});
    });
  }

  /**
   * Adds all write events on any matrices used by nested expressions to a list.
   * @param[out] events List of all events.
   */
  inline void get_write_events(std::vector<cl::Event>& events) const {
    index_apply<N>([&](auto... Is) {
      static_cast<void>(std::initializer_list<int>{
          (this->template get_arg<Is>().get_write_events(events), 0)...});
    });
  }

  /**
   * Number of rows of a matrix that would be the result of evaluating this
   * expression. Some subclasses may need to override this.
   * @return number of rows
   */
  inline int rows() const {
    static_assert(
        N > 0, "default rows does not work on expressions with no arguments!");
    return index_apply<N>([&](auto... Is) {
      // assuming all non-dynamic sizes match
      return std::max({this->get_arg<Is>().rows()...});
    });
  }

  /**
   * Number of columns of a matrix that would be the result of evaluating this
   * expression. Some subclasses may need to override this.
   * @return number of columns
   */
  inline int cols() const {
    static_assert(
        N > 0, "default cols does not work on expressions with no arguments!");
    return index_apply<N>([&](auto... Is) {
      // assuming all non-dynamic sizes match
      return std::max({this->get_arg<Is>().cols()...});
    });
  }

  /**
   * Number of rows threads need to be launched for. For most expressions this
   * equals number of rows of the result.
   * @return number of rows
   */
  inline int thread_rows() const { return derived().rows(); }

  /**
   * Number of columns threads need to be launched for. For most expressions
   * this equals number of cols of the result.
   * @return number of columns
   */
  inline int thread_cols() const { return derived().cols(); }

  /**
   * Determine indices of extreme sub- and superdiagonals written. Some
   * subclasses may need to override this.
   * @return pair of indices - bottom and top diagonal
   */
  inline std::pair<int, int> extreme_diagonals() const {
    static_assert(N > 0,
                  "default extreme_diagonals does not work on expressions with "
                  "no arguments!");
    return index_apply<N>([&](auto... Is) {
      auto arg_diags
          = std::make_tuple(this->get_arg<Is>().extreme_diagonals()...);
      int bottom = std::min(
          std::initializer_list<int>({std::get<Is>(arg_diags).first...}));
      int top = std::max(
          std::initializer_list<int>({std::get<Is>(arg_diags).second...}));
      return std::make_pair(bottom, top);
    });
  }

  /**
   * View of a matrix that would be the result of evaluating this expression.
   * @return view
   */
  inline matrix_cl_view view() const {
    std::pair<int, int> diagonals = derived().extreme_diagonals();
    matrix_cl_view view;
    if (diagonals.first < 0) {
      view = matrix_cl_view::Lower;
    } else {
      view = matrix_cl_view::Diagonal;
    }
    if (diagonals.second > 0) {
      view = either(view, matrix_cl_view::Upper);
    }
    return view;
  }

  /**
   * Collects data that is needed beside types to uniqly identify a kernel
   * generator expression.
   * @param[out] uids ids of unique matrix accesses
   * @param[in,out] id_map map from memory addresses to unique ids
   * @param[in,out] next_id neqt unique id to use
   */
  inline void get_unique_matrix_accesses(std::vector<int>& uids,
                                         std::map<const void*, int>& id_map,
                                         int& next_id) const {
    index_apply<N>([&](auto... Is) {
      static_cast<void>(std::initializer_list<int>{(
          this->get_arg<Is>().get_unique_matrix_accesses(uids, id_map, next_id),
          0)...});
    });
  }
};

template <typename Derived, typename Scalar, typename... Args>
const bool operation_cl<Derived, Scalar, Args...>::require_specific_local_size
    = std::max({false,
                std::decay_t<Args>::Deriv::require_specific_local_size...});
/** @}*/
}  // namespace math
}  // namespace stan

#endif
#endif
