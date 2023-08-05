// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <type_traits>
#include <utility>

#include "frc2/command/CommandScheduler.h"

namespace frc2 {
class Command;
/**
 * A robot subsystem.  Subsystems are the basic unit of robot organization in
 * the Command-based framework; they encapsulate low-level hardware objects
 * (motor controllers, sensors, etc) and provide methods through which they can
 * be used by Commands.  Subsystems are used by the CommandScheduler's resource
 * management system to ensure multiple robot actions are not "fighting" over
 * the same hardware; Commands that use a subsystem should include that
 * subsystem in their GetRequirements() method, and resources used within a
 * subsystem should generally remain encapsulated and not be shared by other
 * parts of the robot.
 *
 * <p>Subsystems must be registered with the scheduler with the
 * CommandScheduler.RegisterSubsystem() method in order for the
 * Periodic() method to be called.  It is recommended that this method be called
 * from the constructor of users' Subsystem implementations.  The
 * SubsystemBase class offers a simple base for user implementations
 * that handles this.
 *
 * @see Command
 * @see CommandScheduler
 * @see SubsystemBase
 */
class Subsystem : public std::enable_shared_from_this<Subsystem> {
 public:
  ~Subsystem();
  /**
   * This method is called periodically by the CommandScheduler.  Useful for
   * updating subsystem-specific state that you don't want to offload to a
   * Command.  Teams should try to be consistent within their own codebases
   * about which responsibilities will be handled by Commands, and which will be
   * handled here.
   */
  virtual void Periodic();

  /**
   * This method is called periodically by the CommandScheduler.  Useful for
   * updating subsystem-specific state that needs to be maintained for
   * simulations, such as for updating simulation classes and setting simulated
   * sensor readings.
   */
  virtual void SimulationPeriodic();

  /**
   * Sets the default Command of the subsystem.  The default command will be
   * automatically scheduled when no other commands are scheduled that require
   * the subsystem. Default commands should generally not end on their own, i.e.
   * their IsFinished() method should always return false.  Will automatically
   * register this subsystem with the CommandScheduler.
   *
   * @param defaultCommand the default command to associate with this subsystem
   */
  template <class T>
  void SetDefaultCommand(T defaultCommand) {
    CommandScheduler::GetInstance().SetDefaultCommand(shared_from_this(), defaultCommand);
  }

  /**
   * Gets the default command for this subsystem.  Returns null if no default
   * command is currently associated with the subsystem.
   *
   * @return the default command associated with this subsystem
   */
  std::shared_ptr<Command> GetDefaultCommand();

  /**
   * Returns the command currently running on this subsystem.  Returns null if
   * no command is currently scheduled that requires this subsystem.
   *
   * @return the scheduled command currently requiring this subsystem
   */
  std::shared_ptr<Command> GetCurrentCommand();

  /**
   * Registers this subsystem with the CommandScheduler, allowing its
   * Periodic() method to be called when the scheduler runs.
   */
  void Register();
};
}  // namespace frc2
