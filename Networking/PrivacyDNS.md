Creating a user for running Docker containers and running the No-IP DUC in a screen session.

### Prerequisites

1. **Ubuntu Server**: Ensure you have an Ubuntu server running.
2. **Docker Installed**: Make sure Docker and Docker Compose are installed.
3. **Screen Installed**: Install the `screen` utility if it’s not already available:

   ```bash
   sudo apt install screen
   ```

### Step 1: Create a User for Docker

1. **Create a New User**:

   Replace `dockeruser` with your desired username:

   ```bash
   sudo adduser dockeruser
   ```

   Follow the prompts to set a password and fill in user details.

2. **Add User to Docker Group**:

   This allows the user to run Docker commands without sudo:

   ```bash
   sudo usermod -aG docker dockeruser
   ```

3. **Switch to the New User**:

   Log in as the new user:

   ```bash
   su - dockeruser
   ```

### Step 2: Create a No-IP Account

1. Go to [No-IP.com] and create a free account.
2. Set up a hostname through their dashboard.

### Step 3: Install the Dynamic Update Client (DUC)

1. **Download the DUC**:

   Open a terminal and run:

   ```bash
   wget --content-disposition https://www.noip.com/download/linux/latest
   ```

2. **Extract and Install**:

   Change to the directory where the DUC was downloaded and install it:

   ```bash
   cd /home/$USER/noip-duc_3.3.0/binaries
   sudo apt install ./noip-duc_3.3.0_amd64.deb
   ```

### Step 4: Configure DUC in a Screen Session

1. **Start a Screen Session**:

   Run the following command to start a screen session:

   ```bash
   screen -S noip
   ```

2. **Run the DUC**:

   Start the No-IP DUC:

   ```bash
   noip-duc
   ```

3. **Explore Options**:

   To see available commands and options, run:

   ```bash
   noip-duc --help
   ```

4. **Login with DDNS Keys**:

   To send updates using your DDNS keys, enter:

   ```bash
   noip-duc -g all.ddnskey.com --username <DDNS Key Username> --password <DDNS Key Password>
   ```

   Replace `<DDNS Key Username>` and `<DDNS Key Password>` with your actual credentials.

5. **Detach from the Screen Session**:

   Press `Ctrl + A`, then `D` to detach from the screen session while keeping it running in the background.

### Step 5: Create a Docker Network

Create a network for the containers to communicate:

```bash
docker network create pihole_network
```

### Step 6: Set Up Unbound

1. **Create Unbound Directory**:

   ```bash
   mkdir -p ~/unbound
   ```

2. **Create Unbound Configuration File**:

   Create a file named `unbound.conf` in `~/unbound`:

   ```bash
   nano ~/unbound/unbound.conf
   ```

   Add the following configuration, including No-IP's DNS:

   ```plaintext
   server:
       verbosity: 1
       interface: 0.0.0.0
       access-control: 0.0.0.0/0 allow
       root-hints: "/var/lib/unbound/root.hints"
       auto-trust-anchor-file: "/var/lib/unbound/root.key"
       prefetch: yes
       forward-zone:
           name: "."
           forward-addr: <your-hostname>.no-ip.org  # Use your No-IP hostname
   ```

3. **Pull and Run Unbound Container**:

   Run the Unbound container:

   ```bash
   docker run -d --name unbound \
       --network pihole_network \
       -v ~/unbound/unbound.conf:/etc/unbound/unbound.conf \
       -v ~/unbound/root.hints:/var/lib/unbound/root.hints \
       -v ~/unbound/root.key:/var/lib/unbound/root.key \
       --restart unless-stopped \
       nlnetlabs/unbound:latest
   ```

### Step 7: Set Up Pi-hole

1. **Create Pi-hole Directory**:

   ```bash
   mkdir -p ~/pihole
   ```

