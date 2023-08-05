
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\src\include\frc2\command\TrapezoidProfileSubsystem.h>





#include <rpygen/frc2__SubsystemBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc2__TrapezoidProfileSubsystem = 
    Pyfrc2__SubsystemBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename Distance, typename CxxBase = PyTrampolineBase>
struct Pyfrc2__TrapezoidProfileSubsystem : PyBasefrc2__TrapezoidProfileSubsystem<PyTrampolineBase, CxxBase> {
    using PyBasefrc2__TrapezoidProfileSubsystem<PyTrampolineBase, CxxBase>::PyBasefrc2__TrapezoidProfileSubsystem;


using Distance_t = units::unit_t<Distance>;
#ifndef RPYGEN_DISABLE_Periodic_v
    void Periodic() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "periodic", Periodic,);    }
#endif

#ifndef RPYGEN_DISABLE_UseState_TState
    void UseState(typename frc::TrapezoidProfile<Distance >::State state) override {
RPYBUILD_OVERRIDE_PURE_NAME(TrapezoidProfileSubsystem,PYBIND11_TYPE(void), CxxBase, "_useState", UseState,state);    }
#endif


#ifndef RPYBLD_DISABLE_Enable_v
  #ifndef RPYBLD_UDISABLE_frc2__TrapezoidProfileSubsystem_Enable
    using frc2::TrapezoidProfileSubsystem<Distance>::Enable;
    #define RPYBLD_UDISABLE_frc2__TrapezoidProfileSubsystem_Enable
  #endif
#endif
#ifndef RPYBLD_DISABLE_Disable_v
  #ifndef RPYBLD_UDISABLE_frc2__TrapezoidProfileSubsystem_Disable
    using frc2::TrapezoidProfileSubsystem<Distance>::Disable;
    #define RPYBLD_UDISABLE_frc2__TrapezoidProfileSubsystem_Disable
  #endif
#endif


};

}; // namespace rpygen


namespace rpygen {

using namespace frc2;


template <typename Distance>
struct bind_frc2__TrapezoidProfileSubsystem {

          using Distance_t = units::unit_t<Distance>;


      using TrapezoidProfileSubsystem_Trampoline = rpygen::Pyfrc2__TrapezoidProfileSubsystem<typename frc2::TrapezoidProfileSubsystem<Distance>, Distance>;
py::class_<typename frc2::TrapezoidProfileSubsystem<Distance>, std::shared_ptr<typename frc2::TrapezoidProfileSubsystem<Distance>>, TrapezoidProfileSubsystem_Trampoline, SubsystemBase> cls_TrapezoidProfileSubsystem;




    py::module &m;
    std::string clsName;

bind_frc2__TrapezoidProfileSubsystem(py::module &m, const char * clsName) :
    cls_TrapezoidProfileSubsystem(m, clsName),



    m(m),
    clsName(clsName)
{}

void finish(const char * set_doc = NULL, const char * add_doc = NULL) {

    
  cls_TrapezoidProfileSubsystem.doc() =
    "A subsystem that generates and runs trapezoidal motion profiles\n"
"automatically.  The user specifies how to use the current state of the motion\n"
"profile by overriding the `UseState` method.";

  cls_TrapezoidProfileSubsystem
      .def(py::init<typename frc::TrapezoidProfile<Distance >::Constraints, units::unit_t<Distance >, units::second_t>(),
      py::arg("constraints"), py::arg("initialPosition")=Distance_t{ 0}, py::arg("period")=20_ms, release_gil(), py::doc(
    "Creates a new TrapezoidProfileSubsystem.\n"
"\n"
":param constraints:     The constraints (maximum velocity and acceleration)\n"
"                        for the profiles.\n"
":param initialPosition: The initial position of the controller mechanism\n"
"                        when the subsystem is constructed.\n"
":param period:          The period of the main robot loop, in seconds.")
  )
    
      .def("periodic", &frc2::TrapezoidProfileSubsystem<Distance>::Periodic, release_gil()
  )
    
      .def("setGoal", static_cast<void (frc2::TrapezoidProfileSubsystem<Distance>::*)(typename frc::TrapezoidProfile<Distance >::State)>(
&frc2::TrapezoidProfileSubsystem<Distance>::SetGoal),
      py::arg("goal"), release_gil(), py::doc(
    "Sets the goal state for the subsystem.\n"
"\n"
":param goal: The goal state for the subsystem's motion profile.")
  )
    
      .def("setGoal", static_cast<void (frc2::TrapezoidProfileSubsystem<Distance>::*)(units::unit_t<Distance >)>(
&frc2::TrapezoidProfileSubsystem<Distance>::SetGoal),
      py::arg("goal"), release_gil(), py::doc(
    "Sets the goal state for the subsystem.  Goal velocity assumed to be zero.\n"
"\n"
":param goal: The goal position for the subsystem's motion profile.")
  )
    
      .def("_useState", static_cast<void (frc2::TrapezoidProfileSubsystem<Distance>::*)(typename frc::TrapezoidProfile<Distance >::State)>(&TrapezoidProfileSubsystem_Trampoline::UseState),
      py::arg("state"), release_gil(), py::doc(
    "Users should override this to consume the current state of the motion\n"
"profile.\n"
"\n"
":param state: The current state of the motion profile.")
  )
    
      .def("_enable", static_cast<void (frc2::TrapezoidProfileSubsystem<Distance>::*)()>(&TrapezoidProfileSubsystem_Trampoline::Enable), release_gil(), py::doc(
    "Enable the TrapezoidProfileSubsystem's output.")
  )
    
      .def("_disable", static_cast<void (frc2::TrapezoidProfileSubsystem<Distance>::*)()>(&TrapezoidProfileSubsystem_Trampoline::Disable), release_gil(), py::doc(
    "Disable the TrapezoidProfileSubsystem's output.")
  )
    
;

  

    if (set_doc) {
        cls_TrapezoidProfileSubsystem.doc() = set_doc;
    }
    if (add_doc) {
        cls_TrapezoidProfileSubsystem.doc() = py::cast<std::string>(cls_TrapezoidProfileSubsystem.doc()) + add_doc;
    }

    
}

}; // struct bind_frc2__TrapezoidProfileSubsystem

}; // namespace rpygen