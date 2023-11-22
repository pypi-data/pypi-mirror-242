import time
import torch
from .cofwriter import coflogger, coftb, WRITER_TABLE


class _Timer:
    """Timer."""

    def __init__(self, name):
        self.name_ = name
        self.elapsed_ = 0.0
        self.started_ = False

    def __enter__(self):
        self.start()
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        """Start the timer."""
        assert not self.started_, 'timer has already been started'
        torch.cuda.synchronize()
        self.start_time = time.time()
        self.started_ = True

    def stop(self):
        """Stop the timer."""
        assert self.started_, 'timer is not started'
        torch.cuda.synchronize()
        self.elapsed_ += (time.time() - self.start_time)
        self.started_ = False

    def reset(self):
        """Reset timer."""
        self.elapsed_ = 0.0
        self.started_ = False

    def elapsed(self, reset=True):
        """Calculate the elapsed time."""
        started_ = self.started_
        # If the timing in progress, end it first.
        if self.started_:
            self.stop()
        # Get the elapsed time.
        elapsed_ = self.elapsed_
        # Reset the elapsed time
        if reset:
            self.reset()
        # If timing was in progress, set it back.
        if started_:
            self.start()
        return elapsed_
    
class Timers:
    """Group of timers."""

    def __init__(self):
        self.timers = {}

    def __call__(self, name):
        if name not in self.timers:
            self.timers[name] = _Timer(name)
        return self.timers[name]
    
    def log(self, normalizer=1.0, timedict=False, writer=None):
        """Log a group of timers."""
        assert normalizer > 0.0

        string = 'time (ms)'
        reset=True
        names = self.timers.keys()
        time_dict = {
                name:self.timers[name].elapsed(
                    reset=reset) * 1000.0 / normalizer for name in names
            }
        if timedict:
            return time_dict
        for k,v in time_dict.items():
            string += ' | {}: {:.2f}'.format(k, v)
        if writer in ['tb', 'csv']:
            # write time profiling results in dictionary format
            WRITER_TABLE[writer](time_dict)
        elif writer in ['debug','info','warn','error']:
            # cof logger print out time result in string format
            WRITER_TABLE[writer](string)
        else:
            # use coflogger.info in default
            coflogger.info(string)
        return None

coftimer=Timers()