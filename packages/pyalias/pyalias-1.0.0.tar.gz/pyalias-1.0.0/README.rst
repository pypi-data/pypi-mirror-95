#######
pyalias
#######

Define shell shortcut and execute it.


How to use
##########
0. Install pyalias

   .. code::

       $: pip install pyalias

1. Add a configure file at `~/.config/pyalias.yaml`
   .. code::

       - name: test
         description: functional test
         command: echo 'test'
       - name: ssh
         description: test ssh
         command: sshpass -p "password" ssh user@host4

2. List shortcut
   
   .. code::

       $ pyalias list
       * [test] functional test
       * [ssh] test ssh

3. Execute shortcut

   .. code::

       $ pyalias ssh
       Welcome to Ubuntu 20.04.1 LTS (GNU/Linux x86_64)
       
        * Documentation:  https://help.ubuntu.com
        * Management:     https://landscape.canonical.com
        * Support:        https://ubuntu.com/advantage
       
       Welcome to Alibaba Cloud Elastic Compute Service !
