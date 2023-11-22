from .target import Target
from ..assemblers.keystone_sparc import KeystoneSparc, keystone
from ..compilers.bcc import Bcc as BccCompiler
from ..assemblers.bcc import Bcc as BccAssembler
from ..disassemblers.capstone import Capstone, capstone
from ..binfmt_tools.elf import ELF
from ..binary_analyzers.angr import Angr
from ..utils.utils import Utils
from ..allocation_management.allocation_management import *

import logging

logger = logging.getLogger(__name__)


class CustomElf(ELF):
    def _init_memory_analysis(self):
        # remove all non-RWX segments
        self._segments = [s for s in self._segments if s["p_flags"] & 0b111 == 0b111]
        block = MappedBlock(
            self._segments[0]["p_offset"],
            self._segments[0]["p_vaddr"],
            self._segments[0]["p_memsz"],
            is_free=False,
            flag=MemoryFlag.RWX,
        )
        self.p.allocation_manager.add_block(block)

        unused_funcs = self.p.binary_analyzer.get_unused_funcs()
        # TODO: ideally, we should use the unused_funcs from binary_analyzer, but it currently has too many false positives
        unused_funcs = [
            {"addr": 1073746424, "size": 12},
            {"addr": 1073746540, "size": 12},
            {"addr": 1073750572, "size": 108},
            {"addr": 1073750680, "size": 56},
            {"addr": 1073750736, "size": 80},
            {"addr": 1073750816, "size": 56},
            {"addr": 1073750872, "size": 60},
            {"addr": 1073750932, "size": 36},
            {"addr": 1073750968, "size": 36},
            {"addr": 1073751004, "size": 36},
            {"addr": 1073751040, "size": 108},
            {"addr": 1073751148, "size": 56},
            {"addr": 1073751204, "size": 56},
            {"addr": 1073751260, "size": 56},
            {"addr": 1073751316, "size": 44},
            {"addr": 1073751360, "size": 44},
            {"addr": 1073751404, "size": 64},
            {"addr": 1073751468, "size": 300},
            {"addr": 1073751768, "size": 116},
            {"addr": 1073751884, "size": 300},
            {"addr": 1073752184, "size": 140},
            {"addr": 1073752360, "size": 96},
            {"addr": 1073752504, "size": 52},
            {"addr": 1073756968, "size": 4},
            {"addr": 1073757864, "size": 12},
            {"addr": 1073758012, "size": 80},
            {"addr": 1073758172, "size": 48},
            {"addr": 1073758220, "size": 116},
            {"addr": 1073758336, "size": 64},
            {"addr": 1073758920, "size": 28},
            {"addr": 1073759052, "size": 56},
            {"addr": 1073760048, "size": 60},
            {"addr": 1073761080, "size": 40},
            {"addr": 1073762588, "size": 168},
            {"addr": 1073762940, "size": 112},
            {"addr": 1073763504, "size": 32},
            {"addr": 1073765352, "size": 56},
            {"addr": 1073765640, "size": 20},
            {"addr": 1073767316, "size": 104},
            {"addr": 1073768572, "size": 408},
            {"addr": 1073769932, "size": 404},
            {"addr": 1073770832, "size": 32},
            {"addr": 1073770864, "size": 20},
            {"addr": 1073770884, "size": 24},
            {"addr": 1073771056, "size": 8},
            {"addr": 1073772108, "size": 12},
        ]

        for func in unused_funcs:
            file_offset = self.p.binary_analyzer.mem_addr_to_file_offset(func["addr"])
            block = MappedBlock(
                file_offset,
                func["addr"],
                func["size"],
                is_free=True,
                flag=MemoryFlag.RWX,
            )
            self.p.allocation_manager.add_block(block)


class ElfLeon3Bare(Target):
    NOP_BYTES = b"\x01\x00\x00\x00"
    NOP_SIZE = 4
    JMP_ASM = "b {dst}\nnop"  # nop due to delay slot
    JMP_SIZE = 8

    @staticmethod
    def detect_target(binary_path):
        with open(binary_path, "rb") as f:
            magic = f.read(0x14)
            # NOTE: probably should not default sparc to this target, but it's fine for now
            if magic.startswith(b"\x7fELF") and magic.startswith(
                b"\x00\x02", 0x12
            ):  # EM_SPARC
                return True
        return False

    def get_assembler(self, assembler="keystone"):
        if assembler == "keystone":
            return KeystoneSparc(
                self.p,
                keystone.KS_ARCH_SPARC,
                keystone.KS_MODE_SPARC32 + keystone.KS_MODE_BIG_ENDIAN,
            )
        elif assembler == "bcc":
            return BccAssembler(self.p)
        raise NotImplementedError()

    def get_allocation_manager(self, allocation_manager="default"):
        if allocation_manager == "default":
            return AllocationManager(self.p)
        raise NotImplementedError()

    def get_compiler(self, compiler="bcc"):
        if compiler == "bcc":
            return BccCompiler(self.p)
        raise NotImplementedError()

    def get_disassembler(self, disassembler="capstone"):
        if disassembler == "capstone":
            return Capstone(capstone.CS_ARCH_SPARC, capstone.CS_MODE_BIG_ENDIAN)
        raise NotImplementedError()

    def get_binfmt_tool(self, binfmt_tool="custom"):
        if binfmt_tool == "custom":
            return CustomElf(self.p, self.binary_path)
        raise NotImplementedError()

    def get_binary_analyzer(self, binary_analyzer="angr"):
        if binary_analyzer == "angr":
            return Angr(self.binary_path)
        raise NotImplementedError()

    def get_utils(self):
        return Utils(self.p, self.binary_path)
