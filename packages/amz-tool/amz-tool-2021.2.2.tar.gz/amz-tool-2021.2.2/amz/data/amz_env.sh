# Auto source ROS setup bash
if [ '$AMZ_ROOT' != '' ] && [[ -f $AMZ_ROOT/devel/setup.bash ]]
then
    source $AMZ_ROOT/devel/setup.bash
fi

# Autocomplete support
eval "$(~/.local/bin/register-python-argcomplete ~/.local/bin/amz)"
source $AMZ_CONFIG/python-argcomplete

# Aliases

## Utilities
alias amz_ssh_pilatus="ssh amz@10.33.0.2 -X"
alias amz_car_master="export ROS_MASTER_URI=http://10.33.0.2:11311 ROS_IP=$(hostname --all-ip-addresses | grep 10.33.0)"
alias amz_monitoring="export ROS_MASTER_URI=http://10.33.0.2:11311 && rosrun monitoring_display node_start.py --columns 4"
