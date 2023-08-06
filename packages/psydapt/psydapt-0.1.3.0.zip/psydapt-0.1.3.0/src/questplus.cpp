#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <optional>
#include "psydapt.hpp"

namespace py = pybind11;
using namespace pybind11::literals;
namespace qp = psydapt::questplus;
using psydapt::questplus::CSF;
using psydapt::questplus::NormCDF;
using psydapt::questplus::Weibull;

typedef std::vector<double> svd;
typedef std::optional<svd> osvd;

class PWeibull : public Weibull
{
public:
    PWeibull(svd intensity,
             svd threshold,
             svd slope,
             svd lower_asymptote,
             svd lapse_rate,
             psydapt::Scale stim_scale,
             osvd threshold_prior,
             osvd slope_prior,
             osvd lower_asymptote_prior,
             osvd lapse_rate_prior,
             qp::StimSelectionMethod stim_selection_method,
             qp::ParamEstimationMethod param_estimation_method,
             unsigned int n,
             unsigned int max_consecutive_reps,
             unsigned int random_seed) : Weibull::Weibull(Weibull::Params{stim_selection_method,
                                                                          param_estimation_method,
                                                                          n,
                                                                          max_consecutive_reps,
                                                                          random_seed,
                                                                          stim_scale,
                                                                          intensity,
                                                                          threshold,
                                                                          slope,
                                                                          lower_asymptote,
                                                                          lapse_rate,
                                                                          threshold_prior,
                                                                          slope_prior,
                                                                          lower_asymptote_prior,
                                                                          lapse_rate_prior}) {}
};

class PNormCDF : public NormCDF
{
public:
    PNormCDF(svd intensity,
             svd location,
             svd scale,
             svd lower_asymptote,
             svd lapse_rate,
             psydapt::Scale stim_scale,
             osvd location_prior,
             osvd scale_prior,
             osvd lower_asymptote_prior,
             osvd lapse_rate_prior,
             qp::StimSelectionMethod stim_selection_method,
             qp::ParamEstimationMethod param_estimation_method,
             unsigned int n,
             unsigned int max_consecutive_reps,
             unsigned int random_seed) : NormCDF::NormCDF(NormCDF::Params{stim_selection_method,
                                                                          param_estimation_method,
                                                                          n,
                                                                          max_consecutive_reps,
                                                                          random_seed,
                                                                          stim_scale,
                                                                          intensity,
                                                                          location,
                                                                          scale,
                                                                          lower_asymptote,
                                                                          lapse_rate,
                                                                          location_prior,
                                                                          scale_prior,
                                                                          lower_asymptote_prior,
                                                                          lapse_rate_prior}) {}
};

class PCSF : public CSF
{
public:
    PCSF(svd contrast,
         svd spatial_freq,
         svd temporal_freq,
         svd c0,
         svd cf,
         svd cw,
         svd min_thresh,
         svd slope,
         svd lower_asymptote,
         svd lapse_rate,
         psydapt::Scale stim_scale,
         osvd c0_prior,
         osvd cf_prior,
         osvd cw_prior,
         osvd min_thresh_prior,
         osvd slope_prior,
         osvd lower_asymptote_prior,
         osvd lapse_rate_prior,
         qp::StimSelectionMethod stim_selection_method,
         qp::ParamEstimationMethod param_estimation_method,
         unsigned int n,
         unsigned int max_consecutive_reps,
         unsigned int random_seed) : CSF::CSF(CSF::Params{stim_selection_method,
                                                          param_estimation_method,
                                                          n,
                                                          max_consecutive_reps,
                                                          random_seed,
                                                          stim_scale,
                                                          contrast,
                                                          spatial_freq,
                                                          temporal_freq,
                                                          c0,
                                                          cf,
                                                          cw,
                                                          min_thresh,
                                                          slope,
                                                          lower_asymptote,
                                                          lapse_rate,
                                                          c0_prior,
                                                          cf_prior,
                                                          cw_prior,
                                                          min_thresh_prior,
                                                          slope_prior,
                                                          lower_asymptote_prior,
                                                          lapse_rate_prior}) {}
};

