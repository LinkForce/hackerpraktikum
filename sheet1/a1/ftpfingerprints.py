#Dictionary of FTP fingerprints used to check for FTPd names

ftp_fingerprints = {
'''214-The following commands are recognized (* =>\'s unimplemented):
214-CWD     XCWD    CDUP    XCUP    SMNT*   QUIT    PORT    PASV
214-EPRT    EPSV    ALLO*   RNFR    RNTO    DELE    MDTM    RMD
214-XRMD    MKD     XMKD    PWD     XPWD    SIZE    SYST    HELP
214-NOOP    FEAT    OPTS    AUTH*   CCC*    CONF*   ENC*    MIC*
214-PBSZ*   PROT*   TYPE    STRU    MODE    RETR    STOR    STOU
214-APPE    REST    ABOR    USER    PASS    ACCT*   REIN*   LIST
214-NLST    STAT    SITE    MLSD    MLST
214 Direct comments to root@fingerprinting
''' : 'pro-ftpd',
'''214-The following SITE commands are recognized
 ALIAS
 CHMOD
 IDLE
 UTIME
214 Pure-FTPd - http://pureftpd.org/
''': 'pure-ftpd',
'''530 Please login with USER and PASS.''': 'vs-ftpd'

}
