# add to .bashrc to execute PcsCli shell to  
# automatically run the PcsCLI script on login

if [ -t 0 ]; then
    python3 /PcsCli/pcscli/pcs_shell.py
    exit
fi

