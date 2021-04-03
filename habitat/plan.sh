pkg_name=axa
pkg_origin=jel
pkg_version=1.30.1
pkg_maintainer="Greg Fodor <gfodor@jel.app>"
pkg_license=('Apache-2.0')
pkg_upstream_url='https://matrix.org'
pkg_description='Jel matrix homeserver'
pkg_deps=(
  'core/bash'
  'core/glibc'
  'jel/python'
  'jel/postgresql12-client'
  'core/gcc-libs'
  'jel/openssl'
  'core/libffi'
  'core/libjpeg-turbo'
  'core/libxslt'
  'core/virtualenv'
)
pkg_build_deps=(
  core/rust
)
pkg_bin_dirs=(bin)
pkg_svc_user="root"

do_before() {
  python -m pip install -U pip
  update_pkg_version
}

do_prepare() {
  python -m venv "$pkg_prefix"
  source "$pkg_prefix/bin/activate"
}

do_build() {
  return 0
}

do_install() {
  # Rust build is not working for python crypto for now.
  export CRYPTOGRAPHY_DONT_BUILD_RUST=1

  pip --disable-pip-version-check install "matrix-synapse[postgres]==$pkg_version"
  cp -R synapse/axa $pkg_prefix/lib/python3.7/site-packages/synapse
  pip install --upgrade --force 'lxml>=3.5.0'
  pip install --upgrade --force 'pyjwt'
  pip freeze > "$pkg_prefix/requirements.txt"
}

do_strip() {
  return 0
}
