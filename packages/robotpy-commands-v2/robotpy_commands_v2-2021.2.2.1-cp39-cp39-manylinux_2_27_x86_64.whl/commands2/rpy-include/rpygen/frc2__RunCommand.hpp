
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <../src/include/frc2/command/RunCommand.h>

#include <frc2/command/Command.h>
#include <frc2/command/Subsystem.h>
#include <src/helpers.h>




#include <rpygen/frc2__CommandBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc2__RunCommand = 
    Pyfrc2__CommandBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc2__RunCommand : PyBasefrc2__RunCommand<PyTrampolineBase, CxxBase> {
    using PyBasefrc2__RunCommand<PyTrampolineBase, CxxBase>::PyBasefrc2__RunCommand;



#ifndef RPYGEN_DISABLE_Execute_v
    void Execute() override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(void), CxxBase, "execute", Execute,);    }
#endif




    using frc2::RunCommand::m_toRun;

};

}; // namespace rpygen
