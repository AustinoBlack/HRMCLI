# add to .bashrc to execute PcsCli shell to  
# automatically run the PcsCLI script on login

if [ -t 0 ]; then
    #!/bin/bash
    USER="user"
    LAST_LOGIN=$(last -i $USER | head -1 | awk '{print $6, $7, $8, $9 " from " $3}')
    echo "Last login: $LAST_LOGIN"
    python3 /PcsCli/pcscli/pcs_shell.py
    exit
fi

