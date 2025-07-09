Here's a comprehensive guide that includes setting up Pi-hole, Unbound, and using No-IP's enhanced DNS service, ensuring Unbound uses the No-IP service for DNS resolution.

### Prerequisites

1. **Ubuntu Server**: Ensure you have an Ubuntu server running.
2. **Docker Installed**: Make sure Docker and Docker Compose are installed.

### Step 1: Create a No-IP Account

1. Go to [No-IP.com](https://www.noip.com) and create a free account.
2. Set up a hostname through their dashboard.

### Step 2: Install the Dynamic Update Client (DUC)

1. **Download the DUC**:

   Open a terminal and run the following command:

   ```bash
wget --content-disposition https://www.noip.com/download/linux/latest
```

2. **Extract and Install**:

   Change to the directory where the DUC was downloaded and install it:

   ```bash

tar xf noip-duc_3.3.0.tar.gz
   cd /home/$USER/noip-duc_3.3.0/binaries
   sudo apt install ./noip-duc_3.3.0_amd64.deb
   ```

### Step 3: Configure DUC

1. **Run the DUC**:

   Start the No-IP DUC:

   ```bash
   noip-duc
   ```

2. **Explore Options**:

   To see available commands and options, run:

   ```bash
   noip-duc --help
   ```

3. **Login with DDNS Keys**:

   To send updates using your DDNS keys, enter:

   ```bash
   noip-duc -g all.ddnskey.com --username <DDNS Key Username> --password <DDNS Key Password>
   ```

   Replace `<DDNS Key Username>` and `<DDNS Key Password>` with your actual credentials.

### Step 4: Create a Docker Network

Create a network for the containers to communicate:

```bash
docker network create pihole_network
```

### Step 5: Set Up Unbound

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

### Step 6: Set Up Pi-hole

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

### Step 7: Configure Pi-hole to Use Unbound

1. **Access the Pi-hole Admin Interface**:

   Navigate to `http://<YOUR_SERVER_IP>/admin` and log in.

2. **Verify DNS Settings**:

   Go to **Settings** > **DNS** and ensure "Custom 1 (IPv4)" is set to `127.0.0.1#5335`.

### Step 8: Test Configuration

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

You've successfully set up No-IP's enhanced DNS service along with Pi-hole and Unbound, ensuring that Unbound uses your No-IP hostname for DNS resolution. Adjust any configurations as needed based on your network requirements!