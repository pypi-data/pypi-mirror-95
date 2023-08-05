
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\src\include\frc2\command\PIDCommand.h>

#include <frc2/command/Command.h>
#include <frc2/command/Subsystem.h>




#include <rpygen/frc2__CommandBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc2__PIDCommand = 
    Pyfrc2__CommandBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc2__PIDCommand : PyBasefrc2__PIDCommand<PyTrampolineBase, CxxBase> {
    using PyBasefrc2__PIDCommand<PyTrampolineBase, CxxBase>::PyBasefrc2__PIDCommand;



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



    using frc2::PIDCommand::m_controller;

    using frc2::PIDCommand::m_measurement;
using frc2::PIDCommand::m_setpoint;
using frc2::PIDCommand::m_useOutput;

};

}; // namespace rpygen
