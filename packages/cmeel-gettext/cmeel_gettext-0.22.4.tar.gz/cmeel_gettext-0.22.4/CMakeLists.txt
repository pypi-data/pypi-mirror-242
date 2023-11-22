cmake_minimum_required(VERSION 3.20)

set(GETTEXT_VERSION 0.22.4)

project(cmeel-gettext VERSION ${GETTEXT_VERSION})

include(ExternalProject)
ExternalProject_Add(
  gettext
  URL "https://ftpmirror.gnu.org/gnu/gettext/gettext-${GETTEXT_VERSION}.tar.xz"
  URL_HASH "SHA1=2ebfb3b5d911a8f41a22919cec5d79553645fa11"
  DOWNLOAD_EXTRACT_TIMESTAMP ON
  BUILD_IN_SOURCE ON
  CONFIGURE_COMMAND "./configure" "--prefix=${CMAKE_INSTALL_PREFIX}"
                    ${CMEEL_CONFIGURE_OPTIONS}
  COMMAND sed -i.bak "/SUBDIRS/s/doc //" Makefile
  BUILD_COMMAND "make" "VERBOSE=1"
  # TEST_COMMAND "make" "check"
  INSTALL_COMMAND "make" "install")

# dummy file for install target
install(FILES README.md DESTINATION share/cmeel-gettext/)
