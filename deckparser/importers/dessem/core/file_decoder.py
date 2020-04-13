from chardet.universaldetector import UniversalDetector
import chardet
import logging

def getLogger():
    return logging.getLogger(__name__)

class FileDecoder:
    def __init__(self, file_path, preferred_encodings=None, confidence_threshold=0.8):
        self.file_path = file_path
        self.file = None
        self.detector = UniversalDetector()
        self.preferred_encodings = preferred_encodings
        self.confidence_threshold = confidence_threshold
    
    def __enter__(self):
        self.file = open(self.file_path, 'rb')
        return self
    
    def __exit__(self, _type, _value, _traceback):
        self.close()
    
    def __iter__(self):
        return self

    def __next__(self):
        line = self.file.readline()
        if not line:
            raise StopIteration()
        cd = chardet.detect(line)
        enc = cd['encoding']
        cf = cd['confidence']
        if not self.detector.done:
            self.detector.feed(line)
        try:
            s = str(line, enc)
            if cf < self.confidence_threshold:
                getLogger().debug('Low confidence level ({:.2f}) for encoding "{:s}" reading "{}"'.
                                 format(cf, enc, s.strip()))
                return self.__alternative_decode(line)
            return s
        except UnicodeDecodeError:
            getLogger().debug('Could not read line "{}" with detected encoding "{:s}"'.format(line, enc))
            s = self.__alternative_decode(line)
            if not s:
                raise
            return s
    
    def get_encodings(self):
        encondings = []
        if self.preferred_encodings:
            encondings.extend(self.preferred_encodings)
        if self.detector.done:
            d_enc = self.detector.result['encoding']
            if d_enc not in encondings:
                encondings.insert(0, d_enc)
        return encondings
    
    def __alternative_decode(self, line):
        for enc in self.get_encodings():
            try:
                s = str(line, enc)
                getLogger().debug('Line "{}" read successfully with encoding: {:s}'.format(s.strip(), enc))
                return s
            except UnicodeDecodeError:
                getLogger().debug('Could not read line "{}" with encoding: {:s}'.format(line, enc))
                continue
        getLogger().warn('Failed to read line "{}", encodings: {:s}'.
                         format(line, str([enc] + self.get_encodings())))
    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None
