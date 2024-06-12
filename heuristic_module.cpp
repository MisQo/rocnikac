#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "heuristic.cpp"


PYBIND11_MODULE(heuristicGenerateMove, m) {
    m.def("generate_move", &generate_move, "generate_move",
        pybind11::arg("signal"), pybind11::arg("sequence"), pybind11::arg("l"), pybind11::arg("r"), pybind11::arg("width"));
}