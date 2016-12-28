#!/bin/bash
#!/bin/sh

help()
{
    cat << HELP
install.sh -- install the module into the system

Usage:
    ./install.sh <module_name> <module_version> [install_dir]

    moduel_name     - name of the module, will be used as the directory name
    moduel_version  - version of the module
    install_dir     - directory to install the module into, default to '/opt/vobile'

Example:
    ./install.sh Zuinews_app 1.0.1.0 /opt/vobile

HELP
    exit 1
}

exist_error()
{
    [ -z "$1" ] && exit 1
    echo "Install failed - file or directory '$1' exist already"
    [ -n "$2" ] && echo " * $2"
    [ -z "$2" ] && echo " * please remove it manually"
    exit 1
}

not_exist_error()
{
    [ -z "$1" ] && exit 1
    echo "Install failed - file or directory '$1' not exist"
    [ -n "$2" ] && echo " * $2"
    [ -z "$2" ] && echo " * make sure '$1' exists before proceeding"
    exit 1
}

echo_and_exec()
{
    [ -n "$1" ] && echo $1
    `$1`
}

exit_clean()
{
    [ -n "$fake_install_dir" ] && echo_and_exec "rm -rf $fake_install_dir"
    if [ -d "$install_dir/$module" ] ; then
        exit 0
    else
        exit 1
    fi
}

# check argument list
[ $# -gt 3 ] && help
[ -z "$1" ] && help
[ "$1" = "-h" ] && help
[ "$1" = "--help" ] && help

project="GRT"
module="$1"
version="$2";
install_dir="/opt/vobile"
[ -n "$3" ] && install_dir="$3"


full_name="${module}_v${version}"

# validate dirs
tdir="$install_dir/$module"
[ -e "$tdir" ] && exist_error "$tdir"

# install the module
fake_install_dir=`mktemp -d`
trap exit_clean EXIT

# copy module files and configuration files to fake_install_dir
tdir="$install_dir/$module/$full_name"
echo_and_exec "mkdir -p $tdir"
for var in `ls`; do
    if [ $var != "auto_deploy" -a $var != "Install.sh" -a $var != "Upgrade.sh" -a $var != "Rollback.sh" ]; then
        echo_and_exec "cp -R $var $tdir"
    fi
done


#echo_and_exec "mkdir $fake_install_dir/$module"
#echo_and_exec "cp -r $module/$full_name/etc $fake_install_dir/$module/etc"


## copy file to the install_dir
#tdir="$install_dir/$module"
#[ -d "$tdir" ] || echo_and_exec "mkdir -p $tdir"
#echo_and_exec "mv $fake_install_dir/app/$module/$full_name $install_dir/app/$module"
#echo_and_exec "mv $fake_install_dir/app/$module/current $install_dir/app/$module"
#echo_and_exec "mv $fake_install_dir/$module $install_dir"


