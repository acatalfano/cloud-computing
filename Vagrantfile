# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"   # Ubuntu 20.04 (use focal64 for 20.04)

  # increase boot timeout from default 5 minutes to 10 minutes
  config.vm.boot_timeout = 600

  config.vm.provider "virtualbox" do |vb|
    # Display the VirtualBox GUI when booting the machine
     vb.gui = true

    # Customize the amount of memory on the VM:
     vb.memory = "2048"

    # Use VMSVGA
    vb.customize ["modifyvm", :id, "--graphicscontroller", "vmsvga"]
  end

  config.vm.provision "shell", path: "./bootstrap.sh"
  config.vm.provision "file", source: "./rsa_private.pem", destination: "~/.ssh/id_rsa"

  # copy AWS credentials
  config.vm.provision "file", source: ".aws", destination: "~/.aws"

  # let's also copy our ansible.cfg, MyInventory and cloud.yaml file
  config.vm.provision "file", source: "./ansible.cfg", destination: "~/.ansible.cfg"

  # Ansible provisioner
  config.vm.provision "ansible_local" do |ansible|
    ansible.playbook = "./playbook_master.yml"
    # ansible.playbook = "./playbook_master_cleanup.yml"
    ansible.install_mode = :pip
    ansible.pip_install_cmd = "sudo apt install -y python3-distutils && curl https://bootstrap.pypa.io/get-pip.py | sudo python3"
    ansible.verbose = true
    ansible.install = true  # installs ansible (and hence python on VM)
    ansible.limit = "all"
    ansible.inventory_path = "./Inventory"  # inventory file
  end
end
