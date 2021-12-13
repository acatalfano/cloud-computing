class FilterModule(object):
    def filters(self):
        return {
            'asSecGroupRules': self.filter_as_sec_group_rules,
            'firstNeq': self.filter_first_neq
        }

    def filter_first_neq(self, str_list, bad_val):
        filtered = [val for val in str_list if val != bad_val]
        return filtered[0] if len(filtered) > 0 else ''

    def filter_as_sec_group_rules(self, rules_data):
        return [
            {
                'cidr_ip': rule['ip'],
                'proto': rule['proto'],
                'from_port': self.port_range_start(rule['port_range']),
                'to_port': self.port_range_end(rule['port_range']),
                'rule_desc': rule['description']
            } for rule in rules_data
        ]

    def port_range_start(self, port_range: str) -> int:
        if port_range.lower() == 'all':
            port = 0
        else:
            hyphen_position = port_range.find('-')
            port_str = port_range[0:hyphen_position]\
                if hyphen_position > -1\
                else port_range
            port = int(port_str)
        return port

    def port_range_end(self, port_range: str) -> int:
        if port_range.lower() == 'all':
            port = 65535
        else:
            port = int(port_range[port_range.find('-') + 1:])
        return port
