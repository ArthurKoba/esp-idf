include($ENV{IDF_PATH}/tools/cmake/utilities.cmake)

set(CMAKE_SYSTEM_NAME Generic)

set(CMAKE_C_COMPILER riscv32-esp-elf-gcc)
set(CMAKE_CXX_COMPILER riscv32-esp-elf-g++)
set(CMAKE_ASM_COMPILER riscv32-esp-elf-gcc)
set(_CMAKE_TOOLCHAIN_PREFIX riscv32-esp-elf-)

remove_duplicated_flags("-march=rv32imafc_zicsr_zifencei_xesppie -mabi=ilp32f ${CMAKE_C_FLAGS}" UNIQ_CMAKE_C_FLAGS)
set(CMAKE_C_FLAGS "${UNIQ_CMAKE_C_FLAGS}" CACHE STRING "C Compiler Base Flags" FORCE)
remove_duplicated_flags("-march=rv32imafc_zicsr_zifencei_xesppie -mabi=ilp32f ${CMAKE_CXX_FLAGS}" UNIQ_CMAKE_CXX_FLAGS)
set(CMAKE_CXX_FLAGS "${UNIQ_CMAKE_CXX_FLAGS}" CACHE STRING "C++ Compiler Base Flags" FORCE)
remove_duplicated_flags("-march=rv32imafc_zicsr_zifencei_xesppie -mabi=ilp32f ${CMAKE_ASM_FLAGS}" UNIQ_CMAKE_ASM_FLAGS)
set(CMAKE_ASM_FLAGS "${UNIQ_CMAKE_CXX_FLAGS}" CACHE STRING "Asm Compiler Base Flags" FORCE)

remove_duplicated_flags("-nostartfiles -march=rv32imafc_zicsr_zifencei_xesppie -mabi=ilp32f ${CMAKE_EXE_LINKER_FLAGS}"
                        UNIQ_CMAKE_SAFE_EXE_LINKER_FLAGS)
set(CMAKE_EXE_LINKER_FLAGS "${UNIQ_CMAKE_SAFE_EXE_LINKER_FLAGS}" CACHE STRING "Linker Base Flags" FORCE)
