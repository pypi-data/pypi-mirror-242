from typing import Any
import torch
import torch.distributed as dist
from .cofwriter import coflogger, coftb, WRITER_TABLE


class Cofmem:
    def __init__(self) -> None:
        self.writers=None
    def set_writer(self, writer:str=None, tb_name=None):
        if writer is None:
            self.writers = None
            return
        if writer == 'tb':
            coftb(tb_name)
        self.writers = [item.strip() for item in writer.split(',')]
        # self.writer = WRITER_TABLE[writer]
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        self.report_memory_usage(*args, **kwds)
    def report_memory_usage(self, msg=""):
        # MC: Memory Allocated in Current
        # MM: Memory Allocated in Max
        # MR: Memory Reserved by PyTorch
        if self.writers is None:
            # memory report API is time-cost; therefore, do nothing if user don't specify the writer
            return
        GB = 1024*1024*1024
        MA = torch.cuda.memory_allocated()/GB
        MM = torch.cuda.max_memory_allocated()/GB
        MR = torch.cuda.memory_reserved()/GB
        memory_report_string = f"{msg} GPU Memory Report (GB): MA = {MA:.2f} | "\
                        f"MM = {MM:.2f} | "\
                        f"MR = {MR:.2f}"
        memory_report_dict = {'MA':MA, 'MM':MM, 'MR':MR}

        for writer in self.writers:
            if writer in ['tb', 'csv']:
                # write time profiling results in dictionary format
                WRITER_TABLE[writer](memory_report_dict)
            elif writer in ['debug','info','warn','error']:
                # cof logger print out time result in string format
                WRITER_TABLE[writer](memory_report_string)
            else:
                # default
                coflogger.info(memory_report_string)
            
cofmem = Cofmem()