
 

// This file is autogenerated. DO NOT EDIT

#pragma once
#include <robotpy_build.h>


#include <..\src\include\frc2\command\Command.h>

#include <frc2/command/ParallelCommandGroup.h>
#include <frc2/command/ParallelRaceGroup.h>
#include <frc2/command/ParallelDeadlineGroup.h>
#include <frc2/command/SequentialCommandGroup.h>
#include <frc2/command/PerpetualCommand.h>
#include <frc2/command/ProxyScheduleCommand.h>
#include <src/helpers.h>




#include <rpygen/frc__ErrorBase.hpp>

namespace rpygen {

using namespace frc2;


template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
using PyBasefrc2__Command = 
    Pyfrc__ErrorBase<
        PyTrampolineBase
    
    , CxxBase
    >
;

template <typename PyTrampolineBase, typename CxxBase = PyTrampolineBase>
struct Pyfrc2__Command : PyBasefrc2__Command<PyTrampolineBase, CxxBase> {
    using PyBasefrc2__Command<PyTrampolineBase, CxxBase>::PyBasefrc2__Command;



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

#ifndef RPYGEN_DISABLE_KGetRequirements_v
    wpi::SmallSet<std::shared_ptr<Subsystem>, 4 > GetRequirements() const override {
RPYBUILD_OVERRIDE_PURE_NAME(Command,PYBIND11_TYPE(wpi::SmallSet<std::shared_ptr<Subsystem>, 4 >), CxxBase, "getRequirements", GetRequirements,);    }
#endif

#ifndef RPYGEN_DISABLE_KRunsWhenDisabled_v
    bool RunsWhenDisabled() const override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(bool), CxxBase, "runsWhenDisabled", RunsWhenDisabled,);    }
#endif

#ifndef RPYGEN_DISABLE_KGetName_v
    std::string GetName() const override {
PYBIND11_OVERRIDE_NAME(PYBIND11_TYPE(std::string), CxxBase, "getName", GetName,);    }
#endif



    using frc2::Command::m_isGrouped;

};

}; // namespace rpygen