2. **Create Docker Compose File**:

   Create a file named `docker-compose.yml` in `~/pihole`:

   ```bash
   nano ~/pihole/docker-compose.yml
   ```

   Add the following configuration:

   ```yaml
   version: '3'
   services:
     pihole:
       image: pihole/pihole:latest
       container_name: pihole
       restart: unless-stopped
       networks:
         - pihole_network
       environment:
         - WEBPASSWORD=yourpassword  # Set your password here
         - DNS1=127.0.0.1#5335        # Point to Unbound
         - DNS2=1.1.1.1               # Optional, secondary DNS
       ports:
         - "80:80"
         - "53:53/tcp"
         - "53:53/udp"
       volumes:
         - ./etc-pihole/:/etc/pihole/
         - ./etc-dnsmasq.d/:/etc/dnsmasq.d/

   networks:
     pihole_network:
       external: true
   ```

3. **Start Pi-hole**:

   Navigate to the Pi-hole directory:

   ```bash
   cd ~/pihole
   ```

   Start the container:

   ```bash
   docker-compose up -d
   ```

### Step 8: Configure Pi-hole to Use Unbound

1. **Access the Pi-hole Admin Interface**:

   Navigate to `http://<YOUR_SERVER_IP>/admin` and log in.

2. **Verify DNS Settings**:

   Go to **Settings** > **DNS** and ensure "Custom 1 (IPv4)" is set to `127.0.0.1#5335`.

### Step 9: Test Configuration

1. **Check No-IP Status**:

   Ensure your No-IP hostname is resolving correctly:

   ```bash
   nslookup <your-hostname>.no-ip.org
   ```

2. **Test DNS Resolution**:

   From a connected device, run:

   ```bash
   nslookup google.com <YOUR_SERVER_IP>
   ```

### Conclusion

You've successfully set up No-IP's enhanced DNS service along with Pi-hole and Unbound, ensuring that Unbound uses your No-IP hostname for DNS resolution. You've also created a dedicated user for running Docker containers and configured the No-IP DUC to run in a screen session. Adjust any configurations as needed based on your network requirements!


To automate the process of starting the No-IP Dynamic Update Client (DUC) in a screen session after booting your server, you can create a script and set it to run at startup. Here’s how to do it:

### Step 1: Create the Script

1. **Create a Script File**:

   Open a terminal and create a new script file, e.g., `start_noip_duc.sh`:

   ```bash
   nano ~/start_noip_duc.sh
   ```

2. **Add the Following Script**:

   Add the following content to the script:

   ```bash
   #!/bin/bash
   # Start No-IP DUC in a screen session

   # Create a new screen session named "noip" if it doesn't exist
   if ! screen -list | grep -q "noip"; then
       screen -dmS noip noip-duc -g all.ddnskey.com --username <DDNS Key Username> --password <DDNS Key Password>
   fi
   ```

   Replace `<DDNS Key Username>` and `<DDNS Key Password>` with your actual credentials.

3. **Make the Script Executable**:

   Save the file and exit the editor. Then, make the script executable:

   ```bash
   chmod +x ~/start_noip_duc.sh
   ```

### Step 2: Set Up the Script to Run on Startup

You can use `cron` to run the script at startup:

1. **Edit the Crontab**:

   Open the crontab for the current user:

   ```bash
   crontab -e
   ```

2. **Add the Following Line**:

   At the end of the file, add the following line to run the script at reboot:

   ```bash
   @reboot /bin/bash /home/dockeruser/start_noip_duc.sh
   ```

   Replace `dockeruser` with your actual username if different.

3. **Save and Exit**:

   Save the changes and exit the editor.

### Step 3: Reboot and Test

1. **Reboot Your Server**:

   ```bash
   sudo reboot
   ```

2. **Check if the Screen Session is Running**:

   After rebooting, check if the No-IP DUC is running in a screen session:

   ```bash
   screen -list
   ```

   You should see a session named `noip`.

### Conclusion

With this setup, your No-IP DUC will automatically start in a screen session every time your server boots. This ensures that your dynamic DNS updates are always running without manual intervention.