void pyquestplus(py::module &m)
{

    py::enum_<qp::StimSelectionMethod>(m, "StimSelectionMethod", py::arithmetic())
        .value("MinEntropy", qp::StimSelectionMethod::MinEntropy)
        .value("MinNEntropy", qp::StimSelectionMethod::MinNEntropy);

    py::enum_<qp::ParamEstimationMethod>(m, "ParamEstimationMethod", py::arithmetic())
        .value("Mean", qp::ParamEstimationMethod::Mean)
        .value("Median", qp::ParamEstimationMethod::Median)
        .value("Mode", qp::ParamEstimationMethod::Mode);

    py::class_<PWeibull>(m, "Weibull")
        .def(py::init<svd, svd, svd, svd, svd, psydapt::Scale,
                      osvd, osvd, osvd, osvd, qp::StimSelectionMethod,
                      qp::ParamEstimationMethod, unsigned int,
                      unsigned int, unsigned int>(),
             "intensity"_a,
             "threshold"_a,
             "slope"_a = svd{3.5},
             "lower_asymptote"_a = svd{0.01},
             "lapse_rate"_a = svd{0.01},
             "stim_scale"_a = psydapt::Scale::Log10,
             "threshold_prior"_a = std::nullopt,
             "slope_prior"_a = std::nullopt,
             "lower_asymptote_prior"_a = std::nullopt,
             "lapse_rate_prior"_a = std::nullopt,
             "stim_selection_method"_a = qp::StimSelectionMethod::MinEntropy,
             "param_estimation_method"_a = qp::ParamEstimationMethod::Mean,
             "n"_a = 5,
             "max_consecutive_reps"_a = 2,
             "random_seed"_a = 1)
        .def("next", &PWeibull::next)
        .def("update", &PWeibull::update, "response"_a, "stimulus"_a = std::nullopt);

    py::class_<PNormCDF>(m, "NormCDF")
        .def(py::init<svd, svd, svd, svd, svd, psydapt::Scale,
                      osvd, osvd, osvd, osvd, qp::StimSelectionMethod,
                      qp::ParamEstimationMethod,
                      unsigned int, unsigned int, unsigned int>(),
             "intensity"_a,
             "location"_a,
             "scale"_a,
             "lower_asymptote"_a = svd{0.01},
             "lapse_rate"_a = svd{0.01},
             "stim_scale"_a = psydapt::Scale::Linear,
             "location_prior"_a = std::nullopt,
             "scale_prior"_a = std::nullopt,
             "lower_asymptote_prior"_a = std::nullopt,
             "lapse_rate_prior"_a = std::nullopt,
             "stim_selection_method"_a = qp::StimSelectionMethod::MinEntropy,
             "param_estimation_method"_a = qp::ParamEstimationMethod::Mean,
             "n"_a = 5,
             "max_consecutive_reps"_a = 2,
             "random_seed"_a = 1)
        .def("next", &PNormCDF::next)
        .def("update", &PNormCDF::update, "response"_a, "stimulus"_a = std::nullopt);

    py::class_<PCSF>(m, "CSF")
        .def(py::init<svd, svd, svd, svd, svd,
                      svd, svd, svd, svd, svd, psydapt::Scale,
                      osvd, osvd, osvd, osvd, osvd, osvd, osvd,
                      qp::StimSelectionMethod, qp::ParamEstimationMethod,
                      unsigned int, unsigned int, unsigned int>(),
             "contrast"_a,
             "spatial_freq"_a,
             "temporal_freq"_a,
             "c0"_a,
             "cf"_a,
             "cw"_a,
             "min_thresh"_a,
             "slope"_a = svd{3.5},
             "lower_asymptote"_a = svd{0.01},
             "lapse_rate"_a = svd{0.01},
             "stim_scale"_a = psydapt::Scale::Log10,
             "c0_prior"_a = std::nullopt,
             "cf_prior"_a = std::nullopt,
             "cw_prior"_a = std::nullopt,
             "min_thresh_prior"_a = std::nullopt,
             "slope_prior"_a = std::nullopt,
             "lower_asymptote_prior"_a = std::nullopt,
             "lapse_rate_prior"_a = std::nullopt,
             "stim_selection_method"_a = qp::StimSelectionMethod::MinEntropy,
             "param_estimation_method"_a = qp::ParamEstimationMethod::Mean,
             "n"_a = 5,
             "max_consecutive_reps"_a = 2,
             "random_seed"_a = 1)
        .def("next", &PCSF::next)
        .def("update", &PCSF::update, "response"_a, "stimulus"_a = std::nullopt);
};