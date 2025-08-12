from contract.Regex import Regex
from contract.Version import Version


class VersionChecker:
    '''
    public static class
    '''
    FROM_0_4_17_TO_0_5_8 = 'FROM_0_4_17_TO_0_5_8'
    FROM_0_4_17_TO_0_5_8_EXPERIMENTAL = 'FROM_0_4_17_TO_0_5_8_EXPERIMENTAL'
    FROM_0_5_9_TO_0_5_11 = 'FROM_0_5_9_TO_0_5_11'
    FROM_0_5_9_TO_0_5_11_EXPERIMENTAL = 'FROM_0_5_9_TO_0_5_11_EXPERIMENTAL'
    FROM_0_5_12_TO_0_5_15 = 'FROM_0_5_12_TO_0_5_15'
    FROM_0_5_12_TO_0_5_15_EXPERIMENTAL = 'FROM_0_5_12_TO_0_5_15_EXPERIMENTAL'
    FROM_0_6_0_TO_0_6_1 = 'FROM_0_6_0_TO_0_6_1'
    FROM_0_6_2_TO_LATEST = 'FROM_0_6_2_TO_LATEST'
    UNKNOWN = 'UNKNOWN'

    versions = [Version(FROM_0_4_17_TO_0_5_8,
                        Regex.SOLC_0_4_17),
                Version(FROM_0_4_17_TO_0_5_8_EXPERIMENTAL,
                        Regex.ABIENCODER_V2_1),
                Version(FROM_0_5_9_TO_0_5_11,
                        Regex.SOLC_0_5_9),
                Version(FROM_0_5_9_TO_0_5_11_EXPERIMENTAL,
                        Regex.ABIENCODER_V2_2),
                Version(FROM_0_5_12_TO_0_5_15,
                        Regex.SOLC_0_5_12),
                Version(FROM_0_5_12_TO_0_5_15_EXPERIMENTAL,
                        Regex.ABIENCODER_V2_3),
                Version(FROM_0_6_0_TO_0_6_1,
                        Regex.SOLC_0_6_0),
                Version(FROM_0_6_2_TO_LATEST,
                        Regex.SOLC_0_6_2)]
    unknownVersion = Version(UNKNOWN, '')

    @staticmethod
    def checkVersions(binary: str) -> Version:
        '''
        check the version of the binary
        return a Version object
        '''
        for version in VersionChecker.versions:
            if version.checkVersion(binary):
                return version
        return VersionChecker.unknownVersion
