import csv
import argparse
from collections import defaultdict

# Mapping of protocol numbers to protocol names: https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml
PROTOCOL_MAP = {
    '6': 'tcp',
    '17': 'udp',
    '1': 'icmp'
}

# Lookup table. key: dstport, protocol. value: tag
def lookupTable(lookup_file):
    table = dict()
    # going through line by line in a csv file
    with open(lookup_file, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile) 
        # separates each column into a variable to make an entry in the dictionary
        for row in reader:
            dstport = row['dstport'].strip().lower()
            protocol = row['protocol'].strip().lower()
            tag = row['tag'].strip()
            table[(dstport, protocol)] = tag
    return table

# parse through the flow logs
def parse(flowLog_file, lookup_table):
    tag_counts = defaultdict(int)
    port_proto_counts = defaultdict(int)

    # opening the csv file and reading line by line
    with open(flowLog_file, mode='r') as f:
        for line in f:
            # edge case when lines are just blank
            if not line.strip():
                continue
            # separates each column into an array
            parts = line.strip().split()
            # retrieve dstport and protocol_num
            try:
                dstport = parts[5].strip().lower()      # dstport: col 6
                protocol_num = parts[7].strip()         # protocol: col 8
            except IndexError:
                continue 

            # converting protocol # to protocol name
            protocol_name = PROTOCOL_MAP.get(protocol_num)
            # skip unknown protocols
            if protocol_name is None:
                continue  

            # creating lookup key
            lookup_key = (dstport, protocol_name)

            # Find the tag, or default to "Untagged"
            tag = lookup_table.get(lookup_key, 'Untagged')

            # Update counts
            tag_counts[tag] += 1
            port_proto_counts[(dstport, protocol_name)] += 1

    return tag_counts, port_proto_counts

# Utilized GPT to help w/ writing the output into a result file
def write_output(tag_counts, port_proto_counts, output_file):
    with open(output_file, mode='w') as f:
        # Tag Counts
        f.write("Tag Counts:\n")
        f.write("Tag,Count\n")
        for tag, count in tag_counts.items():
            f.write(f"{tag},{count}\n")

        f.write("\n")

        # Port/Protocol Counts
        f.write("Port/Protocol Combination Counts:\n")
        f.write("Port,Protocol,Count\n")
        for (port, protocol), count in port_proto_counts.items():
            f.write(f"{port},{protocol},{count}\n")

def main():
    # arguements to add required files
    parser = argparse.ArgumentParser(description="Flow Log Parser and Tag Counter")
    parser.add_argument('--flowlog', required=True, help='flow log path')
    parser.add_argument('--lookup', required=True, help='lookup table file path')
    parser.add_argument('--output', default='output.txt', help='results file (default: output.txt)')

    # run script
    args = parser.parse_args()
    lookup_table = lookupTable(args.lookup)
    tag_counts, port_proto_counts = parse(args.flowlog, lookup_table)
    write_output(tag_counts, port_proto_counts, args.output)

    print(f"Processing complete! Results saved to {args.output}")

if __name__ == "__main__":
    main()
    
