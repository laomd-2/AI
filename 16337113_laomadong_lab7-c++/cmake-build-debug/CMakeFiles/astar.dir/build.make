# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.12

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "D:\Program Files\JetBrains\CLion 2018.2.5\bin\cmake\win\bin\cmake.exe"

# The command to remove a file.
RM = "D:\Program Files\JetBrains\CLion 2018.2.5\bin\cmake\win\bin\cmake.exe" -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = D:\learning\ai\lab\16337113_laomadong_lab7-c++

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = D:\learning\ai\lab\16337113_laomadong_lab7-c++\cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/astar.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/astar.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/astar.dir/flags.make

CMakeFiles/astar.dir/code/astar/main.cpp.obj: CMakeFiles/astar.dir/flags.make
CMakeFiles/astar.dir/code/astar/main.cpp.obj: ../code/astar/main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=D:\learning\ai\lab\16337113_laomadong_lab7-c++\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/astar.dir/code/astar/main.cpp.obj"
	"D:\Program Files\mingw64\bin\g++.exe"  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\astar.dir\code\astar\main.cpp.obj -c D:\learning\ai\lab\16337113_laomadong_lab7-c++\code\astar\main.cpp

CMakeFiles/astar.dir/code/astar/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/astar.dir/code/astar/main.cpp.i"
	"D:\Program Files\mingw64\bin\g++.exe" $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E D:\learning\ai\lab\16337113_laomadong_lab7-c++\code\astar\main.cpp > CMakeFiles\astar.dir\code\astar\main.cpp.i

CMakeFiles/astar.dir/code/astar/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/astar.dir/code/astar/main.cpp.s"
	"D:\Program Files\mingw64\bin\g++.exe" $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S D:\learning\ai\lab\16337113_laomadong_lab7-c++\code\astar\main.cpp -o CMakeFiles\astar.dir\code\astar\main.cpp.s

# Object files for target astar
astar_OBJECTS = \
"CMakeFiles/astar.dir/code/astar/main.cpp.obj"

# External object files for target astar
astar_EXTERNAL_OBJECTS =

astar.exe: CMakeFiles/astar.dir/code/astar/main.cpp.obj
astar.exe: CMakeFiles/astar.dir/build.make
astar.exe: CMakeFiles/astar.dir/linklibs.rsp
astar.exe: CMakeFiles/astar.dir/objects1.rsp
astar.exe: CMakeFiles/astar.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=D:\learning\ai\lab\16337113_laomadong_lab7-c++\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable astar.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\astar.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/astar.dir/build: astar.exe

.PHONY : CMakeFiles/astar.dir/build

CMakeFiles/astar.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\astar.dir\cmake_clean.cmake
.PHONY : CMakeFiles/astar.dir/clean

CMakeFiles/astar.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" D:\learning\ai\lab\16337113_laomadong_lab7-c++ D:\learning\ai\lab\16337113_laomadong_lab7-c++ D:\learning\ai\lab\16337113_laomadong_lab7-c++\cmake-build-debug D:\learning\ai\lab\16337113_laomadong_lab7-c++\cmake-build-debug D:\learning\ai\lab\16337113_laomadong_lab7-c++\cmake-build-debug\CMakeFiles\astar.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/astar.dir/depend
