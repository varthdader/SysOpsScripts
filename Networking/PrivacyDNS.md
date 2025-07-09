A step-by-step guide to install Pi-hole and Unbound as Docker containers on an Ubuntu server, and configure Pi-hole to resolve DNS requests through Unbound.

### Prerequisites

1. **Ubuntu Server**: Ensure you have an Ubuntu server running.
2. **Docker Installed**: Make sure Docker and Docker Compose are installed. Install Docker if not already done:

   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   ```

3. **Set Up Docker Permissions**: To run Docker without `sudo`, add your user to the Docker group:

   ```bash
   sudo usermod -aG docker $USER
   ```

   Log out and back in, or reboot the server.

### Step 1: Create a Docker Network

Create a network for the containers to communicate:

```bash
docker network create pihole_network
```

### Step 2: Set Up Unbound

1. **Create Unbound Directory**:

   ```bash
   mkdir -p ~/unbound
   ```

2. **Create Unbound Configuration File**:

   Create a file named `unbound.conf` in `~/unbound`:

   ```bash
   nano ~/unbound/unbound.conf
   ```

   Add the following configuration:

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
           forward-addr: 1.1.1.1  # Cloudflare DNS
           forward-addr: 8.8.8.8   # Google DNS
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

### Step 3: Set Up Pi-hole

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

   Navigate to the Pi-hole directory and start the container:

   ```bash
   cd ~/pihole
   docker-compose up -d
   ```

### Step 4: Configure Pi-hole to Use Unbound

Pi-hole should already be configured to use Unbound as its DNS resolver through the Docker Compose setup. To verify:

1. Access the Pi-hole admin interface by navigating to `http://<YOUR_SERVER_IP>/admin`.
2. Log in with the password you set.
3. Go to **Settings** > **DNS** and ensure that "Custom 1 (IPv4)" is set to `127.0.0.1#5335`.

### Step 5: Test the Configuration

1. Use a device connected to your network and set its DNS to the IP address of your Ubuntu server.
2. Test DNS resolution using a command line:

   ```bash
   nslookup google.com <YOUR_SERVER_IP>
   ```

### Conclusion

You now have a Pi-hole and Unbound setup running as Docker containers on your Ubuntu server! Adjust configurations as needed for your specific environment.