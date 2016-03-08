import csv


def main():
    with open('ma_exprs.csv') as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = list(reader)

    with open('np_exprs.csv') as f:
        reader = csv.reader(f)
        next(reader)
        rows.extend(list(reader))

    nc = NeuronClassifier()
    new_rows = []

    for row in rows:
        try:
            for neuron_name in nc[row[0]]:
                new_row = row.copy()
                new_row[0] = neuron_name
                new_rows.append(new_row)
        except ValueError:
            new_rows.append(row)

    with open('combined.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(sorted(new_rows, key=lambda x: (x[1], x[0], x[2])))


class NeuronClassifier:
    def __init__(self):
        self._nodes = set(NODES)
        self._subs = dict(ALLOWED_SUBSTITUTIONS)

    def __getitem__(self, key):
        if key in self._nodes:
            return [key]

        ret = []
        for node in self._nodes:
            if node.startswith(key) and self.partner_exists(key, node):
                ret.append(node)

        if not ret:
            raise ValueError("'{}' does not correspond to a neuron class.".format(key))

        return sorted(ret)

    def partner_exists(self, key, node):
        # check that remaining characters are R, L, D, V or numbers
        if not set(str(i) for i in range(10)).union(self._subs).issuperset(node[len(key):]):
            return False

        # check that there are partner nodes
        for i, node_char in enumerate(node[len(key):], len(key)):
            if node_char.isdigit():
                return True
            elif ''.join([node[:i], self._subs[node_char], node[i+1:]]) not in self._nodes:
                return False

        return True


ALLOWED_SUBSTITUTIONS = tuple([
    ('D', 'V'),
    ('V', 'D'),
    ('L', 'R'),
    ('R', 'L')
])

NODES = (
    'ADAL',
    'ADAR',
    'ADEL',
    'ADER',
    'ADFL',
    'ADFR',
    'ADLL',
    'ADLR',
    'AFDL',
    'AFDR',
    'AIAL',
    'AIAR',
    'AIBL',
    'AIBR',
    'AIML',
    'AIMR',
    'AINL',
    'AINR',
    'AIYL',
    'AIYR',
    'AIZL',
    'AIZR',
    'ALA',
    'ALML',
    'ALMR',
    'ALNL',
    'ALNR',
    'AQR',
    'AS1',
    'AS10',
    'AS11',
    'AS2',
    'AS3',
    'AS4',
    'AS5',
    'AS6',
    'AS7',
    'AS8',
    'AS9',
    'ASEL',
    'ASER',
    'ASGL',
    'ASGR',
    'ASHL',
    'ASHR',
    'ASIL',
    'ASIR',
    'ASJL',
    'ASJR',
    'ASKL',
    'ASKR',
    'AUAL',
    'AUAR',
    'AVAL',
    'AVAR',
    'AVBL',
    'AVBR',
    'AVDL',
    'AVDR',
    'AVEL',
    'AVER',
    'AVFL',
    'AVFR',
    'AVG',
    'AVHL',
    'AVHR',
    'AVJL',
    'AVJR',
    'AVKL',
    'AVKR',
    'AVL',
    'AVM',
    'AWAL',
    'AWAR',
    'AWBL',
    'AWBR',
    'AWCL',
    'AWCR',
    'BAGL',
    'BAGR',
    'BDUL',
    'BDUR',
    'CANL',
    'CANR',
    'CEPDL',
    'CEPDR',
    'CEPVL',
    'CEPVR',
    'DA1',
    'DA2',
    'DA3',
    'DA4',
    'DA5',
    'DA6',
    'DA7',
    'DA8',
    'DA9',
    'DB1',
    'DB2',
    'DB3',
    'DB4',
    'DB5',
    'DB6',
    'DB7',
    'DD1',
    'DD2',
    'DD3',
    'DD4',
    'DD5',
    'DD6',
    'DVA',
    'DVB',
    'DVC',
    'FLPL',
    'FLPR',
    'HSNL',
    'HSNR',
    'I1L',
    'I1R',
    'I2L',
    'I2R',
    'I3',
    'I4',
    'I5',
    'I6',
    'IL1DL',
    'IL1DR',
    'IL1L',
    'IL1R',
    'IL1VL',
    'IL1VR',
    'IL2DL',
    'IL2DR',
    'IL2L',
    'IL2R',
    'IL2VL',
    'IL2VR',
    'LUAL',
    'LUAR',
    'M1',
    'M2L',
    'M2R',
    'M3L',
    'M3R',
    'M4',
    'M5',
    'MCL',
    'MCR',
    'MI',
    'NSML',
    'NSMR',
    'OLLL',
    'OLLR',
    'OLQDL',
    'OLQDR',
    'OLQVL',
    'OLQVR',
    'PDA',
    'PDB',
    'PDEL',
    'PDER',
    'PHAL',
    'PHAR',
    'PHBL',
    'PHBR',
    'PHCL',
    'PHCR',
    'PLML',
    'PLMR',
    'PLNL',
    'PLNR',
    'PQR',
    'PVCL',
    'PVCR',
    'PVDL',
    'PVDR',
    'PVM',
    'PVNL',
    'PVNR',
    'PVPL',
    'PVPR',
    'PVQL',
    'PVQR',
    'PVR',
    'PVT',
    'PVWL',
    'PVWR',
    'RIAL',
    'RIAR',
    'RIBL',
    'RIBR',
    'RICL',
    'RICR',
    'RID',
    'RIFL',
    'RIFR',
    'RIGL',
    'RIGR',
    'RIH',
    'RIML',
    'RIMR',
    'RIPL',
    'RIPR',
    'RIR',
    'RIS',
    'RIVL',
    'RIVR',
    'RMDDL',
    'RMDDR',
    'RMDL',
    'RMDR',
    'RMDVL',
    'RMDVR',
    'RMED',
    'RMEL',
    'RMER',
    'RMEV',
    'RMFL',
    'RMFR',
    'RMGL',
    'RMGR',
    'RMHL',
    'RMHR',
    'SAADL',
    'SAADR',
    'SAAVL',
    'SAAVR',
    'SABD',
    'SABVL',
    'SABVR',
    'SDQL',
    'SDQR',
    'SIADL',
    'SIADR',
    'SIAVL',
    'SIAVR',
    'SIBDL',
    'SIBDR',
    'SIBVL',
    'SIBVR',
    'SMBDL',
    'SMBDR',
    'SMBVL',
    'SMBVR',
    'SMDDL',
    'SMDDR',
    'SMDVL',
    'SMDVR',
    'URADL',
    'URADR',
    'URAVL',
    'URAVR',
    'URBL',
    'URBR',
    'URXL',
    'URXR',
    'URYDL',
    'URYDR',
    'URYVL',
    'URYVR',
    'VA1',
    'VA10',
    'VA11',
    'VA12',
    'VA2',
    'VA3',
    'VA4',
    'VA5',
    'VA6',
    'VA7',
    'VA8',
    'VA9',
    'VB1',
    'VB10',
    'VB11',
    'VB2',
    'VB3',
    'VB4',
    'VB5',
    'VB6',
    'VB7',
    'VB8',
    'VB9',
    'VC1',
    'VC2',
    'VC3',
    'VC4',
    'VC5',
    'VC6',
    'VD1',
    'VD10',
    'VD11',
    'VD12',
    'VD13',
    'VD2',
    'VD3',
    'VD4',
    'VD5',
    'VD6',
    'VD7',
    'VD8',
    'VD9'
)

if __name__ == '__main__':
    main()
    print('done')
