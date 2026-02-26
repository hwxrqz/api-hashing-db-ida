#!/usr/bin/python3

import ida_idaapi, ida_idp, ida_ua, ida_bytes, ida_diskio, zlib, apihashes_search

class hk(ida_idp.IDB_Hooks):
    def CheckHash(self, ea, value):
        fname = apihashes_search.FindHash(value)
        if fname:
            print("ah [%X] Found API hash for %s" % (ea, fname));
            ida_bytes.set_cmt(ea, fname, False)


    def make_code(self, insn):
        for op in insn.ops:
            if op.type == ida_ua.o_void:
                break
            if op.type == ida_ua.o_imm and op.value != 0:
                self.CheckHash(insn.ea, op.value)

        return None
    def make_data(self, ea, flags, tid, sz):
        if sz == 4:
            opValue = ida_bytes.get_dword(ea)
        elif sz == 8:
            opValue = ida_bytes.get_qword(ea)
        else:
            return None
        self.CheckHash(ea, opValue)
        return None

class apihashes_plugin(ida_idaapi.plugin_t):
    flags = 0
    comment = "Resolve API hashes on code/data creation"
    help = "No help"
    wanted_name = "Resolve API"
    wanted_hotkey = ""
    

    def init(self):
        print("apihashes plugin by @section_remadev (c) 2025");
        self.hk = hk()
        self.hk.hook()
        apihashes_search.LoadHashes(ida_diskio.idadir(ida_diskio.PLG_SUBDIR) + "/apihashes_storage.bin")

        return ida_idaapi.PLUGIN_KEEP

    def run(self, arg):
        pass

    def term(self):
        pass


def PLUGIN_ENTRY():
    return apihashes_plugin()
