#!/bin/bash

# Check to make sure this script is being run from the correct directory
if [ ! -e "scripts/setup.sh" ]
then
    echo "You must run this script from the root directory"
    exit 2
fi

echo -n "Upgrade core system packages (via apt-get)? [Y/n] "
read UPGRADE_CORE

if [ "$UPGRADE_CORE" == "Y" ] || [ "$UPGRADE_CORE" == "y" ] || [ "$UPGRADE_CORE" == "" ]
then
    UPGRADE_CORE="y"
else
    UPGRADE_CORE="n"
fi

if [ $UPGRADE_CORE == "y" ]
then
    echo ""

    # Upgrade all core packages
    sudo apt-get update
    sudo apt-get upgrade
fi

echo ""
echo -n "Install prerequisite system packages (via apt-get)? [Y/n] "
read INSTALL_SYSTEM_PREREQS

if [ "$INSTALL_SYSTEM_PREREQS" == "Y" ] || [ "$INSTALL_SYSTEM_PREREQS" == "y" ] || [ "$INSTALL_SYSTEM_PREREQS" == "" ]
then
    INSTALL_SYSTEM_PREREQS="y"
else
    INSTALL_SYSTEM_PREREQS="n"
fi

if [ $INSTALL_SYSTEM_PREREQS == "y" ]
then
    echo ""

    # Install prerequisite packages
    sudo apt-get install apache2 build-essential libapache2-mod-wsgi libldap2-dev libmysqlclient-dev libsasl2-dev libssl-dev mercurial mysql-server python-dev  python-setuptools vim
fi

echo ""
echo -n "Secure your MySQL installation? [Y/n] "
read SECURE_MYSQL

if [ "$SECURE_MYSQL" == "Y" ] || [ "$SECURE_MYSQL" == "y" ] || [ "$SECURE_MYSQL" == "" ]
then
    SECURE_MYSQL="y"
else
    SECURE_MYSQL="n"
fi

if [ $SECURE_MYSQL == "y" ]
then
    # Secure MySQL installation
    sudo mysql_secure_installation
else
    echo ""
fi

echo -n "Install virtualenv (via easy_install)? [Y/n] "
read INSTALL_VIRTUALENV

if [ "$INSTALL_VIRTUALENV" == "Y" ] || [ "$INSTALL_VIRTUALENV" == "y" ] || [ "$INSTALL_VIRTUALENV" == "" ]
then
    INSTALL_VIRTUALENV="y"
else
    INSTALL_VIRTUALENV="n"
fi

if [ $INSTALL_VIRTUALENV == "y" ]
then
    echo ""

    # Install virtualenv
    sudo easy_install virtualenv virtualenvwrapper

    if [ ! -d "/opt/virtualenv" ]
    then
        # Create directory to store virtualenvs
        sudo mkdir /opt/virtualenv
    fi

    # Correct ownership of virtualenv directory
    sudo chown -R $USER:$USER /opt/virtualenv

    # Set virtualenv configuration settings
    export WORKON_HOME=/opt/virtualenv
    source /usr/local/bin/virtualenvwrapper.sh

    if [ ! -d "/opt/virtualenv/osp" ]
    then
        # Create virtualenv for OSP
        mkvirtualenv -p /usr/bin/python2.6 --no-site-packages osp
    fi
fi

echo ""
echo -n "Install prerequisite Python packages (via easy_install)? [Y/n] "
read INSTALL_PYTHON_PREREQS

if [ "$INSTALL_PYTHON_PREREQS" == "Y" ] || [ "$INSTALL_PYTHON_PREREQS" == "y" ] || [ "$INSTALL_PYTHON_PREREQS" == "" ]
then
    INSTALL_PYTHON_PREREQS="y"
else
    INSTALL_PYTHON_PREREQS="n"
fi

if [ $INSTALL_PYTHON_PREREQS == "y" ]
then
    echo ""

    # Make sure we're inside the right virtualenv
    workon osp

    # Install prerequisite Python packages
    easy_install mysql-python==1.2.3 python-ldap==2.3.13 xlwt==0.7.2 django==1.2.5 django-auth-ldap==1.0.9 django-cas==2.0.3 south==0.7.3
fi


echo ""
echo -n "Install Online Student Profile? [Y/n] "
read INSTALL_OSP

if [ "$INSTALL_OSP" == "Y" ] || [ "$INSTALL_OSP" == "y" ] || [ "$INSTALL_OSP" == "" ]
then
    INSTALL_OSP="y"
else
    INSTALL_OSP="n"
fi

if [ $INSTALL_OSP == "y" ]
then
    if [ ! -d "/opt/django" ]
    then
        # Create directory to store Django apps
        sudo mkdir /opt/django
    fi

    # Correct ownership of Django directory
    sudo chown -R $USER:$USER /opt/django

    if [ ! -d "/opt/django/osp" ]
    then
        mkdir /opt/django/osp
        cp -R * /opt/django/osp
    fi
fi

echo ""
echo -n "Create MySQL database? [Y/n] "
read CREATE_DATABASE

if [ "$CREATE_DATABASE" == "Y" ] || [ "$CREATE_DATABASE" == "y" ] || [ "$CREATE_DATABASE" == "" ]
then
    CREATE_DATABASE="y"
else
    CREATE_DATABASE="n"
fi

