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
include libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/depend.make

# Include the progress variables for this target.
include libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/progress.make

# Include the compile flags for this target's objects.
include libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/flags.make

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/base.cpp.o: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/flags.make
libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/base.cpp.o: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/base.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/noah/starid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/base.cpp.o"
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/sandbox_vs_dll.dir/base.cpp.o -c /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/base.cpp

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/base.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/sandbox_vs_dll.dir/base.cpp.i"
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/base.cpp > CMakeFiles/sandbox_vs_dll.dir/base.cpp.i

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/base.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/sandbox_vs_dll.dir/base.cpp.s"
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/base.cpp -o CMakeFiles/sandbox_vs_dll.dir/base.cpp.s

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/derived.cpp.o: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/flags.make
libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/derived.cpp.o: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/derived.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/noah/starid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/derived.cpp.o"
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/sandbox_vs_dll.dir/derived.cpp.o -c /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/derived.cpp

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/derived.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/sandbox_vs_dll.dir/derived.cpp.i"
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/derived.cpp > CMakeFiles/sandbox_vs_dll.dir/derived.cpp.i

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/derived.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/sandbox_vs_dll.dir/derived.cpp.s"
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/derived.cpp -o CMakeFiles/sandbox_vs_dll.dir/derived.cpp.s

# Object files for target sandbox_vs_dll
sandbox_vs_dll_OBJECTS = \
"CMakeFiles/sandbox_vs_dll.dir/base.cpp.o" \
"CMakeFiles/sandbox_vs_dll.dir/derived.cpp.o"

# External object files for target sandbox_vs_dll
sandbox_vs_dll_EXTERNAL_OBJECTS =

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/libsandbox_vs_dll.so: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/base.cpp.o
libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/libsandbox_vs_dll.so: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/derived.cpp.o
libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/libsandbox_vs_dll.so: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/build.make
libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/libsandbox_vs_dll.so: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/noah/starid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX shared library libsandbox_vs_dll.so"
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/sandbox_vs_dll.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/build: libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/libsandbox_vs_dll.so

.PHONY : libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/build

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/clean:
	cd /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib && $(CMAKE_COMMAND) -P CMakeFiles/sandbox_vs_dll.dir/cmake_clean.cmake
.PHONY : libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/clean

libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/depend:
	cd /home/noah/starid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/noah/starid /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib /home/noah/starid /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib /home/noah/starid/libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : libstarid/cereal-1.2.2/sandbox/sandbox_shared_lib/CMakeFiles/sandbox_vs_dll.dir/depend

