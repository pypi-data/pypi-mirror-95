// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#include "frc2/command/CommandBase.h"

#include <frc/smartdashboard/SendableBuilder.h>
#include <frc/smartdashboard/SendableRegistry.h>

using namespace frc2;

CommandBase::CommandBase() {
  frc::SendableRegistry::GetInstance().Add(this, GetTypeName(*this));
}

void CommandBase::AddRequirements(
    std::initializer_list<std::shared_ptr<Subsystem>> requirements) {
  m_requirements.insert(requirements.begin(), requirements.end());
}

void CommandBase::AddRequirements(wpi::ArrayRef<std::shared_ptr<Subsystem>> requirements) {
  m_requirements.insert(requirements.begin(), requirements.end());
}

void CommandBase::AddRequirements(wpi::SmallSet<std::shared_ptr<Subsystem>, 4> requirements) {
  m_requirements.insert(requirements.begin(), requirements.end());
}

wpi::SmallSet<std::shared_ptr<Subsystem>, 4> CommandBase::GetRequirements() const {
  return m_requirements;
}

void CommandBase::SetName(const wpi::Twine& name) {
  frc::SendableRegistry::GetInstance().SetName(this, name);
}

std::string CommandBase::GetName() const {
  return frc::SendableRegistry::GetInstance().GetName(this);
}

std::string CommandBase::GetSubsystem() const {
  return frc::SendableRegistry::GetInstance().GetSubsystem(this);
}

void CommandBase::SetSubsystem(const wpi::Twine& subsystem) {
  frc::SendableRegistry::GetInstance().SetSubsystem(this, subsystem);
}

void CommandBase::InitSendable(frc::SendableBuilder& builder) {
  builder.SetSmartDashboardType("Command");
  builder.AddStringProperty(
      ".name", [this] { return GetName(); }, nullptr);
  builder.AddBooleanProperty(
      "running", [this] { return IsScheduled(); },
      [this](bool value) {
        bool isScheduled = IsScheduled();
        if (value && !isScheduled) {
          Schedule();
        } else if (!value && isScheduled) {
          Cancel();
        }
      });
}
