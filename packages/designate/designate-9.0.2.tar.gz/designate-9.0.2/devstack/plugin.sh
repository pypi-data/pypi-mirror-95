# Install and start **Designate** service in Devstack

# Save trace setting
XTRACE=$(set +o | grep xtrace)
set +o xtrace

# Get backend configuration
# -------------------------
if is_service_enabled designate && [[ -r $DESIGNATE_PLUGINS/backend-$DESIGNATE_BACKEND_DRIVER ]]; then
    # Load plugin
    source $DESIGNATE_PLUGINS/backend-$DESIGNATE_BACKEND_DRIVER
fi

# DevStack Plugin
# ---------------

# cleanup_designate - Remove residual data files, anything left over from previous
# runs that a clean run would need to clean up
function cleanup_designate {
    sudo rm -rf $DESIGNATE_STATE_PATH $DESIGNATE_AUTH_CACHE_DIR
    cleanup_designate_backend
}

# configure_designate - Set config files, create data dirs, etc
function configure_designate {
    [ ! -d $DESIGNATE_CONF_DIR ] && sudo mkdir -m 755 -p $DESIGNATE_CONF_DIR
    sudo chown $STACK_USER $DESIGNATE_CONF_DIR

    [ ! -d $DESIGNATE_LOG_DIR ] &&  sudo mkdir -m 755 -p $DESIGNATE_LOG_DIR
    sudo chown $STACK_USER $DESIGNATE_LOG_DIR

    # (Re)create ``designate.conf``
    rm -f $DESIGNATE_CONF

    # General Configuration
    iniset_rpc_backend designate $DESIGNATE_CONF DEFAULT

    iniset $DESIGNATE_CONF DEFAULT debug $ENABLE_DEBUG_LOG_LEVEL
    iniset $DESIGNATE_CONF DEFAULT state_path $DESIGNATE_STATE_PATH
    iniset $DESIGNATE_CONF DEFAULT root-helper sudo designate-rootwrap $DESIGNATE_ROOTWRAP_CONF
    iniset $DESIGNATE_CONF storage:sqlalchemy connection `database_connection_url designate`

    # Quota Configuration
    iniset $DESIGNATE_CONF DEFAULT quota_zones $DESIGNATE_QUOTA_ZONES
    iniset $DESIGNATE_CONF DEFAULT quota_zone_recordsets $DESIGNATE_QUOTA_ZONE_RECORDSETS
    iniset $DESIGNATE_CONF DEFAULT quota_zone_records $DESIGNATE_QUOTA_ZONE_RECORDS
    iniset $DESIGNATE_CONF DEFAULT quota_recordset_records $DESIGNATE_QUOTA_RECORDSET_RECORDS
    iniset $DESIGNATE_CONF DEFAULT quota_api_export_size $DESIGNATE_QUOTA_API_EXPORT_SIZE

    # Coordination Configuration
    if [[ -n "$DESIGNATE_COORDINATION_URL" ]]; then
        iniset $DESIGNATE_CONF coordination backend_url $DESIGNATE_COORDINATION_URL
    fi

    # API Configuration
    sudo cp $DESIGNATE_DIR/etc/designate/api-paste.ini $DESIGNATE_APIPASTE_CONF
    iniset $DESIGNATE_CONF service:api enabled_extensions_v2 $DESIGNATE_ENABLED_EXTENSIONS_V2
    iniset $DESIGNATE_CONF service:api enabled_extensions_admin $DESIGNATE_ENABLED_EXTENSIONS_ADMIN
    iniset $DESIGNATE_CONF service:api api_base_uri $DESIGNATE_SERVICE_PROTOCOL://$DESIGNATE_SERVICE_HOST:$DESIGNATE_SERVICE_PORT/
    iniset $DESIGNATE_CONF service:api enable_api_v2 $DESIGNATE_ENABLE_API_V2
    iniset $DESIGNATE_CONF service:api enable_api_admin $DESIGNATE_ENABLE_API_ADMIN

    # mDNS Configuration
    iniset $DESIGNATE_CONF service:mdns listen ${DESIGNATE_SERVICE_HOST}:${DESIGNATE_SERVICE_PORT_MDNS}

    # Worker Configuration
    if is_service_enabled designate-worker; then
        iniset $DESIGNATE_CONF service:worker notify True
        iniset $DESIGNATE_CONF service:worker poll_max_retries $DESIGNATE_POLL_RETRIES
        iniset $DESIGNATE_CONF service:worker poll_retry_interval $DESIGNATE_POLL_INTERVAL
    else
        iniset $DESIGNATE_CONF service:worker enabled False
    fi

    # Set up Notifications/Ceilometer Integration
    iniset $DESIGNATE_CONF oslo_messaging_notifications driver "$DESIGNATE_NOTIFICATION_DRIVER"
    iniset $DESIGNATE_CONF oslo_messaging_notifications topics "$DESIGNATE_NOTIFICATION_TOPICS"

    # Root Wrap
    sudo cp $DESIGNATE_DIR/etc/designate/rootwrap.conf.sample $DESIGNATE_ROOTWRAP_CONF
    iniset $DESIGNATE_ROOTWRAP_CONF DEFAULT filters_path $DESIGNATE_DIR/etc/designate/rootwrap.d root-helper

    # Oslo Concurrency
    iniset $DESIGNATE_CONF oslo_concurrency lock_path "$DESIGNATE_STATE_PATH"

    # Set up the rootwrap sudoers for designate
    local rootwrap_sudoer_cmd="$DESIGNATE_BIN_DIR/designate-rootwrap $DESIGNATE_ROOTWRAP_CONF *"
    local tempfile=`mktemp`
    echo "$STACK_USER ALL=(root) NOPASSWD: $rootwrap_sudoer_cmd" >$tempfile
    chmod 0440 $tempfile
    sudo chown root:root $tempfile
    sudo mv $tempfile /etc/sudoers.d/designate-rootwrap

    # TLS Proxy Configuration
    if is_service_enabled tls-proxy; then
        # Set the service port for a proxy to take the original
        iniset $DESIGNATE_CONF service:api listen ${DESIGNATE_SERVICE_HOST}:${DESIGNATE_SERVICE_PORT_INT}
        iniset $DESIGNATE_CONF keystone cafile $SSL_BUNDLE_FILE
    else
        iniset $DESIGNATE_CONF service:api listen ${DESIGNATE_SERVICE_HOST}:${DESIGNATE_SERVICE_PORT}
    fi

    # Setup the Keystone Integration
    if is_service_enabled keystone; then
        iniset $DESIGNATE_CONF service:api auth_strategy keystone
        configure_auth_token_middleware $DESIGNATE_CONF designate $DESIGNATE_AUTH_CACHE_DIR
        iniset $DESIGNATE_CONF keystone region_name $REGION_NAME
        iniset $DESIGNATE_CONF service:api quotas_verify_project_id True
    fi

    # Logging Configuration
    if [ "$USE_SYSTEMD" != "False" ]; then
        setup_systemd_logging $DESIGNATE_CONF
    fi

    # Format logging
    if [ "$LOG_COLOR" == "True" ] && [ "$USE_SYSTEMD" == "False" ]; then
        setup_colorized_logging $DESIGNATE_CONF DEFAULT
    fi

    # Backend Plugin Configuation
    configure_designate_backend
}

