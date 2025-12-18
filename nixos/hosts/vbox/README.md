# Oracle VirtualBox Setup

1. Download graphical [NixOS](https://nixos.org/download/#nixos-virtualbox) ISO image.
2. Create a new virtual machine within VirtualBox.
   ```
   Name: NixOS
   ISO Image: <select download>
   Type: Linux
   Subtype: Other Linux
   Base Memory: >6 GB
   Processors: >2
   Enable EFI: Yes (for systemd)
   Create Virtual Hard Disk Memory: >50 GB
   ```
3. Using the graphical installer, setup NixOS then shutdown VM.
4. Withn VirtualBox Manager -> select NixOS VM -> Settings -> Storage -> Remove CD.
5. Within VirtualBox Manager -> slect NixOS VM -> Start.
7. Open default terminal and perform the below actions:
   ```
   > cd ~
   > nix-shell -p git
   > git clone https://github.com/AndrewFarber/AndrewOS
   > cd ~/AndrewOS/nixos/hosts/vbox
   > rm hardware.nix
   > nixos-generate-config --dir .
   > rm configuration.nix
   > mv hardware-configuration.nix hardware.nix
   ```
8. Copy `.env.example` to `.env` and update with your user settings:
   ```
   > cd ~/AndrewOS
   > cp .env.example .env
   > nano .env
   ```
9. Rebuild NixOS then reboot.
   ```
   > source .env && sudo nixos-rebuild switch --flake .#vbox --impure
   > reboot
   ```
