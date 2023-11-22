import numpy as np

def uint8_to_uint32(uint8_tab, L) :
    ''' Convert uint8_tab of L uint8 to uint32 tab of L/4 uint32'''
    uint32_tab = np.array([0]*(L//4), dtype='uint32')
    j = 0
    for i in range(0, L, 4) :
        uint32_tab[j] = (np.array(uint8_tab[i],"uint32") << 24) + (np.array(uint8_tab[i+1],"uint32") << 16) + (np.array(uint8_tab[i+2],"uint32") << 8) + (np.array(uint8_tab[i+3],"uint32"))
        j += 1
    return uint32_tab

def uint32_to_uint8(uint32_tab,L) :
    '''Convert uint32_tab of L uint32 to uint32 tab of 4*L uint8'''
    uint8_tab = np.array([0]*(4*L), dtype='uint8')
    j = 0
    for i in range(L) :
        tmp = uint32_tab[i:i+4].view(dtype='uint8')
        uint8_tab[j] = tmp[3]
        uint8_tab[j+1] = tmp[2]
        uint8_tab[j+2] = tmp[1]
        uint8_tab[j+3] = tmp[0]
        j += 4
    return uint8_tab

uint32 = lambda x: x & (2**32-1)
rotl32 = lambda x, k: uint32((x<<k) | (uint32(x) >> (32-k)))

def xoshiro128pp(s):
    result = uint32( rotl32(s[1] * 5, 7)  * 9 )
        
    t = uint32(s[1] << 9)
    s[2] ^= s[0]
    s[3] ^= s[1]
    s[1] ^= s[2]
    s[0] ^= s[3]
    s[2] ^= t
    s[3] = rotl32(s[3], 11)
        
    return result        

def randombytes(seed, L):
    s = np.array([0]*4,dtype='uint32')
    s[0] = uint8_to_uint32(seed,4)[0]
    #Populating all state s
    for i in range(4) :
        xoshiro128pp(s)
    
    result32 = np.array([0]*(L//4),dtype='uint32')
    for i in range(L//4) :
        result32[i] = xoshiro128pp(s)
    
    return uint32_to_uint8(result32,L//4).tobytes()