function configure_designatedashboard {
    # Compile message catalogs
    if [ -d ${DESIGNATEDASHBOARD_DIR}/designatedashboard/locale ]; then
        (cd ${DESIGNATEDASHBOARD_DIR}/designatedashboard; DJANGO_SETTINGS_MODULE=openstack_dashboard.settings ../manage.py compilemessages)
    fi
}

# Configure the needed tempest options
function configure_designate_tempest() {
    if is_service_enabled tempest; then
        # Tell tempest we're available
        iniset $TEMPEST_CONFIG service_available designate True

        # Tell tempest which APIs are available
        iniset $TEMPEST_CONFIG dns_feature_enabled api_v2 $DESIGNATE_ENABLE_API_V2
        iniset $TEMPEST_CONFIG dns_feature_enabled api_admin $DESIGNATE_ENABLE_API_ADMIN
        iniset $TEMPEST_CONFIG dns_feature_enabled api_v2_root_recordsets True
        iniset $TEMPEST_CONFIG dns_feature_enabled api_v2_quotas True
        iniset $TEMPEST_CONFIG dns_feature_enabled api_v2_quotas_verify_project True
        iniset $TEMPEST_CONFIG dns_feature_enabled bug_1573141_fixed True

        # Tell tempest where are nameservers are.
        nameservers=$DESIGNATE_SERVICE_HOST:$DESIGNATE_SERVICE_PORT_DNS
        # TODO(kiall): Remove hardcoded list of plugins
        case $DESIGNATE_BACKEND_DRIVER in
            bind9)
                nameservers="$DESIGNATE_SERVICE_HOST:$DESIGNATE_SERVICE_PORT_DNS"
                ;;
            akamai)
                nameservers="$DESIGNATE_AKAMAI_NAMESERVERS"
                ;;
            dynect)
                nameservers="$DESIGNATE_DYNECT_NAMESERVERS"
                ;;
        esac

        if [ ! -z "$DESIGNATE_NAMESERVERS" ]; then
            nameservers=$DESIGNATE_NAMESERVERS
        fi

        iniset $TEMPEST_CONFIG dns nameservers $nameservers

        # For legacy functionaltests
        iniset $TEMPEST_CONFIG designate nameservers $nameservers
    fi
}

