# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.12

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

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/noah/.local/share/JetBrains/Toolbox/apps/CLion/ch-0/182.3911.40/bin/cmake/linux/bin/cmake

# The command to remove a file.
RM = /home/noah/.local/share/JetBrains/Toolbox/apps/CLion/ch-0/182.3911.40/bin/cmake/linux/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/noah/starid

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/noah/starid

# Include any dependencies generated for this target.
include libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/depend.make

# Include the progress variables for this target.
include libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/progress.make

# Include the compile flags for this target's objects.
include libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/flags.make

libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/pod.cpp.o: libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/flags.make
libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/pod.cpp.o: libstarid/cereal-1.2.2/unittests/pod.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/noah/starid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/pod.cpp.o"
	cd /home/noah/starid/libstarid/cereal-1.2.2/unittests && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/coverage_pod.dir/pod.cpp.o -c /home/noah/starid/libstarid/cereal-1.2.2/unittests/pod.cpp

libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/pod.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/coverage_pod.dir/pod.cpp.i"
	cd /home/noah/starid/libstarid/cereal-1.2.2/unittests && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/noah/starid/libstarid/cereal-1.2.2/unittests/pod.cpp > CMakeFiles/coverage_pod.dir/pod.cpp.i

libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/pod.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/coverage_pod.dir/pod.cpp.s"
	cd /home/noah/starid/libstarid/cereal-1.2.2/unittests && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/noah/starid/libstarid/cereal-1.2.2/unittests/pod.cpp -o CMakeFiles/coverage_pod.dir/pod.cpp.s

# Object files for target coverage_pod
coverage_pod_OBJECTS = \
"CMakeFiles/coverage_pod.dir/pod.cpp.o"

# External object files for target coverage_pod
coverage_pod_EXTERNAL_OBJECTS =

coverage/coverage_pod: libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/pod.cpp.o
coverage/coverage_pod: libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/build.make
coverage/coverage_pod: libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/noah/starid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../../../coverage/coverage_pod"
	cd /home/noah/starid/libstarid/cereal-1.2.2/unittests && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/coverage_pod.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/build: coverage/coverage_pod

.PHONY : libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/build

libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/clean:
	cd /home/noah/starid/libstarid/cereal-1.2.2/unittests && $(CMAKE_COMMAND) -P CMakeFiles/coverage_pod.dir/cmake_clean.cmake
.PHONY : libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/clean

libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/depend:
	cd /home/noah/starid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/noah/starid /home/noah/starid/libstarid/cereal-1.2.2/unittests /home/noah/starid /home/noah/starid/libstarid/cereal-1.2.2/unittests /home/noah/starid/libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : libstarid/cereal-1.2.2/unittests/CMakeFiles/coverage_pod.dir/depend

