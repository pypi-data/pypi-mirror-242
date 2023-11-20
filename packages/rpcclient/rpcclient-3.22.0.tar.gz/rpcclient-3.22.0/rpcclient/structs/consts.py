O_RDONLY = 0
O_WRONLY = 1
O_RDWR = 2
O_CREAT = 512
O_TRUNC = 1024

R_OK = 0x04

SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2
SEEK_HOLE = 3
SEEK_DATA = 4

S_IFMT = 0o00170000
S_IFSOCK = 0o0140000
S_IFLNK = 0o0120000
S_IFREG = 0o0100000
S_IFBLK = 0o0060000
S_IFDIR = 0o0040000
S_IFCHR = 0o0020000
S_IFIFO = 0o0010000
S_ISUID = 0o0004000
S_ISGID = 0o0002000
S_ISVTX = 0o0001000

SOL_IP = 0
SOL_SOCKET = 65535
SOL_TCP = 6
SOL_UDP = 17

SO_SNDLOWAT = 0x1003
SO_RCVLOWAT = 0x1004
SO_SNDTIMEO = 0x1005
SO_RCVTIMEO = 0x1006

MSG_WAITALL = 0x40
MSG_NOSIGNAL = 524288

AF_UNIX = 1
AF_INET = 2
AF_INET6 = 30

SOCK_STREAM = 1

IPPROTO_TCP = 6

DT_UNKNOWN = 0
DT_FIFO = 1
DT_CHR = 2
DT_DIR = 4
DT_BLK = 6
DT_REG = 8
DT_LNK = 10
DT_SOCK = 12
DT_WHT = 14

RTLD_NOW = 2

SIGABRT = 6
SIGALRM = 14
SIGBUS = 10
SIGCHLD = 20
SIGCONT = 19
SIGEMT = 7
SIGFPE = 8
SIGHUP = 1
SIGILL = 4
SIGINFO = 29
SIGINT = 2
SIGIO = 23
SIGIOT = 6
SIGKILL = 9
SIGPIPE = 13
SIGPROF = 27
SIGQUIT = 3
SIGSEGV = 11
SIGSTOP = 17
SIGSYS = 12
SIGTERM = 15
SIGTRAP = 5
SIGTSTP = 18
SIGTTIN = 21
SIGTTOU = 22
SIGURG = 16
SIGUSR1 = 30
SIGUSR2 = 31
SIGVTALRM = 26
SIGWINCH = 28
SIGXCPU = 24
SIGXFSZ = 25

EPERM = 1
ENOENT = 2
EACCESS = 13
EEXIST = 17
ENOTDIR = 20
EISDIR = 21
EPIPE = 32
EAGAIN = 35
ECONNREFUSED = 61
ENOTEMPTY = 66

F_SETFL = 4
F_GETFL = 3

O_NONBLOCK = 4
