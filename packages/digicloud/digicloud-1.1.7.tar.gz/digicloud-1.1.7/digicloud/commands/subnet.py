"""
    DigiCloud Subnet Service.
"""

from cliff.command import Command
from cliff.lister import Lister
from cliff.show import ShowOne

from ..cli import parseractions
from ..utils import tabulate


class CreateSubnet(ShowOne):
    """Create Network Subnet"""

    def get_parser(self, prog_name):
        parser = super(CreateSubnet, self).get_parser(prog_name)
        subnet_group = parser.add_mutually_exclusive_group()
        parser.add_argument(
            'name',
            metavar='<name>',
            help='Subnet name'
        )
        parser.add_argument(
            '--ip-version',
            default='4',
            metavar='<ip_version>',
            help='IP version, default to IPv4'
        )
        parser.add_argument(
            '--cidr',
            required=True,
            metavar='<cidr>',
            help='CIDR, e.g: 10.0.0.0/16'
        )
        parser.add_argument(
            '--network',
            required=True,
            metavar='<network>',
            help='network name or ID'
        )
        parser.add_argument(
            '--enable-dhcp',
            metavar='<enable_dhcp>',
            help='Enable DHCP for this subnet'
        )
        subnet_group.add_argument(
            '--disable-gateway',
            action='store_true',
            help='Disable gateway for this subnet'
        )
        subnet_group.add_argument(
            '--gateway-ip',
            metavar='<gateway_ip>',
            help='Set gateway IP for this subnet'
        )
        parser.add_argument(
            '--allocation-pool',
            metavar='start=<ip-address>,end=<ip-address>',
            dest='allocation_pools',
            action=parseractions.MultiKeyValueAction,
            required_keys=['start', 'end'],
            help='Allocation pool IP addresses for this subnet e.g.: start=192.168.199.2,'
                 'end=192.168.199.254 (repeat option to add multiple IP addresses)'
        )
        parser.add_argument(
            '--dns-server',
            metavar='<dns_server>',
            action='append',
            dest='dns_server',
            help="DNS server for this subnet (repeat option to set multiple DNS servers)"
        )
        parser.add_argument(
            '--host-route',
            metavar='destination=<subnet>,nexthop=<ip-address>',
            dest='host_route',
            action=parseractions.MultiKeyValueAction,
            required_keys=['destination', 'nexthop'],
            help="Additional route for this subnet "
                 "e.g.: destination=10.10.0.0/16,nexthop=192.168.71.254 "
                 "destination: destination subnet (in CIDR notation) "
                 "nexthop: nexthop IP address "
                 "(repeat option to add multiple routes)")

        return parser

    def take_action(self, parsed_args):
        uri = '/networks/%s/subnets' % parsed_args.network
        payload = {
            'ip_version': parsed_args.ip_version,
            'cidr': parsed_args.cidr,
            'subnet_name': parsed_args.name,
            **self._get_optional_fields(parsed_args)
        }
        data = self.app.session.post(uri, payload)

        return tabulate(data)

    def _get_optional_fields(self, args):
        optional_args = {}

        if args.enable_dhcp is not None:
            optional_args["enable_dhcp"] = args.enable_dhcp

        # NOTE: It's boolean
        if args.disable_gateway:
            optional_args["gateway_ip"] = None

        if args.gateway_ip is not None:
            optional_args["gateway_ip"] = args.gateway_ip

        if args.allocation_pools is not None:
            optional_args["allocation_pools"] = args.allocation_pools

        if args.dns_server is not None:
            optional_args["dns_servers"] = args.dns_server

        if args.host_route is not None:
            optional_args["host_routes"] = args.host_route

        return optional_args


class ListSubnet(Lister):
    """List subnets."""

    def take_action(self, parsed_args):
        data = self.app.session.get('/subnets')

        return tabulate(data)


class ShowSubnet(ShowOne):
    """Show subnet details."""

    def get_parser(self, prog_name):
        parser = super(ShowSubnet, self).get_parser(prog_name)
        parser.add_argument(
            'subnet',
            metavar='<subnet>',
            help='Subnet name or ID',
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/subnets/%s' % parsed_args.subnet
        data = self.app.session.get(uri)

        return tabulate(data)


class DeleteSubnet(Command):
    """Delete subnet."""

    def get_parser(self, prog_name):
        parser = super(DeleteSubnet, self).get_parser(prog_name)
        parser.add_argument(
            'subnet',
            metavar='<subnet>',
            help='subnet name or ID'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/subnets/%s' % parsed_args.subnet
        self.app.session.delete(uri)


class UpdateSubnet(ShowOne):
    """Update subnets."""
    def get_parser(self, prog_name):
        parser = super(UpdateSubnet, self).get_parser(prog_name)
        parser.add_argument(
            'subnet',
            metavar='<subnet>',
            help='Subnet ID',
        )
        parser.add_argument(
            '--name',
            required=True,
            metavar='<Name>',
            help='New name for subnet.'
        )
        parser.add_argument(
            '--description',
            metavar='<Description>',
            help='New description for subnet.'
        )
        return parser

    def take_action(self, parsed_args):
        uri = '/subnets/%s' % parsed_args.subnet
        payload = {
            'name': parsed_args.name,
            'description': parsed_args.description,
        }
        data = self.app.session.patch(uri, payload)
        return tabulate(data)
