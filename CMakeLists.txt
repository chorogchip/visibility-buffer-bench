cmake_minimum_required(VERSION 3.26)

project(TVBPerf LANGUAGES CXX RC)

include(FetchContent)
include(CheckIPOSupported)

# =============================================================================
# Supported build environment
# =============================================================================

if(NOT WIN32)
    message(FATAL_ERROR "TVBPerf is a Windows-only Direct3D 12 project.")
endif()

if(NOT MSVC)
    message(FATAL_ERROR "TVBPerf currently requires the MSVC toolchain.")
endif()

# Ninja discovers MSVC header dependencies by parsing /showIncludes output.
# CMake 4.x can misdecode the Korean VS 2026 prefix while probing cl.exe,
# leaving every object with zero tracked headers. Set the actual compiler
# prefix explicitly so ProgramArgument layout changes cannot leave stale
# objects in the same executable.
if(CMAKE_GENERATOR MATCHES "Ninja")
    set(CMAKE_CL_SHOWINCLUDES_PREFIX "참고: 포함 파일: ")
endif()

if(CMAKE_SIZEOF_VOID_P EQUAL 4)
    message(FATAL_ERROR "TVBPerf supports only 64-bit builds.")
endif()

# The repository's CMakeSettings.json uses one Ninja build tree per
# configuration.
if(CMAKE_CONFIGURATION_TYPES)
    message(FATAL_ERROR
        "TVBPerf requires a single-config generator. "
        "Use the x64-Debug or x64-Release Ninja configuration from CMakeSettings.json."
    )
endif()

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build configuration" FORCE)
endif()
set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS Debug Release)

if(NOT CMAKE_BUILD_TYPE STREQUAL "Debug" AND
   NOT CMAKE_BUILD_TYPE STREQUAL "Release")
    message(FATAL_ERROR
        "Unsupported CMAKE_BUILD_TYPE='${CMAKE_BUILD_TYPE}'. "
        "TVBPerf supports Debug and Release."
    )
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Keep all in-tree libraries on the same CRT.
set(CMAKE_MSVC_RUNTIME_LIBRARY
    "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL"
)

# Avoid remote update checks after a dependency has been populated. Version
# changes in this file still cause the appropriate dependency to be refreshed.
set(FETCHCONTENT_UPDATES_DISCONNECTED ON CACHE BOOL
    "Do not contact remotes for already-populated FetchContent dependencies"
    FORCE
)

# Third-party libraries are linked statically except for the prebuilt DXC DLL.
set(BUILD_SHARED_LIBS OFF CACHE BOOL "Build static third-party libraries" FORCE)
set(BUILD_TESTING OFF CACHE BOOL "Disable third-party tests" FORCE)

# =============================================================================
# Project options and paths
# =============================================================================

option(TVBPERF_ENABLE_IPO
    "Enable interprocedural optimization for the Release renderer"
    ON
)

set(TVBPERF_SRC_DIR      "${CMAKE_CURRENT_SOURCE_DIR}/src")
set(TVBPERF_INCLUDE_DIR  "${CMAKE_CURRENT_SOURCE_DIR}/include")
set(TVBPERF_ASSETS_DIR   "${CMAKE_CURRENT_SOURCE_DIR}/assets")
set(TVBPERF_SHADER_DIR   "${TVBPERF_ASSETS_DIR}/shaders")
set(TVBPERF_EXTERNAL_DIR "${CMAKE_CURRENT_SOURCE_DIR}/external")

# Optional local source overrides. When left empty, an existing source tree in
# external/ is reused; otherwise CMake downloads the pinned revision.
set(TVBPERF_ASSIMP_SOURCE_DIR "" CACHE PATH
    "Optional local Assimp source directory"
)
mark_as_advanced(
    TVBPERF_ASSIMP_SOURCE_DIR
)

function(tvbperf_resolve_local_source output_variable override_path fallback_path)
    set(_resolved "")

    if(NOT "${override_path}" STREQUAL "")
        get_filename_component(_resolved
            "${override_path}"
            ABSOLUTE
            BASE_DIR "${CMAKE_CURRENT_SOURCE_DIR}"
        )
        if(NOT EXISTS "${_resolved}/CMakeLists.txt")
            message(FATAL_ERROR
                "Local dependency source '${_resolved}' does not contain CMakeLists.txt."
            )
        endif()
    elseif(EXISTS "${fallback_path}/CMakeLists.txt")
        get_filename_component(_resolved "${fallback_path}" ABSOLUTE)
    endif()

    set(${output_variable} "${_resolved}" PARENT_SCOPE)
