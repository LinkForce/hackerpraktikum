#define _GNU_SOURCE

#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <dlfcn.h>
#include <sys/stat.h>
#include <sys/types.h>

//defining types to original functions that the sandbox controls
typedef ssize_t (*_open_t)(int, void *, size_t);
typedef ssize_t (*_read_t)(int, void *, size_t);
typedef int (*_stat_t)(const char *, struct stat *);
typedef int (*_lstat_t)(const char *, struct stat *);


//functions to return the real functions if the requested file is on the whitelist
ssize_t _open(int fd, void *data, size_t size) {
    return ((_open_t)dlsym(RTLD_NEXT, "open"))(fd, data, size);
}

ssize_t _read(int fd, void *data, size_t size) {
    return ((_read_t)dlsym(RTLD_NEXT, "read"))(fd, data, size);
}

int _stat(const char *path, struct stat *buf) {
    return ((_stat_t)dlsym(RTLD_NEXT, "stat"))(path, buf);
}

int _lstat(const char *path, struct stat *buf) {
    return ((_lstat_t)dlsym(RTLD_NEXT, "lstat"))(path, buf);
}

int isWhitelisted(char *filename){
    FILE* file = fopen("whitelist", "r");
    char line[256];

    int isfile = 0;

    //iterate through the whitelist file
    while (fgets(line, sizeof(line), file)) {
        int i = -1;

        //find line break and replace with \0 to use strcmp
        while(line[++i] != '\n');

        line[i] = '\0';

        isfile = strcmp(line,filename);
    
        //if file is this line of the whitelist, just break the loop and return
        //strcmp return 0 when str1 == str2, so we have to invert the result
        if (!isfile)
            break;
    }
    
    fclose(file);

    //inverting for the same reason stated above
    return !isfile;
}

//edited functions that checks the whitelist before returng
ssize_t open(int fd, void *data, size_t size) {
    if(isWhitelisted((char*)data))
        return _open(fd,data,size);
    
    return (ssize_t)NULL;
}

ssize_t read(int fd, void *data, size_t size) {
    if(isWhitelisted((char*)data))
        return _read(fd,data,size);
    
    return (ssize_t)NULL;
}

int stat(const char *path, struct stat *buf) {
    if(isWhitelisted((char*)path))
        return _stat(path,buf);

    return 0;
}

int lstat(const char *path, struct stat *buf) {
    if(isWhitelisted((char*)path))
        return _lstat(path,buf);

    return 0;
}
