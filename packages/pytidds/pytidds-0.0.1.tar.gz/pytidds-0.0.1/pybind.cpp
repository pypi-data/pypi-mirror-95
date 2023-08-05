/*
 * Copyright (c) 2021 Alex Yu
 * All rights reserved.
 *
 * This library is free software; you can redistribute it and/or modify it under
 * the terms of the GNU Lesser General Public License version 2.1 as published
 * by the Free Software Foundation.
 *
 * This library is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 * details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#include "tidds/ddsbase.h"

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <string>
#include <cstdlib>
#include <memory>
#include <vector>
#include <tuple>
#include <cstdint>

namespace pybind11 {
namespace detail {
namespace {
struct float16 {
    uint16_t data;
};
}  // namespace
template <>
struct npy_format_descriptor<float16> {
    static const int NPY_FLOAT16 = 23;
    static pybind11::dtype dtype() {
        handle ptr = npy_api::get().PyArray_DescrFromType_(NPY_FLOAT16);
        return reinterpret_borrow<pybind11::dtype>(ptr);
    }
    static std::string format() { return "e"; }
    static constexpr auto name = _("float16");
};
}  // namespace detail
}  // namespace pybind11

namespace py = pybind11;

namespace {
struct DDSReadBuffer {
    uint8_t *data;
    const std::vector<size_t> shape;
    DDSReadBuffer(uint8_t *data, const std::vector<size_t> &shape)
        : data(data), shape(shape) {}

    py::array_t<uint8_t> u8() {
        _calc_stride();
        return py::array_t<uint8_t>(
            shape, _strides, data, py::capsule(data, [](void *f) {
                std::free(reinterpret_cast<uint8_t *>(f));
            }));
    }
    py::array_t<uint16_t> u16() {
        _calc_stride();
        std::vector<size_t> nshape = shape;
        std::vector<size_t> nstrides = _strides;
        if (shape.size()) {
            if (shape.back() & 1)
                throw std::invalid_argument("Components not divisible by 2");
            nshape.back() /= 2;
            nstrides.back() = 2;
        }
        return py::array_t<uint16_t>(
            nshape, nstrides, reinterpret_cast<uint16_t *>(data),
            py::capsule(data, [](void *f) {
                std::free(reinterpret_cast<uint8_t *>(f));
            }));
    }
    py::array_t<uint32_t> u32() {
        _calc_stride();
        std::vector<size_t> nshape = shape;
        std::vector<size_t> nstrides = _strides;
        if (shape.size()) {
            if (shape.back() & 3)
                throw std::invalid_argument("Components not divisible by 4");
            nshape.back() /= 4;
            nstrides.back() = 4;
        }
        return py::array_t<uint32_t>(
            nshape, nstrides, reinterpret_cast<uint32_t *>(data),
            py::capsule(data, [](void *f) {
                std::free(reinterpret_cast<uint8_t *>(f));
            }));
    }
    py::array_t<py::detail::float16> f16() {
        _calc_stride();
        std::vector<size_t> nshape = shape;
        std::vector<size_t> nstrides = _strides;
        if (shape.size()) {
            if (shape.back() & 1)
                throw std::invalid_argument("Components not divisible by 2");
            nshape.back() /= 2;
            nstrides.back() = 2;
        }
        return py::array_t<py::detail::float16>(
            nshape, nstrides, reinterpret_cast<py::detail::float16 *>(data),
            py::capsule(data, [](void *f) {
                std::free(reinterpret_cast<uint8_t *>(f));
            }));
    }
    py::array_t<float> f32() {
        _calc_stride();
        std::vector<size_t> nshape = shape;
        std::vector<size_t> nstrides = _strides;
        if (shape.size()) {
            if (shape.back() & 3)
                throw std::invalid_argument("Components not divisible by 4");
            nshape.back() /= 4;
            nstrides.back() = 4;
        }
        return py::array_t<float>(nshape, nstrides,
                                  reinterpret_cast<float *>(data),
                                  py::capsule(data, [](void *f) {
                                      std::free(reinterpret_cast<uint8_t *>(f));
                                  }));
    }

    py::buffer_info get_buffer() {
        _calc_stride();
        return py::buffer_info(data, 1,
                               py::format_descriptor<uint8_t>::format(),
                               shape.size(), shape, _strides);
    }

   private:
    std::vector<size_t> _strides;
    void _calc_stride() {
        if (_strides.empty()) {
            _strides.resize(shape.size());
            if (shape.size()) {
                _strides.back() = 1u;
                for (size_t i = shape.size() - 2; ~i; --i)
                    _strides[i] = _strides[i + 1] * shape[i + 1];
            }
        }
    }
};

// ** UTILS

// ** READ
DDSReadBuffer _readRAWfile(const std::string &path) {
    size_t nbytes;
    uint8_t *data = readRAWfile(path.c_str(), &nbytes);
    return DDSReadBuffer{data, {nbytes}};
}

DDSReadBuffer _readDDSfile(const std::string &path) {
    size_t nbytes;
    uint8_t *data = readDDSfile(path.c_str(), &nbytes);
    return DDSReadBuffer{data, {nbytes}};
}

std::tuple<DDSReadBuffer, std::tuple<float, float, float>> _readPVMvolume(
    const std::string &path) {
    uint32_t width, height, depth, comps;
    float scalex, scaley, scalez;
    uint8_t *data = readPVMvolume(path.c_str(), &width, &height, &depth, &comps,
                                  &scalex, &scaley, &scalez);
    return {DDSReadBuffer{data, {width, height, depth, comps}},
            std::make_tuple(scalex, scaley, scalez)};
}

DDSReadBuffer _readPNMimage(const std::string &path) {
    uint32_t width, height, comps;
    uint8_t *data = readPNMimage(path.c_str(), &width, &height, &comps);
    return DDSReadBuffer{data, {width, height, comps}};
}

// * WRITING
void _writeRAWfile(const std::string &path, py::buffer arr) {
    py::buffer_info arr_info = arr.request();
    writeRAWfile(path.c_str(), reinterpret_cast<uint8_t *>(arr_info.ptr),
                 arr_info.size * arr_info.itemsize, 1);
}
void _writeDDSfile(const std::string &path, py::buffer arr) {
    py::buffer_info arr_info = arr.request();
    writeDDSfile(path.c_str(), reinterpret_cast<uint8_t *>(arr_info.ptr),
                 arr_info.size * arr_info.itemsize, 0, 0, 1);
}
void _writePVMvolume(const std::string &path, py::buffer arr,
                     std::tuple<float, float, float> scale = {1.f, 1.f, 1.f}) {
    py::buffer_info arr_info = arr.request();
    if (arr_info.ndim != 4) {
        throw std::invalid_argument("Volumetric array must be WxHxDxC");
    }
    writePVMvolume(path.c_str(), reinterpret_cast<uint8_t *>(arr_info.ptr),
                   arr_info.shape[0], arr_info.shape[1], arr_info.shape[2],
                   arr_info.shape[3] * arr_info.itemsize, std::get<0>(scale),
                   std::get<1>(scale), std::get<2>(scale));
}
void _writePNMImage(const std::string &path, py::buffer arr, bool dds = false) {
    py::buffer_info arr_info = arr.request();
    if (arr_info.ndim != 3) {
        throw std::invalid_argument("Image array must be WxHxC");
    }
    writePNMimage(path.c_str(), reinterpret_cast<uint8_t *>(arr_info.ptr),
                  arr_info.shape[0], arr_info.shape[1],
                  arr_info.shape[2] * arr_info.itemsize, dds);
}
}  // namespace

PYBIND11_MODULE(tidds, m) {
    m.doc() = R"pbdoc(DDS)pbdoc";
    py::class_<DDSReadBuffer>(m, "_DDSReadBuffer", py::buffer_protocol())
        .def_readonly("shape", &DDSReadBuffer::shape)
        .def_buffer(&DDSReadBuffer::get_buffer)
        .def("u8", &DDSReadBuffer::u8)
        .def("u16", &DDSReadBuffer::u16)
        .def("u32", &DDSReadBuffer::u32)
        .def("f16", &DDSReadBuffer::f16)
        .def("f32", &DDSReadBuffer::f32)
        .def("__repr__", [](DDSReadBuffer &buf) {
            std::string s = "tidds._DDSReadBuffer(shape=[";
            for (size_t i = 0; i < buf.shape.size(); ++i) {
                if (i) s.append(", ");
                s.append(std::to_string(buf.shape[i]));
            }
            s.append("])");
            return s;
        });

    m.def("readRAWfile", _readRAWfile, py::arg("path"));
    m.def("readDDSfile", _readDDSfile, py::arg("path"));
    m.def("readPVMvolume", _readPVMvolume, py::arg("path"));
    m.def("readPNMimage", _readPNMimage, py::arg("path"));

    m.def("writeRAWfile", _writeRAWfile, py::arg("path"), py::arg("arr"));
    m.def("writeDDSfile", _writeDDSfile, py::arg("path"), py::arg("arr"));
    m.def("writePVMvolume", _writePVMvolume, py::arg("path"), py::arg("arr"),
          py::arg("scale") = std::make_tuple(1.f, 1.f, 1.f));
    m.def("writePNMimage", _writePNMImage, py::arg("path"), py::arg("arr"),
          py::arg("dds") = false);
}
