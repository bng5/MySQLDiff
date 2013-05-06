
import random
import math

class Jumble:
    def __init__(self):

        self.errors = []#        # array of error messages

        ## Each of these two strings must contain the same characters, but in a different order.
        ## Use only printable characters from the ASCII table.
        ## Do not use single quote, double quote or backslash as these have special meanings in PHP.
        ## Each character can only appear once in each string.

        #     # 1st string of ASCII characters
        self.scramble1 = '! #$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        #     # 2nd string of ASCII characters
        self.scramble2 = 'f^jAE]okIOzU[2&q1{3`h5w_794p@6s8?BgP>dFV=m D<TcS%Ze|r:lGK/uCy.Jx)HiQ!#$~(;Lt-R}Ma,NvW+Ynb*0X'

        if len(self.scramble1) <> len(self.scramble2):
            trigger_error('** SCRAMBLE1 is not same length as SCRAMBLE2 **', E_USER_ERROR)
            
        #           # 1st adjustment value (optional)
        self.adj = 1.75#  # this value is added to the rolling fudgefactors
        #           # 2nd adjustment value (optional)
        self.mod = 3#     # if divisible by this the adjustment is made negative

    """
    decrypt string into its original form

     @param string $source
     @param string $key
     @return string
    """
    def decrypt(self, source, key = None):
        print source
        self.errors = []

        if key == None:
            key = source[0:8]
            source = source[8:]
        ## convert $key into a sequence of numbers
        fudgefactor = self._convertKey(key)
        if self.errors:
            return

        if len(source) == 0:
            self.errors.append('No value has been supplied for decryption')
            return

        target = ''#None
        factor2 = 0

        i = 0
        while i < len(source):
            # extract a (multibyte) character from source
            #if (function_exists('mb_substr')) {
            #    char2 = mb_substr(source, i, 1)
            #} else {
            char2 = source[i]
            #}

            # identify its position in scramble2
            #num2 = strpos(self.scramble2, char2)
            # returns -1 when not found:
            num2 = self.scramble2.find(char2)
            if num2 == -1:
                self.errors.append("Source string contains an invalid character (char2)")
                return

            # get an adjustment value using fudgefactor
            adj = self._applyFudgeFactor(fudgefactor)

            factor1 = factor2 + adj                 # accumulate in factor1
            num1    = num2 - int(round(factor1))         # generate offset for scramble1
            num1    = self._checkRange(num1)
            factor2 = factor1 + num2                # accumulate in factor2

            # extract (multibyte) character from scramble1
            #if (function_exists('mb_substr')) {
            #    char1 = mb_substr(self.scramble1, num1, 1)
            #} else {
            char1 = self.scramble1[num1]
            #} # if

            # append to target string
            target = target+char1

            i = i+1
            #echo "char1=char1, num1=num1, adj= adj, factor1= factor1, num2=num2, char2=char2, factor2= factor2<br />\n"
        return target.rstrip()

    """
     * encrypt string into a garbled form
     *
     * @param string source
     * @param string key
     * @param int sourcelen
     * @return string
     """
    def encrypt (self, source, key = None, sourcelen = 0):
        #self.errors = array()

        if key == None:
            key = self._genKey()
        # convert key into a sequence of numbers
        fudgefactor = self._convertKey(key)

        if len(self.errors):
            return

        if len(source) == 0:
            self.errors.append('No value has been supplied for encryption')
            return

        # pad source with spaces up to sourcelen
        source = source.rjust(sourcelen)

        target = ''#None
        factor2 = 0

        i = 0
        while i < len(source):
            # extract a (multibyte) character from source
            #if (function_exists('mb_substr')) {
            #    char1 = mb_substr(source, i, 1)
            #} else {
            char1 = source[i]
            #} # if

            # identify its position in scramble1
            num1 = self.scramble1.find(char1)
            if num1 == -1:
                self.errors.append("Source string contains an invalid character (char1)")
                return

            # get an adjustment value using fudgefactor
            adj = self._applyFudgeFactor(fudgefactor)
            factor1 = factor2 + adj             # accumulate in factor1
            num2    = round(factor1) + num1     # generate offset for scramble2
            num2    = int(self._checkRange(num2))
            factor2 = factor1 + num2            # accumulate in factor2

            # extract (multibyte) character from scramble2
            #if function_exists('mb_substr')) {
            #    char2 = mb_substr(self.scramble2, num2, 1)
            #} else {
            char2 = self.scramble2[num2]
            #} # if

            # append to target string
            target += char2

            i = i+1

            #echo "char1=char1, num1=num1, adj= adj, factor1= factor1, num2=num2, char2=char2, factor2= factor2<br />\n"
        return key+target

    """
    # return the adjustment value
    """
    def getAdjustment(self):
        return self.adj

    """
    # return the modulus value
    """
    def getModulus (self):
        return self.mod

    """
    # set the adjustment value
    """
    def setAdjustment (self, adj):
        self.adj = float(adj)

    """
     * set the modulus value
     *
     * @param <type> mod
     """
    def setModulus (self, mod):
        self.mod = int(abs(mod))    # must be a positive whole number

    """
     * return an adjustment value  based on the contents of fudgefactor
     * NOTE: fudgefactor is passed by reference so that it can be modified
     *
     * @param array &fudgefactor
     * @return <type>
     """
    def _applyFudgeFactor(self, fudgefactor):
        fudge = fudgefactor.pop(0)     # extract 1st number from array
        fudge = fudge + self.adj           # add in adjustment value
        fudgefactor.append(fudge)                # put it back at end of array

        if self.mod > 0:               # if modifier has been supplied
            if math.floor(fudge % self.mod) == 0:     # if it is divisible by modifier
                fudge = (fudge * -1)           # make it negative
        return fudge

    """
     * check that num points to an entry in self.scramble1
     *
     * @param <type> num
     * @return <type>
     """
    def _checkRange (self, num):
        num = int(round(num))         # round up to nearest whole number
        limit = len(self.scramble1)

        while num >= limit:
            num -= limit
        while num < 0:
            num += limit
        return num

    """
     * convert key into an array of numbers
     *
     * @param string key
     * @return array
     """
    def _convertKey (self, key):
        if len(key) == 0:
            self.errors.append('No value has been supplied for the encryption key')
            return
        array = []
        array.append(len(key))    # first entry in array is length of key

        tot = 0
        i = 0
        while i < len(key):
            # extract a (multibyte) character from key
            #if (function_exists('mb_substr')) {
            #    char = mb_substr(key, i, 1)
            #} else {
            char = key[i]
            #} # if

            # identify its position in scramble1
            num = self.scramble1.find(char)
            if num == -1:
                self.errors.append("Key contains an invalid character (char)")
                return

            array.append(num)        # store in output array
            tot = tot + num     # accumulate total for later
            i = i + 1

        array.append(tot)            # insert total as last entry in array

        return array

    """
     *
     * @param int length
     * @return string
     """
    def _genKey(self, length = 8):
        clave_caract = ".0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
        cod_aut = ""
        max = len(clave_caract)-1
        i = 0
        while i < length:
            cod_aut = cod_aut + clave_caract[random.randint(0, max)]
            i = i+1
        return cod_aut
