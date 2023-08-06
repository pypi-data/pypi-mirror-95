#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <optional>
#include "psydapt.hpp"

namespace py = pybind11;
using namespace pybind11::literals;
using psydapt::staircase::Staircase;

class PStaircase : public Staircase
{
public:
    PStaircase(double start_val,
               std::vector<double> step_sizes,
               unsigned int n_trials,
               int n_up,
               int n_down,
               bool apply_initial_rule,
               psydapt::Scale stim_scale,
               std::optional<unsigned int> n_reversals,
               std::optional<double> min_val,
               std::optional<double> max_val) : Staircase::Staircase(Staircase::Params{start_val,
                                                                                       step_sizes,
                                                                                       n_trials,
                                                                                       n_up,
                                                                                       n_down,
                                                                                       apply_initial_rule,
                                                                                       stim_scale,
                                                                                       n_reversals,
                                                                                       min_val,
                                                                                       max_val}) {}
};

void pystaircase(py::module &m)
{
    py::class_<PStaircase>(m, "Staircase")
        .def(py::init<double,
                      std::vector<double>,
                      unsigned int,
                      int,
                      int,
                      bool,
                      psydapt::Scale,
                      std::optional<unsigned int>,
                      std::optional<double>,
                      std::optional<double>>(),
             "start_val"_a,
             "step_sizes"_a,
             "n_trials"_a,
             "n_up"_a,
             "n_down"_a,
             "apply_initial_rule"_a,
             "stim_scale"_a,
             "n_reversals"_a = std::nullopt,
             "min_val"_a = std::nullopt,
             "max_val"_a = std::nullopt)
        .def("next", &Staircase::next)
        .def("update", &Staircase::update, "response"_a, "stimulus"_a = std::nullopt);
};
