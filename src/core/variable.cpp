#include <string>
#include <carl/core/Variable.h>
#include <carl/core/VariablePool.h>

#include "variable.h"
#include "src/helpers.h"
#include "src/types.h"


carl::Variable getOrCreateVariable(std::string const & name, carl::VariableType type) {
    // Variables are constructed by the Pool. Note that for a given name,
    // two Variable instances may differ, but refer to the same id (data)
    auto& pool = carl::VariablePool::getInstance();
    carl::Variable res = pool.findVariableWithName(name);
    if (res != carl::Variable::NO_VARIABLE) {
        return res;
    }
    return freshVariable(name, type);
}

void define_variabletype(py::module& m) {
    py::enum_<carl::VariableType>(m, "VariableType")
        .value("BOOL", carl::VariableType::VT_BOOL)
        .value("INT", carl::VariableType::VT_INT)
        .value("REAL", carl::VariableType::VT_REAL);
}

void define_variable(py::module& m) {

    py::class_<carl::Variable>(m, "Variable")
        .def("__init__", [](carl::Variable &instance, carl::Variable const& other) {
                new(&instance) carl::Variable(other);
            })
        .def("__init__", [](carl::Variable &instance, std::string name, carl::VariableType type) {
                carl::Variable tmp = freshVariable(name, type);
                new(&instance) carl::Variable(tmp);
            }, py::arg("name"), py::arg("type") = carl::VariableType::VT_REAL)
        .def("__init__", [](carl::Variable &instance, carl::VariableType type) {
                carl::Variable tmp = freshVariable(type);
                new (&instance) carl::Variable(tmp);
            }, py::arg("type") = carl::VariableType::VT_REAL)

        .def("__mul__",  static_cast<Monomial::Arg (*)(carl::Variable, carl::Variable)>(&carl::operator*))


        .def(py::self == py::self)
        .def(py::self != py::self)
        .def(py::self < py::self)
        .def(py::self <= py::self)
        .def(py::self > py::self)
        .def(py::self >= py::self)

        .def_property_readonly("name", [](const carl::Variable& r) -> std::string {
                if (r != carl::Variable::NO_VARIABLE) {
                    return r.name();
                } else {
                    return std::string("__NOVAR__");
                }
            })
        .def_property_readonly("type", &carl::Variable::type)
        .def_property_readonly("id", &carl::Variable::id)
        .def_property_readonly("rank", &carl::Variable::rank)
        .def("__repr__", [](const carl::Variable& r)  { if (r != carl::Variable::NO_VARIABLE) { return "<Variable " + r.name() + " [id = " + std::to_string(r.id()) + "]>"; } else { return std::string("<NOVARIABLE>");} })
        .def("__str__", &streamToString<carl::Variable>)
        .def_property_readonly("is_no_variable", [](const carl::Variable& v) {return v == carl::Variable::NO_VARIABLE;})
            // TODO get state has an issue if there are several variables with the same name; they cannot be distinguished afterwards
        .def("__getstate__", [](const carl::Variable& v) { return std::make_tuple<std::string, std::string>(v.name(), carl::to_string(v.type()));})

        .def("__setstate__", [](carl::Variable& v, const std::tuple<std::string, std::string>& data ) {
                carl::Variable tmp = getOrCreateVariable(std::get<0>(data), carl::variableTypeFromString(std::get<1>(data)));
                new(&v) carl::Variable(tmp);
            })
        .def("__hash__", [](const carl::Variable& v) { std::hash<carl::Variable> h; return h(v);})

    ;

    m.def("variable_with_name", [](std::string const& name){
            return carl::VariablePool::getInstance().findVariableWithName(name);
        }, "Get a variable from the pool with the given name.");


    m.def("clear_variable_pool", [](){
            carl::VariablePool::getInstance().clear();
        }, "Clear variable pool and remove all variables");
}