endfunction()

tvbperf_resolve_local_source(
    TVBPERF_ASSIMP_LOCAL_SOURCE
    "${TVBPERF_ASSIMP_SOURCE_DIR}"
    "${TVBPERF_EXTERNAL_DIR}/assimp"
)

# =============================================================================
# Common project compile settings
# =============================================================================

add_library(TVBPerfProjectOptions INTERFACE)
add_library(TVBPerf::ProjectOptions ALIAS TVBPerfProjectOptions)

set_target_properties(TVBPerfProjectOptions PROPERTIES FOLDER "CMake")

target_compile_features(TVBPerfProjectOptions INTERFACE cxx_std_20)
target_compile_definitions(TVBPerfProjectOptions INTERFACE
    UNICODE
    _UNICODE
    NOMINMAX
    "$<$<CONFIG:Debug>:_DEBUG>"
    "$<$<CONFIG:Release>:NDEBUG>"
)
target_compile_options(TVBPerfProjectOptions INTERFACE
    /W3
    /sdl
    /permissive-
    /Zc:__cplusplus
    /utf-8
)

# =============================================================================
# DirectXTex
# =============================================================================

# Texture decoding only. GPU resources and uploads are managed by TVBPerf.
set(BUILD_TOOLS OFF CACHE BOOL "" FORCE)
set(BUILD_SAMPLE OFF CACHE BOOL "" FORCE)
set(BUILD_DX11 OFF CACHE BOOL "" FORCE)
set(BUILD_DX12 OFF CACHE BOOL "" FORCE)
set(BC_USE_OPENMP OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
    directxtex
    GIT_REPOSITORY https://github.com/microsoft/DirectXTex.git
    GIT_TAG may2026
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(directxtex)

if(NOT TARGET DirectXTex)
    message(FATAL_ERROR "DirectXTex did not create the expected DirectXTex target.")
endif()
set_target_properties(DirectXTex PROPERTIES FOLDER "External/DirectXTex")

# =============================================================================
# fastgltf
# =============================================================================

set(FASTGLTF_ENABLE_TESTS OFF CACHE BOOL "" FORCE)
set(FASTGLTF_ENABLE_EXAMPLES OFF CACHE BOOL "" FORCE)
set(FASTGLTF_ENABLE_DOCS OFF CACHE BOOL "" FORCE)
set(FASTGLTF_ENABLE_GLTF_RS OFF CACHE BOOL "" FORCE)
set(FASTGLTF_ENABLE_ASSIMP OFF CACHE BOOL "" FORCE)
set(FASTGLTF_ENABLE_CPP_MODULES OFF CACHE BOOL "" FORCE)
set(FASTGLTF_ENABLE_INSTALL OFF CACHE BOOL "" FORCE)
set(FASTGLTF_COMPILE_AS_CPP20 ON CACHE BOOL "" FORCE)

FetchContent_Declare(
    fastgltf
    GIT_REPOSITORY https://github.com/spnda/fastgltf.git
    GIT_TAG v0.9.0
    GIT_SHALLOW TRUE
)
FetchContent_MakeAvailable(fastgltf)

if(NOT TARGET fastgltf)
    message(FATAL_ERROR "fastgltf did not create the expected fastgltf target.")
endif()
set_target_properties(fastgltf PROPERTIES FOLDER "External/fastgltf")

# =============================================================================
# DirectX Shader Compiler (official prebuilt NuGet package)
# =============================================================================

FetchContent_Declare(
    dxc
    URL https://www.nuget.org/api/v2/package/Microsoft.Direct3D.DXC/1.8.2505.32
    URL_HASH SHA256=C6E82B70C14552F1DD58E4A79C93EEAB1567EEB0A9EE63A51564C410429BCE3E
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(dxc)

set(TVBPERF_DXC_ROOT "${dxc_SOURCE_DIR}/build/native")
set(TVBPERF_DXC_ARCH x64)
set(TVBPERF_DXCOMPILER_DLL
    "${TVBPERF_DXC_ROOT}/bin/${TVBPERF_DXC_ARCH}/dxcompiler.dll"
)
set(TVBPERF_DXIL_DLL
    "${TVBPERF_DXC_ROOT}/bin/${TVBPERF_DXC_ARCH}/dxil.dll"
)

foreach(_required_dxc_file IN ITEMS
    "${TVBPERF_DXC_ROOT}/include/dxcapi.h"
    "${TVBPERF_DXC_ROOT}/lib/${TVBPERF_DXC_ARCH}/dxcompiler.lib"
    "${TVBPERF_DXCOMPILER_DLL}"
    "${TVBPERF_DXIL_DLL}"
)
    if(NOT EXISTS "${_required_dxc_file}")
        message(FATAL_ERROR "DXC package file is missing: ${_required_dxc_file}")
    endif()
endforeach()

add_library(DXC::dxcompiler SHARED IMPORTED GLOBAL)
set_target_properties(DXC::dxcompiler PROPERTIES
    IMPORTED_IMPLIB
        "${TVBPERF_DXC_ROOT}/lib/${TVBPERF_DXC_ARCH}/dxcompiler.lib"
    IMPORTED_LOCATION
        "${TVBPERF_DXCOMPILER_DLL}"
    INTERFACE_INCLUDE_DIRECTORIES
        "${TVBPERF_DXC_ROOT}/include"
)

# =============================================================================
# Assimp
# =============================================================================

set(ASSIMP_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(ASSIMP_BUILD_ASSIMP_TOOLS OFF CACHE BOOL "" FORCE)
set(ASSIMP_BUILD_SAMPLES OFF CACHE BOOL "" FORCE)
set(ASSIMP_BUILD_DOCS OFF CACHE BOOL "" FORCE)
set(ASSIMP_INSTALL OFF CACHE BOOL "" FORCE)
set(ASSIMP_WARNINGS_AS_ERRORS OFF CACHE BOOL "" FORCE)
set(ASSIMP_BUILD_ALL_EXPORTERS_BY_DEFAULT OFF CACHE BOOL "" FORCE)

if(TVBPERF_ASSIMP_LOCAL_SOURCE)
    message(STATUS "Using local Assimp source: ${TVBPERF_ASSIMP_LOCAL_SOURCE}")
    add_subdirectory(
        "${TVBPERF_ASSIMP_LOCAL_SOURCE}"
        "${CMAKE_BINARY_DIR}/external/assimp-build"
        EXCLUDE_FROM_ALL
    )
else()
    message(STATUS "Fetching Assimp v5.4.3")
    FetchContent_Declare(
        assimp
        GIT_REPOSITORY https://github.com/assimp/assimp.git
        GIT_TAG v5.4.3
        GIT_SHALLOW TRUE
    )
    FetchContent_MakeAvailable(assimp)
endif()

if(NOT TARGET assimp)
    message(FATAL_ERROR "Assimp did not create the expected assimp target.")
endif()
set_target_properties(assimp PROPERTIES FOLDER "External/assimp")

if(TARGET zlibstatic)
    set_target_properties(zlibstatic PROPERTIES FOLDER "External/assimp")
endif()
if(TARGET UpdateAssimpLibsDebugSymbolsAndDLLs)
    set_target_properties(UpdateAssimpLibsDebugSymbolsAndDLLs PROPERTIES
        FOLDER "External/assimp"
    )
endif()

# =============================================================================
# Source discovery
# =============================================================================

file(GLOB_RECURSE TVBPERF_CPP_FILES
    CONFIGURE_DEPENDS
    "${TVBPERF_SRC_DIR}/*.cpp"
)
file(GLOB_RECURSE TVBPERF_HEADER_FILES
    CONFIGURE_DEPENDS
    "${TVBPERF_INCLUDE_DIR}/*.h"
    "${TVBPERF_INCLUDE_DIR}/*.hpp"
)
file(GLOB_RECURSE TVBPERF_RC_FILES
    CONFIGURE_DEPENDS
    "${TVBPERF_SRC_DIR}/*.rc"
)
file(GLOB_RECURSE TVBPERF_SHADER_FILES
    CONFIGURE_DEPENDS
    "${TVBPERF_SHADER_DIR}/*.hlsl"
    "${TVBPERF_SHADER_DIR}/*.hlsli"
    "${TVBPERF_SHADER_DIR}/*.fx"
    "${TVBPERF_SHADER_DIR}/*.vs"
    "${TVBPERF_SHADER_DIR}/*.ps"
    "${TVBPERF_SHADER_DIR}/*.cs"
)

foreach(_source_list IN ITEMS
    TVBPERF_CPP_FILES
    TVBPERF_HEADER_FILES
    TVBPERF_RC_FILES
)
    list(FILTER ${_source_list} EXCLUDE REGEX "[/\\\\]trashes[/\\\\]")
    list(SORT ${_source_list})
endforeach()
list(SORT TVBPERF_SHADER_FILES)

# =============================================================================
# Renderer executable
# =============================================================================

add_executable(TVBPerf WIN32
    ${TVBPERF_CPP_FILES}
    ${TVBPERF_HEADER_FILES}
    ${TVBPERF_RC_FILES}
    ${TVBPERF_SHADER_FILES}
)

target_link_libraries(TVBPerf PRIVATE
    TVBPerf::ProjectOptions
    assimp
    DirectXTex
    fastgltf::fastgltf
    DXC::dxcompiler
    d3d12
    dxgi
    d3dcompiler
    user32
    gdi32
    kernel32
    ole32
    windowscodecs
    Shell32
)

target_include_directories(TVBPerf PRIVATE
    "${TVBPERF_INCLUDE_DIR}"
    "${TVBPERF_SHADER_DIR}"
)

# CMake already supplies the standard /Od,/Zi and /O2 configuration flags.
# Keep only the additional release tuning used by the benchmark.
target_compile_options(TVBPerf PRIVATE
    "$<$<CONFIG:Release>:/Oi>"
    "$<$<CONFIG:Release>:/Ot>"
    "$<$<CONFIG:Release>:/Gy>"
)

target_link_options(TVBPerf PRIVATE
    /DEBUG
    "$<$<CONFIG:Debug>:/INCREMENTAL>"
    "$<$<CONFIG:Release>:/INCREMENTAL:NO>"
    "$<$<CONFIG:Release>:/OPT:REF>"
    "$<$<CONFIG:Release>:/OPT:ICF>"
)

if(TVBPERF_ENABLE_IPO)
    check_ipo_supported(RESULT TVBPERF_IPO_SUPPORTED OUTPUT TVBPERF_IPO_ERROR)
    if(TVBPERF_IPO_SUPPORTED)
        set_property(TARGET TVBPerf PROPERTY
            INTERPROCEDURAL_OPTIMIZATION_RELEASE TRUE
        )
    else()
        message(WARNING "Release IPO is unavailable: ${TVBPERF_IPO_ERROR}")
    endif()
endif()

set(TVBPERF_RUNTIME_OUTPUT_DIR
    "${CMAKE_BINARY_DIR}/bin/${CMAKE_BUILD_TYPE}"
)
set_target_properties(TVBPerf PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${TVBPERF_RUNTIME_OUTPUT_DIR}"
    PDB_OUTPUT_DIRECTORY "${TVBPERF_RUNTIME_OUTPUT_DIR}"
    VS_DEBUGGER_WORKING_DIRECTORY "${TVBPERF_RUNTIME_OUTPUT_DIR}"
    FOLDER "TVBPerf"
)

# HLSL is compiled at runtime by DXC. Keep shader files visible in the IDE but
# prevent Visual Studio from assigning a build tool to them.
if(TVBPERF_SHADER_FILES)
    set_source_files_properties(${TVBPERF_SHADER_FILES} PROPERTIES
        VS_TOOL_OVERRIDE "None"
        HEADER_FILE_ONLY TRUE
    )
endif()

# =============================================================================
# Incremental runtime-file deployment
# =============================================================================

# The previous ALL custom target copied the complete shader directory on every
# build. These stamp commands run only when a source shader, DXC binary, or the
# generated shader manifest changes. BYPRODUCTS also lets Ninja restore a
# deleted runtime file without rebuilding unrelated C++ targets.
set(TVBPERF_RUNTIME_STAMP_DIR "${CMAKE_BINARY_DIR}/runtime-stamps")
file(MAKE_DIRECTORY "${TVBPERF_RUNTIME_STAMP_DIR}")

set(TVBPERF_RUNTIME_DEPLOY_STAMPS "")

if(TVBPERF_SHADER_FILES)
    set(TVBPERF_SHADER_OUTPUT_DIR
        "${TVBPERF_RUNTIME_OUTPUT_DIR}/assets/shaders"
    )
    set(TVBPERF_SHADER_MANIFEST
        "${TVBPERF_RUNTIME_STAMP_DIR}/shader-manifest.txt"
    )
    set(TVBPERF_SHADER_STAMP
        "${TVBPERF_RUNTIME_STAMP_DIR}/shaders.stamp"
    )
    set(TVBPERF_SHADER_OUTPUT_FILES "")
    set(_tvbperf_shader_manifest_content "")

    foreach(_shader IN LISTS TVBPERF_SHADER_FILES)
        file(RELATIVE_PATH _shader_relative
            "${TVBPERF_SHADER_DIR}"
            "${_shader}"
        )
        list(APPEND TVBPERF_SHADER_OUTPUT_FILES
            "${TVBPERF_SHADER_OUTPUT_DIR}/${_shader_relative}"
        )
        string(APPEND _tvbperf_shader_manifest_content
            "${_shader_relative}\n"
        )
    endforeach()

    # file(CONFIGURE) preserves the timestamp when the manifest content did not
    # change, so a normal CMake regeneration does not force another copy.
    file(CONFIGURE
        OUTPUT "${TVBPERF_SHADER_MANIFEST}"
        CONTENT "${_tvbperf_shader_manifest_content}"
        @ONLY
    )

    add_custom_command(
        OUTPUT "${TVBPERF_SHADER_STAMP}"
        BYPRODUCTS ${TVBPERF_SHADER_OUTPUT_FILES}
        COMMAND "${CMAKE_COMMAND}" -E rm -rf "${TVBPERF_SHADER_OUTPUT_DIR}"
        COMMAND "${CMAKE_COMMAND}" -E make_directory "${TVBPERF_SHADER_OUTPUT_DIR}"
        COMMAND "${CMAKE_COMMAND}" -E copy_directory
            "${TVBPERF_SHADER_DIR}"
            "${TVBPERF_SHADER_OUTPUT_DIR}"
        COMMAND "${CMAKE_COMMAND}" -E touch "${TVBPERF_SHADER_STAMP}"
        DEPENDS
            ${TVBPERF_SHADER_FILES}
            "${TVBPERF_SHADER_MANIFEST}"
        COMMENT "Updating runtime shaders"
        VERBATIM
    )
    list(APPEND TVBPERF_RUNTIME_DEPLOY_STAMPS "${TVBPERF_SHADER_STAMP}")
endif()

set(TVBPERF_DXC_STAMP "${TVBPERF_RUNTIME_STAMP_DIR}/dxc-runtime.stamp")
set(TVBPERF_DEPLOYED_DXCOMPILER
    "${TVBPERF_RUNTIME_OUTPUT_DIR}/dxcompiler.dll"
)
set(TVBPERF_DEPLOYED_DXIL
    "${TVBPERF_RUNTIME_OUTPUT_DIR}/dxil.dll"
)
set(TVBPERF_RUNTIME_LICENSE_DIR
    "${TVBPERF_RUNTIME_OUTPUT_DIR}/licenses"
)
set(TVBPERF_DXC_LICENSE_DIR
    "${TVBPERF_RUNTIME_LICENSE_DIR}/DXC"
)
set(TVBPERF_PROJECT_LICENSE
    "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE"
)
set(TVBPERF_THIRD_PARTY_NOTICES
    "${CMAKE_CURRENT_SOURCE_DIR}/THIRD_PARTY_NOTICES.md"
)
set(TVBPERF_SCENE_ASSET_NOTICES
    "${CMAKE_CURRENT_SOURCE_DIR}/SCENE_ASSET_NOTICES.md"
)
set(TVBPERF_DXC_LICENSE_LLVM
    "${dxc_SOURCE_DIR}/LICENSE-LLVM.txt"
)
set(TVBPERF_DXC_LICENSE_MS
    "${dxc_SOURCE_DIR}/LICENSE-MS.txt"
)
set(TVBPERF_DXC_LICENSE_MIT
    "${dxc_SOURCE_DIR}/LICENCE-MIT.txt"
)
set(TVBPERF_DXC_DISTRIBUTABLES
    "${dxc_SOURCE_DIR}/distributable_files.txt"
)

add_custom_command(
    OUTPUT "${TVBPERF_DXC_STAMP}"
    BYPRODUCTS
        "${TVBPERF_DEPLOYED_DXCOMPILER}"
        "${TVBPERF_DEPLOYED_DXIL}"
        "${TVBPERF_RUNTIME_OUTPUT_DIR}/LICENSE"
        "${TVBPERF_RUNTIME_OUTPUT_DIR}/THIRD_PARTY_NOTICES.md"
        "${TVBPERF_RUNTIME_OUTPUT_DIR}/SCENE_ASSET_NOTICES.md"
        "${TVBPERF_DXC_LICENSE_DIR}/LICENSE-LLVM.txt"
        "${TVBPERF_DXC_LICENSE_DIR}/LICENSE-MS.txt"
        "${TVBPERF_DXC_LICENSE_DIR}/LICENCE-MIT.txt"
        "${TVBPERF_DXC_LICENSE_DIR}/distributable_files.txt"
    COMMAND "${CMAKE_COMMAND}" -E make_directory
        "${TVBPERF_RUNTIME_OUTPUT_DIR}"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_DXCOMPILER_DLL}"
        "${TVBPERF_DEPLOYED_DXCOMPILER}"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_DXIL_DLL}"
        "${TVBPERF_DEPLOYED_DXIL}"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_PROJECT_LICENSE}"
        "${TVBPERF_RUNTIME_OUTPUT_DIR}/LICENSE"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_THIRD_PARTY_NOTICES}"
        "${TVBPERF_RUNTIME_OUTPUT_DIR}/THIRD_PARTY_NOTICES.md"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_SCENE_ASSET_NOTICES}"
        "${TVBPERF_RUNTIME_OUTPUT_DIR}/SCENE_ASSET_NOTICES.md"
    COMMAND "${CMAKE_COMMAND}" -E make_directory
        "${TVBPERF_DXC_LICENSE_DIR}"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_DXC_LICENSE_LLVM}"
        "${TVBPERF_DXC_LICENSE_DIR}/LICENSE-LLVM.txt"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_DXC_LICENSE_MS}"
        "${TVBPERF_DXC_LICENSE_DIR}/LICENSE-MS.txt"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_DXC_LICENSE_MIT}"
        "${TVBPERF_DXC_LICENSE_DIR}/LICENCE-MIT.txt"
    COMMAND "${CMAKE_COMMAND}" -E copy_if_different
        "${TVBPERF_DXC_DISTRIBUTABLES}"
        "${TVBPERF_DXC_LICENSE_DIR}/distributable_files.txt"
    COMMAND "${CMAKE_COMMAND}" -E touch "${TVBPERF_DXC_STAMP}"
    DEPENDS
        "${TVBPERF_DXCOMPILER_DLL}"
        "${TVBPERF_DXIL_DLL}"
        "${TVBPERF_PROJECT_LICENSE}"
        "${TVBPERF_THIRD_PARTY_NOTICES}"
        "${TVBPERF_SCENE_ASSET_NOTICES}"
        "${TVBPERF_DXC_LICENSE_LLVM}"
        "${TVBPERF_DXC_LICENSE_MS}"
        "${TVBPERF_DXC_LICENSE_MIT}"
        "${TVBPERF_DXC_DISTRIBUTABLES}"
    COMMENT "Updating DXC runtime DLLs and legal notices"
    VERBATIM
)
list(APPEND TVBPERF_RUNTIME_DEPLOY_STAMPS "${TVBPERF_DXC_STAMP}")

add_custom_target(TVBPerfRuntimeFiles
    DEPENDS ${TVBPERF_RUNTIME_DEPLOY_STAMPS}
)
add_dependencies(TVBPerf TVBPerfRuntimeFiles)
set_target_properties(TVBPerfRuntimeFiles PROPERTIES FOLDER "TVBPerf")

# =============================================================================
# IDE source groups
# =============================================================================

source_group(TREE "${TVBPERF_SRC_DIR}"
    PREFIX "Source"
    FILES ${TVBPERF_CPP_FILES} ${TVBPERF_RC_FILES}
)
source_group(TREE "${TVBPERF_INCLUDE_DIR}"
    PREFIX "Include"
    FILES ${TVBPERF_HEADER_FILES}
)
if(TVBPERF_SHADER_FILES)
    source_group(TREE "${TVBPERF_SHADER_DIR}"
        PREFIX "Shader Files"
        FILES ${TVBPERF_SHADER_FILES}
    )
endif()

message(STATUS "TVBPerf configuration: ${CMAKE_BUILD_TYPE}")
message(STATUS "TVBPerf runtime directory: ${TVBPERF_RUNTIME_OUTPUT_DIR}")
