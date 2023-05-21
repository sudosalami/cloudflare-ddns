import cloudflare


if __name__ == '__main__':
    root = cloudflare.DNSRecord()
    root.validate_record()