# --------------------------------------------------------------------
# 
#                         DEVELOPMENT
#                            PLAN
# 
# - support custom types defined in Fortran
# --- parse the custom type and determine its contents in terms of basic types
# --- generate a matching C struct using ctypes to the custom type
# --- identify proper allocation schema in numpy to make sure memory
#     maps correctly into Fortran
# 
# - support procedures as arguments
# --- construct C function in Python (with ctypes) that translates C 
#     style data into Python compatible data, calls the Python 
#     function that was passed in as an argument, then translates the
#     results back into C style data for return
# --- construct a BIND(C) Fortran wrapper function that translates
#     arguments from Fortran style into C style and calls the C 
#     (Python) function from Fortran, nested in a MODULE with PUBLIC
#     variables that assign the address of the C function
# --- pass the memory address of the C function in Python to Fortran
#     wrapper, use that address to assign a local Fortran function 
#     in the BIND(C) wrapper module that calls Python C function
# 
# - extend test cases to achieve (near) 100% coverage of all lines
# 
# 
# --------------------------------------------------------------------
#                            TODO LISTS
# 
# FMODPY
# - assign implicit_typing to True and named_end to False for '.f' files
# - assign correct shape (from shape[0] ...) for implicit array arguments
# - check the memory contiguity of OPTIONAL input arrays 
# - LOGICAL array warning should only happen *after* non-arguments are deleted
# - compile dependencies first when 'depends_files' are given and 'autocompile=True'
# - remove automatic size option in wrapper for optional arguments with unknown shape
# - handle automatic shapes that have a ":" inside of them
# - check for existence of Fortran compiler on install, offer instruction
# - support lists of compilation commands to run before making final object
# - support list of files to include in final module compilation (like objects)
# - support multiple file input, for specifying all files that are part
#   of a module or may contain important types or constants
# - empty classes should not be added into wrappers, they should be skipped
#   (i.e., a class that only defines interfaces)
# - automatic documentation of the types of inputs in Python, included
#   in addition to original Fortran documentation.
# 
# 
# TYPE
# - find the definition of this Type, and all of its contents.
# - the type could be declared in a module that is "USED" in
#   another file, will have to scan other files for modules
#   with type definitions?
#    in the same subroutine or function
#    in the same module
#    in a USED module, potentially in another file
# - define a C struct in the appropriate context 
# - cycle all arugments in type, initializing them correctly
# - store all the initialized values into a C struct
# 
# 
# PROCEDURE
# - The interface being used by a subroutine-as-an-argument could
#   be defined in another module. Need to check for that.
#   Need to disallow "EXTERNAL" subroutines-as-arguments.
# - Need to write fort_to_py versions of interface functions in
#   fortran wrapper and in python wrapper
# - Have a way to bypass Python when a fmodpy wrapped fortran routine
#   is given. Maybe define a get_address function for all source
#   functions in Fortran wrappers?
# 