# create_designate_accounts - Set up common required designate accounts

# Tenant               User       Roles
# ------------------------------------------------------------------
# service              designate  admin        # if enabled
function create_designate_accounts {
    if is_service_enabled designate-api; then
        create_service_user "designate"

        get_or_create_service "designate" "dns" "Designate DNS Service"
        get_or_create_endpoint "dns" \
            "$REGION_NAME" \
            "$DESIGNATE_SERVICE_PROTOCOL://$DESIGNATE_SERVICE_HOST:$DESIGNATE_SERVICE_PORT/"
    fi
}

# create_designate_pool_configuration - Create Pool Configuration
function create_designate_pool_configuration {
    # Sync Pools Config
    $DESIGNATE_BIN_DIR/designate-manage pool update --file $DESIGNATE_CONF_DIR/pools.yaml

    # Allow Backends to do backend specific tasks
    if function_exists create_designate_pool_configuration_backend; then
        create_designate_pool_configuration_backend
    fi
}

# init_designate - Initialize etc.
function init_designate {
    # Create cache dir
    sudo mkdir -p $DESIGNATE_AUTH_CACHE_DIR
    sudo chown $STACK_USER $DESIGNATE_AUTH_CACHE_DIR
    rm -f $DESIGNATE_AUTH_CACHE_DIR/*

    # Some Designate Backends require mdns be bound to port 53, make that
    # doable.
    sudo setcap 'cap_net_bind_service=+ep' $(readlink -f /usr/bin/python)

    # (Re)create designate database
    recreate_database designate utf8

    # Init and migrate designate database
    $DESIGNATE_BIN_DIR/designate-manage database sync

    init_designate_backend
}

# install_designate - Collect source and prepare
function install_designate {
    if is_ubuntu; then
        install_package libcap2-bin
    elif is_fedora; then
        # bind-utils package provides `dig`
        install_package libcap bind-utils
    fi

    git_clone $DESIGNATE_REPO $DESIGNATE_DIR $DESIGNATE_BRANCH
    setup_develop $DESIGNATE_DIR

    # Install reqs for tooz driver
    if [[ "$DESIGNATE_COORDINATION_URL" =~ "memcached" ]]; then
        pip_install_gr "pymemcache"
    fi

    install_designate_backend
}

# install_designateclient - Collect source and prepare
function install_designateclient {
    if use_library_from_git "python-designateclient"; then
        git_clone_by_name "python-designateclient"
        setup_dev_lib "python-designateclient"
    else
        pip_install_gr "python-designateclient"
    fi
}

# install_designatedashboard - Collect source and prepare
function install_designatedashboard {
    git_clone_by_name "designate-dashboard"
    setup_dev_lib "designate-dashboard"

    for panel in _1710_project_dns_panel_group.py \
                 _1721_dns_zones_panel.py \
                 _1722_dns_reversedns_panel.py; do
        ln -fs $DESIGNATEDASHBOARD_DIR/designatedashboard/enabled/$panel $HORIZON_DIR/openstack_dashboard/local/enabled/$panel
    done
}

# install_designatetempest - Collect source and prepare
function install_designatetempest {
    git_clone_by_name "designate-tempest-plugin"
    setup_dev_lib "designate-tempest-plugin"
}

# start_designate - Start running processes
function start_designate {
    start_designate_backend

    run_process designate-central "$DESIGNATE_BIN_DIR/designate-central --config-file $DESIGNATE_CONF"
    run_process designate-api "$DESIGNATE_BIN_DIR/designate-api --config-file $DESIGNATE_CONF"
    run_process designate-mdns "$DESIGNATE_BIN_DIR/designate-mdns --config-file $DESIGNATE_CONF"
    run_process designate-agent "$DESIGNATE_BIN_DIR/designate-agent --config-file $DESIGNATE_CONF"
    run_process designate-sink "$DESIGNATE_BIN_DIR/designate-sink --config-file $DESIGNATE_CONF"

    run_process designate-worker "$DESIGNATE_BIN_DIR/designate-worker --config-file $DESIGNATE_CONF"
    run_process designate-producer "$DESIGNATE_BIN_DIR/designate-producer --config-file $DESIGNATE_CONF"

    # Start proxies if enabled
    if is_service_enabled designate-api && is_service_enabled tls-proxy; then
        start_tls_proxy designate-api '*' $DESIGNATE_SERVICE_PORT $DESIGNATE_SERVICE_HOST $DESIGNATE_SERVICE_PORT_INT &
    fi

    if ! timeout $SERVICE_TIMEOUT sh -c "while ! wget --no-proxy -q -O- $DESIGNATE_SERVICE_PROTOCOL://$DESIGNATE_SERVICE_HOST:$DESIGNATE_SERVICE_PORT; do sleep 1; done"; then
        die $LINENO "Designate did not start"
    fi
}

# stop_designate - Stop running processes
function stop_designate {
    stop_process designate-central
    stop_process designate-api
    stop_process designate-mdns
    stop_process designate-agent
    stop_process designate-sink
    stop_process designate-worker
    stop_process designate-producer

    stop_designate_backend
}

# This is the main for plugin.sh
if is_service_enabled designate; then
    # Sanify check for agent backend
    # ------------------------------
    if ! is_service_enabled designate-agent && [ "$DESIGNATE_BACKEND_DRIVER" == "agent" ]; then
        die $LINENO "To use the agent backend, you must enable the designate-agent service"
    fi

    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        echo_summary "Installing Designate client"
        install_designateclient

        echo_summary "Installing Designate"
        stack_install_service designate

        if is_service_enabled horizon; then
            echo_summary "Installing Designate dashboard"
            install_designatedashboard
        fi

        if is_service_enabled tempest; then
            echo_summary "Installing Designate Tempest Plugin"
            install_designatetempest
        fi

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        echo_summary "Configuring Designate"
        configure_designate
        if is_service_enabled horizon; then
            echo_summary "Configuring Designate dashboard"
            configure_designatedashboard
        fi

        if is_service_enabled keystone; then
            echo_summary "Creating Designate Keystone accounts"
            create_designate_accounts
        fi

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        echo_summary "Initializing Designate"
        init_designate

        echo_summary "Starting Designate"
        start_designate

        echo_summary "Creating Pool Configuration"
        create_designate_pool_configuration
    elif [[ "$1" == "stack" && "$2" == "test-config" ]]; then
        echo_summary "Configuring Tempest options for Designate"
        configure_designate_tempest
    fi

    if [[ "$1" == "unstack" ]]; then
        stop_designate
    fi

    if [[ "$1" == "clean" ]]; then
        echo_summary "Cleaning Designate"
        cleanup_designate
    fi
fi

# Restore xtrace
$XTRACE
