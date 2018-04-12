#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/evana/apv_ws/src/baxter_tools"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/evana/apv_ws/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/evana/apv_ws/install/lib/python2.7/dist-packages:/home/evana/apv_ws/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/evana/apv_ws/build" \
    "/usr/bin/python" \
    "/home/evana/apv_ws/src/baxter_tools/setup.py" \
    build --build-base "/home/evana/apv_ws/build/baxter_tools" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/evana/apv_ws/install" --install-scripts="/home/evana/apv_ws/install/bin"
