
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\src\include\frc2\command\SequentialCommandGroup.h>

#include <frc2/command/Command.h>
#include <frc2/command/Subsystem.h>
#include <src/helpers.h>


#define RPYGEN_DISABLE_AddCommands_OTshared_ptr_Command__


#include <rpygen/frc2__CommandGroupBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc2__SequentialCommandGroup = 
    Pyfrc2__CommandGroupBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc2__SequentialCommandGroup : PyBasefrc2__SequentialCommandGroup<PyTrampolineBase, CxxBase> {
    using PyBasefrc2__SequentialCommandGroup<PyTrampolineBase, CxxBase>::PyBasefrc2__SequentialCommandGroup;



#ifndef RPYGEN_DISABLE_Initialize_v
    void Initialize() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "initialize", Initialize,);    }
#endif

#ifndef RPYGEN_DISABLE_Execute_v
    void Execute() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "execute", Execute,);    }
#endif

#ifndef RPYGEN_DISABLE_End_b
    void End(bool interrupted) override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "end", End,interrupted);    }
#endif

#ifndef RPYGEN_DISABLE_IsFinished_v
    bool IsFinished() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(bool), CxxBase, "isFinished", IsFinished,);    }
#endif

#ifndef RPYGEN_DISABLE_KRunsWhenDisabled_v
    bool RunsWhenDisabled() const override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(bool), CxxBase, "runsWhenDisabled", RunsWhenDisabled,);    }
#endif




};

}; // namespace rpygen