if [ $CREATE_DATABASE == "y" ]
then
    # Collect information from the user to create the MySQL database for OSP
    echo ""
    echo "Collecting MySQL database information..."
    echo ""
    echo -n "Choose a MySQL database name: "
    read MYSQL_DATABASE
    echo -n "Choose a MySQL username: "
    read MYSQL_USERNAME
    PASSWORDS_MATCH="false"
    while [ $PASSWORDS_MATCH == "false" ]
    do
        echo -n "Choose a MySQL password: "
        stty -echo
        read MYSQL_PASSWORD_1
        stty echo
        echo ""
        echo -n "Confirm your MySQL password: "
        stty -echo
        read MYSQL_PASSWORD_2
        stty echo
        if [ $MYSQL_PASSWORD_1 == $MYSQL_PASSWORD_2 ]
        then
            PASSWORDS_MATCH="true"
        else
            echo ""
            echo "Passwords do not match. Try again."
        fi
    done
    # Create MySQL database
    echo ""
    echo ""
    echo "Prompting for MySQL root password..."
    echo ""
    mysql -u root -p<<EOFMYSQL
CREATE DATABASE $MYSQL_DATABASE;
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO $MYSQL_USERNAME@localhost IDENTIFIED BY '$MYSQL_PASSWORD_1';
EOFMYSQL
fi

echo ""
echo -n "Install WSGI configuration files? [Y/n] "
read INSTALL_WSGI_CONFIG

if [ "$INSTALL_WSGI_CONFIG" == "Y" ] || [ "$INSTALL_WSGI_CONFIG" == "y" ] || [ "$INSTALL_WSGI_CONFIG" == "" ]
then
    INSTALL_WSGI_CONFIG="y"
else
    INSTALL_WSGI_CONFIG="n"
fi

if [ $INSTALL_WSGI_CONFIG == "y" ]
then
    if [ ! -d "/opt/wsgi" ]
    then
        # Create directory to store WSGI configuration files
        sudo mkdir /opt/wsgi
    fi

    # Correct ownership of WSGI directory
    sudo chown -R $USER:$USER /opt/wsgi

    # Copy WSGI configuration files from OSP respository
    cp /opt/django/osp/deploy/osp.wsgi /opt/django/osp/deploy/osp_settings.py /opt/wsgi/

    if [ ! -d "/var/www/python-eggs" ]
    then
        # Create directory for Python egg cache
        sudo mkdir /var/www/python-eggs
    fi

    # Correct ownership of Python egg cache directory
    sudo chown -R www-data:www-data /var/www
fi

echo ""
echo "Open Django settings file for editing? [Y/n] "
read EDIT_SETTINGS

if [ "$EDIT_SETTINGS" == "Y" ] || [ "$EDIT_SETTINGS" == "y" ] || [ "$EDIT_SETTINGS" == "" ]
then
    EDIT_SETTINGS="y"
else
    EDIT_SETTINGS="n"
fi

if [ $EDIT_SETTINGS == "y" ]
then
    # Open Django settings file for editing
    vim /opt/wsgi/osp_settings.py
else
    echo ""
fi

echo -n "Create Django database tables and superuser account? [Y/n] "
read DO_SYNCDB

if [ "$DO_SYNCDB" == "Y" ] || [ "$DO_SYNCDB" == "y" ] || [ "$DO_SYNCDB" == "" ]
then
    DO_SYNCDB="y"
else
    DO_SYNCDB="n"
fi

if [ $DO_SYNCDB == "y" ]
then
    echo ""

    # Create the Django database tables and superuser account
    export PYTHONPATH=$PYTHONPATH:/opt/wsgi:/opt/django/osp
    django-admin.py syncdb --settings=osp_settings
    django-admin.py migrate assessments --settings=osp_settings
    django-admin.py migrate core --settings=osp_settings
    django-admin.py migrate notifications --settings=osp_settings
    django-admin.py migrate surveys --settings=osp_settings
    django-admin.py migrate visits --settings=osp_settings
fi

echo ""
echo -n "Install Apache configuration files? [Y/n] "
read INSTALL_APACHE_CONFIG

if [ "$INSTALL_APACHE_CONFIG" == "Y" ] || [ "$INSTALL_APACHE_CONFIG" == "y" ] || [ "$INSTALL_APACHE_CONFIG" == "" ]
then
    INSTALL_APACHE_CONFIG="y"
else
    INSTALL_APACHE_CONFIG="n"
fi

if [ $INSTALL_APACHE_CONFIG == "y" ]
then
    # Overwrite default Apache configuration file with OSP one
    sudo cp /opt/django/osp/deploy/osp.conf /etc/apache2/sites-available/default
fi

echo ""
echo "Open Apache configuration file for editing? [Y/n] "
read EDIT_APACHE_CONFIG

if [ "$EDIT_APACHE_CONFIG" == "Y" ] || [ "$EDIT_APACHE_CONFIG" == "y" ] || [ "$EDIT_APACHE_CONFIG" == "" ]
then
    EDIT_APACHE_CONFIG="y"
else
    EDIT_APACHE_CONFIG="n"
fi

if [ $EDIT_APACHE_CONFIG == "y" ]
then
    # Open Django settings file for editing
    sudo vim /etc/apache2/sites-available/default
else
    echo ""
fi

if [ ! -L "/opt/django/osp/osp/media/admin" ]
then
    # Symlink Django admin media directory into OSP media directory
    ln -s /opt/virtualenv/osp/lib/python2.6/site-packages/Django-1.2.5-py2.6.egg/django/contrib/admin/media /opt/django/osp/osp/media/admin
fi

echo "Restart Apache? [Y/n] "
read RESTART_APACHE

if [ "$RESTART_APACHE" == "Y" ] || [ "$RESTART_APACHE" == "y" ] || [ "$RESTART_APACHE" == "" ]
then
    RESTART_APACHE="y"
else
    RESTART_APACHE="n"
fi

if [ $RESTART_APACHE == "y" ]
then
    # Restart Apache
    sudo /etc/init.d/apache2 restart
fi
