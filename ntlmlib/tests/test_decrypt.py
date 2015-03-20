from Crypto.Cipher import ARC4
from Crypto.Hash import MD4
import hashlib
import hmac
import struct

def ntowfv2(domain, user, password):
    md4 = MD4.new()
    md4.update(password)
    hmac_context = hmac.new(md4.digest())
    hmac_context.update(user.upper().encode('utf-16le'))
    hmac_context.update(domain.encode('utf-16le'))
    return hmac_context.digest()


username = 'Administrator'
password = 'Pa55w0rd'.encode('utf-16le')

# -- UNCOMMENT TO GET DATA FROM WINRS IMPLEMENTATION --
# -- Extracted these from the packet capture of WinRs running (note different domain?)
#domain = 'MicrosoftAccount'
#response_key = ntowfv2(domain, username, password)
#enc_message = '\x81\xAD\x40\x3D\x3D\x6F\x71\xB0\x48\xE8\x85\x95\x02\xEA\x83\xB4\xAE\xA5\xFF\xBB\xCA\x54\xF5\x27\xFB\x2E\x92\xC1\xA2\xBE\x0B\x76\x59\x3A\x64\x66\x54\x5B\x05\xF6\xA9\x7F\xB1\xAB\x9A\xC9\xF1\x0E\xAC\xB8\x36\xDA\xE5\xEE\xF5\x2E\xDD\xAA\x14\x79\xDF\x84\x69\xE9\x86\xFA\xBE\xE6\xBE\x9F\xCE\x4B\xED\x87\x07\xFE\x52\x62\x87\x8A\xC6\xB4\xF4\xA5\x56\x98\x55\xA5\x3D\x99\x0B\x60\xA3\x29\x49\x1B\xEB\xBF\x5E\x95\x10\xF1\x8F\xBF\x94\xDA\x11\xF9\xD1\x84\x2C\xAF\x39\x81\x2C\x26\xFB\x04\x93\xAA\xFA\x84\xB6\xDF\xBD\xE6\xFA\xD0\x7B\x9A\xC9\x8C\xC5\xBE\x92\x21\x6F\xFA\x98\xC4\xEA\x7C\x09\xEA\x85\x9F\x13\x6D\xCD\xB8\x24\xB5\xDB\x5D\x55\x43\x07\x73\xD8\x73\x64\x90\x7B\x1F\xA5\xBE\xDC\x6C\x3D\x68\x80\x9E\x5E\xE4\xD8\x2F\xE2\x80\x6E\xBA\x16\x36\xED\xAC\x40\xA7\x88\x74\xD4\x66\x94\x17\x0F\x4D\x38\xAD\xAB\xF7\xC0\xCB\xA6\x74\x2F\xD9\x13\x21\x67\x65\x3C\x01\xEF\x95\x8B\x82\xC6\x6F\x09\x2A\x00\xA1\x68\xAE\x46\x19\x8D\xAC\x79\xA0\x2B\xA9\xE8\x8F\xE1\x51\x60\xBB\xF8\xDC\xD5\xA0\x63\x76\x21\xF9\x17\xDF\x21\xA0\xEA\xF5\x9C\x3C\xA1\x57\x98\xC0\x15\x6E\xB7\x22\xEA\x79\xAF\xF6\xA4\x34\xCE\x39\xCA\xF7\xDF\x54\xDC\x62\xD1\xEB\x0D\x63\xDF\x43\x83\x56\xD2\x32\x8D\xF7\xA5\x81\x97\x89\x0B\x78\xD9\xA1\xB5\x62\x00\xC8\x2C\xAF\x45\x54\x77\x0A\xE9\x43\x07\x12\xA6\x89\x04\x39\x6B\x14\x7F\xAA\x04\x28\x56\x08\x99\xFF\xAE\xD0\xFB\x06\xB7\x80\x16\x0B\x7F\x95\xF6\x5B\x95\x4E\x6F\x58\x57\xD0\xF4\xD8\x51\x82\xCD\x9B\xF7\xA5\x7A\x6F\xF1\x6A\x0D\xC3\xED\x47\x0A\xC1\x13\x62\x93\xC8\x20\x5A\x78\xAE\x35\x7D\x21\xC9\xD7\x64\x39\x53\x71\x97\xD3\xF6\x26\x73\x30\xB7\x46\xFE\x38\xD3\xD7\xED\xF1\x38\xEE\x42\x29\x0B\xA2\xF5\x95\x50\x05\xA9\xEF\x44\x63\x1B\x99\x84\x75\xA9\x44\x8C\xA4\xD5\x8F\x8D\x3F\x51\x9A\x9B\xC8\x9B\xE5\x1C\x78\xC1\xBC\x7A\xCB\x54\x2F\xEE\x21\xED\xBA\xD2\x3D\xFB\x1B\x8B\x5E\x83\x6D\xDD\x21\xF8\x3A\xBF\xCE\xB0\xF3\x55\x54\xED\xB2\xC4\x48\x09\xEF\xC7\x1A\x82\x29\x10\xB5\xE5\x3E\x00\x82\x78\x70\x53\x8F\xEC\x80\xEF\x01\x54\x5D\xC9\xED\x7B\xBD\xAC\xAB\xEC\xBA\x78\xC8\x18\x87\x82\xAA\x6D\xE8\x4F\xCB\x04\x0C\x51\x77\x7C\x32\xAC\x3E\xBB\x04\x46\xAB\x15\x5F\xBF\x2D\xF1\x7F\x0D\x9B\x61\xEF\x1F\x8A\xD5\xCF\xA6\xE2\x4E\x21\xDE\x76\x40\x01\x13\x74\x72\x94\xCB\xCA\x0A\xEA\xEF\x76\xD1\x33\xA3\x2B\x3C\xA9\x8C\x9F\xD2\xE7\x6C\xB9\x5F\x68\xDD\x1E\x33\x25\x4D\xEA\x43\x29\x95\xDF\xAD\x41\x99\xB6\x64\xEE\x4F\xFE\x31\xC8\x60\x1D\x73\xA2\xCA\xDB\x49\x67\xAF\x98\xB4\xB2\xC4\x62\x82\xCB\x95\x58\x73\x59\x9F\x79\x96\x8D\x31\x6E\xAD\x95\x9A\xBB\x98\x6A\x34\xBB\xF1\xB0\xE2\xAF\xD2\xC8\x61\x89\xB3\x9B\xA8\x4E\xF0\x9F\x8D\x32\x79\x81\x39\x5D\x67\x8E\xE7\x88\xCE\x7B\x8A\xE1\xED\xC1\xEC\x12\x2D\x8E\x44\x0F\x28\x9A\xA0\xE5\xE6\xC7\x2D\xF9\xC2\x30\xF1\x81\x2D\x03\x6C\x99\xD3\x31\x59\x86\x0B\x87\x2E\x80\x6B\xCF\x47\xD6\xE9\xC1\xE1\x9A\x80\xE3\x87\xDB\x61\xC7\x19\x7F\x93\x89\x31\xD0\xAB\x07\xD1\x4F\x10\xCF\x7D\x1C\x71\x0A\x3C\x25\x74\xA6\x95\xAF\x7B\xEC\x83\x6B\x2A\x81\xAA\x76\xE8\x2C\x25\x8E\xEA\x41\xA9\x8C\x02\xF1\xCA\x9C\xC0\x78\x71\xE6\xB5\xAB\x2B\x88\xB4\x61\x77\xA1\xEE\x1E\x03\x07\x6F\x77\x65\xC9\xC9\x6A\x30\xBD\xF3\xD1\x9B\x17\x1D\xDB\xEE\x36\x22\x74\x90\x61\xD8\xAF\xDE\x28\xE8\x38\x07\x63\xD0\xA8\xF5\xB5\x5D\xD6\xAE\x10\x64\xB8\x52\xDF\xC4\x37\x25\xA5\xE9\xD8\x89\x08\x88\x6F\x4F\xCA\x10\x8E\x4A\x90\x77\xDC\x9E\xD6\x5C\xB0\xFA\xE9\x8F\xBB\x27\xB8\xE1\x60\x8A\xEA\x5F\x00\xEC\x31\x90\x46\x52\x5A\xCB\xE6\x59\x5F\xA8\xC7\x11\x7F\xE0\x0F\x53\xBC\xF5\xC9\x50\xB6\xB8\xD0\xB7\x1E\xB3\x27\x5B\x9F\x18\x69\x09\x4C\xBA\xD3\x19\xB4\x01\x95\x5E\xC5\x1D\x1D\xCC\xEF\x99\x14\x70\x41\xD2\x7C\x79\xB9\x45\xAD\x12\x70\xED\x97\xBD\xBE\xE1\x84\xA7\xA6\xAD\x27\xAB\x99\xBE\xC2\x6A\x3C\xD0\x41\x0A\x1A\x1D\xB9\xB5\xA4\xA5\x1F\xE3\xFB\x32\x44\x2F\xA8\xC1\x31\x6E\xB2\x61\xC3\x40\x4A\x78\x3F\x2B\xDD\x55\xE0\x8B\xDB\x34\x82\xA0\xC1\x44\x3B\x35\xCF\x00\xA0\xD0\xD1\xC0\x37\x1B\xF5\xD4\x3F\xFF\xF7\x4F\x4C\x4B\xEB\x27\xE9\x1F\xAF\xCD\x12\x7A\x5E\xD8\xC5\x53\x5F\x12\x7F\xCC\x81\xC6\x3B\xC9\x57\xF6\xC2\x2B\x6F\x82\x7A\xD7\xCC\xF9\xEF\xB9\x21\xB3\x36\x4D\x5A\x15\x21\x16\xFD\x43\x8B\x40\xB4\x0E\xF6\x04\x4E\x47\xAC\x6A\x80\xA0\x3E\xC7\xDC\xE2\xA3\x19\x03\x35\x83\x93\x60\x8F\xBF\x7A\xA6\x57\x4F\xAD\x75\xF7\x28\x51\xEE\xA7\x8C\xE6\x07\xC8\x96\xC3\x2C\x9F\x8A\x34\x3C\x91\xA1\x8C\x5C\xA9\x08\x41\x03\x7F\x8A\x64\x6F\x49\x98\x4F\x33\x29\x73\x6F\xD9\x3D\xBE\xEE\xF6\xF7\xC4\x8F\x5E\x67\x3B\x7C\x13\x58\xD9\x18\x9F\x84\x13\xAD\xCE\x2B\x6A\xDA\xF7\x1E\x60\x39\x77\x76\x0C\xA2\xD8\x47\xC5\xE0\x43\x6B\xDC\x0D\xCB\x5D\xC2\xDC\xF9\xE5\x38\xB3\xFF\x7B\xAD\xB8\xEC\xAE\xBC\x25\x92\x34\x37\x89\xE4\xF4\xB2\xA4\x2D\x62\x33\xB5\xD7\x7C\x48\xD4\x9B\xB7\x35\x09\x4F\xF6\x48\x32\x35\xD1\x73\xB2\x07\x25\xD5\x92\xF7\xED\x73\xEC\xF2\x1A\x3F\xD8\x46\x1B\xB7\xCF\x99\x5D\x59\x08\x83\xBC\x42\xCD\x64\xFF\x48\x0B\x04\x68\xDA\x5A\x1C\xB8\xDE\x74\xFC\x3A\x18\x2F\x59\x88\x5A\xBA\x47\xF0\x50\xEF\x3B\x5B\x68\x06\x39\xD9\x0B\x13\x13\x64\x75\xB8\x02\xB6\x6A\xD9\x14\xAD\xFE\xCE\x4B\xEA\x70\xCB\x6E\x15\x88\x70\x57\xC6\xA8\x6B\x9C\xF3\x75\xB1\xDC\x78\x94\xF6\x2B\xC0\xC9\x42\xE2\x79\x99\xD4\x24\xB5\x7A\x62\xA9\x00\xB4\xA9\x44\x03\xBD\x03\x7C\x62\xD0\x93\x2E\x98\xD5\x3B\xDF\xE6\xD6\xC3\xF6\xBD\x2F\xE1\x6D\x7D\x2A\x63\x92\x00\x1C\x75\xCC\x49\x9D\xE3\x49\xE6\xAF\xB1\x27\xC2\xAB\x97\xC5\x0D\x7D\x77\x6D\xE7\xC3\xE2\x6D\x96\x1D\xC0\xD6\xE3\xD4\x1E\x14\x83\x7D\x30\x74\x94\x49\x57\x07\xB2\xB8\x70\xA8\x86\xBC\x56\x61\xC5\x44\x7B\xF7\x94\x30\x2C\xA2\xC1\x8C\x24\xC7\x24\x1A\x69\x46\x60\x50\x05\xD2\xE4\xC3\xA6\x94\xD7\xEE\xC9\xBE\x71\x85\x40\x9D\x4A\xC5\x9A\x4A\x11\x94\x53\xB4\xA4\xD5\x11\x39\x9D\xAA\x3A\x76\x9E\x92\x87\x5B\xF1\x93\x6F\x76\xA8\xED\x0D\xC0\x25\xF4\x33\x6B\x0F\x27\x52\x51\xCD\xA3\x05\x15\x57\xB5\x46\xDD\xB2\x02\x3A\x1F\xC9\x92\xBB\x5D\x54\x8D\xE8\x2A\xD9\x29\x9C\xF8\x09\x6A\xAD\x84\xE3\x7D\x12\xC5\xCF\x08\xCC\x06\x97\xBA\x0C\xA6\x13\x98\x94\xDB\x2D\x15\x4A\xFA\x08\xE3\x8F\x65\x79\x72\xE0\xE1\xF5\xD3\x48\x75\x2F\xFF\x6E\xFB\xBE\xEE\x78\x0E\xFB\x51\xD1\x4D\xB5\xE8\xB5\x76\x8D\x37\xAD\x38\x4B\x85\xEA\x99\x46\xA6\x20\x17\xFA\x18\x4C\xE3\xB8\xB7\x99\x25\x06\x64\x07\xF2\xC8\x00\x87\x9F\xF2\x22\xC8\x88\x69\x09\x07\x4C\x35\xA2\x57\x10\x51\x31\x46\x2A\x8C\x59\xBE\x3A\xB1\x2F\xC0\xE2\x61\x5E\x8E\xA5\x4D\x68\xE4\xD9\x8A\x46\x3F\xFD\x4D\x4B\xA6\x56\x24\x7E\xAD\x50\x3D\xCD\x58\x09\x29\x0E\xE3\x4F\xF8\xB5\xF7\xD1\x74\x9D\x11\xBB\x7F\x15\x3E\x56\x70\x4E\x25\x79\x2A\x70\xFA\x68\x90\x19\x44\xAD\xBE\x12\x51\x9F\x68\x4B\xF1\x58\xA6\x3A\xDB\x71\xF9\xCC\x0D\x80\x7F\x80\x8C\x44\x27\xD6\x72\x7A\xC9\xCC\x08\xCA'
#enc_session_key = '\xE8\xF0\xA7\xA3\xB0\xEB\xCC\xA4\xD9\xFE\xBF\xA8\x18\x93\x79\x01'
#proof = '\x1E\x0A\x43\xC1\x9B\xEB\xDE\x4A\xB1\x5B\x11\xEC\x07\xE8\x4A\x7D'
#expected_sig = '\x49\x22\x81\x89\xe2\xa4\x9d\xe3'
# -----------------------------------------


# -- UNCOMMENT TO GET DATA FROM MY IMPLEMENTATION --
# -- Extracted these values from the packet capture of my implementation
domain = 'SERVER2012'
response_key = ntowfv2(domain, username, password)
enc_message ='\x22\x7a\x32\x50\x79\x04\xb2\x78\x03\xd1\x49\x8c\xc8\x62\x68\x44\x80\x1b\x1a\x87\xdb\x3a\x2d\xe1\xe0\xf0\x17\xc5\x2c\xe1\x3b\x82\x05\x07\x8a\x2f\xb8\x13\x2b\xa5\x65\x69\x79\xd4\x93\xa1\x8a\x0b\x21\x78\x86\x78\x7a\xdc\xf3\x44\xc9\x70\x75\x6e\x91\x79\x2d\xb9\xdc\x8f\xb0\x4e\xbc\xe4\x06\x13\xf3\xfa\xf7\x96\x04\xa7\x67\xfe\xa4\x7f\x49\x49\x93\x86\x9a\x41\x4e\x00\xc7\x86\x01\x28\x0e\x91\x39\xb9\x4e\x17\x76\x3e\xf7\xae\x5f\x6a\x81\xa3\x1f\xde\x1c\x96\xff\x63\xcd\x10\x4c\x72\x32\xb9\x54\x14\x2b\x79\xa3\x47\x55\xa8\x3c\x64\xe0\x42\xf4\xae\xb0\xba\xd1\x81\xc1\xdf\x86\x8c\xab\x85\x9c\xbc\x2e\x64\x62\x60\x06\x26\x98\x1c\xa5\x63\xf9\x0d\x59\x33\x1e\x1d\x13\xcc\x8b\xa6\x7a\x0a\xe9\xf0\x51\xf9\x6d\x9c\x86\xa8\x3e\x7e\xb1\x6a\xfc\xcb\xa1\xfa\x7d\x80\x3e\xca\xd0\x74\xc1\x45\x5f\x70\xb4\xeb\x40\x94\xdf\x90\x43\xca\x4e\x0b\x63\x22\xef\x5e\x6b\xda\x52\x5f\xce\x1d\x79\xca\x08\xd9\xf4\xb8\xab\xf2\x3f\x30\x11\x2b\x50\xa6\xe7\x3c\xce\x15\x51\xa4\xc6\xc4\xbf\x87\x25\xdf\x2a\xd7\xc5\xcf\x28\x25\xe6\x98\x2e\x6b\xbc\x06\x3b\x5e\xf6\x0b\x87\xde\x3a\x27\xe8\xdc\xd7\xad\x8c\x6e\xfc\x60\xf0\x1d\x92\x16\x0e\x11\x97\x9d\x69\xf3\x90\xd7\x88\x81\x27\x5a\xa9\xc6\x08\xe0\x55\xdc\x58\x17\xa5\x77\x09\x49\x51\xaf\xfb\xe2\xe9\x3d\xbe\xfa\x7c\x51\xa7\xc6\x3f\x6f\x75\x7c\x94\xb7\x57\xc6\x2a\x42\x5a\x1f\x58\xaa\xd4\x62\x2a\x20\x29\xce\xee\x99\x06\x90\x79\xe4\xa0\x91\x11\xe1\xde\xc1\x39\x96\x93\x9a\xa0\x7b\xc7\x74\xde\xf1\xb5\x86\xad\xa8\x94\x4a\xbb\xa8\xb3\xe7\x4b\x22\xc2\x5a\xe3\xb9\x0b\x8c\xdd\x29\x3c\x23\xaf\x69\x4d\xeb\xd2\x30\x9c\x39\x51\xe9\x7c\x1c\x63\x59\x8f\x65\xd1\x74\xd8\x14\x17\x5d\x90\x82\x47\xff\x65\x6a\xcf\xca\xa4\x87\x00\x59\x1c\x7e\xe2\x3e\x2b\x5e\x20\x06\xb6\x6f\xa7\xe7\x83\x47\x4f\x9e\xc8\x76\x34\xe2\x27\xd7\xee\xf0\xdd\x89\x18\x05\xc5\x52\xfe\xdf\x27\x2e\x54\x0a\xb4\x83\x5c\x41\x2f\x60\x2f\xac\xe9\xaa\x51\x5b\xc1\xbd\xa4\x94\x00\x8f\x72\xcf\x67\xd4\x12\x7e\x66\xd9\x99\xb3\x54\xac\xf1\xa8\xcf\x80\x93\xff\x7d\xad\xe2\xcc\x6b\x00\x91\x78\x25\xad\x5a\x00\x84\x1a\xca\xca\x3a\x98\x17\x97\xbe\xe8\xd7\x5a\x21\xa3\x47\x81\x09\xf7\x52\xae\x9b\x90\x72\xd9\x69\x0a\x8c\x09\x88\x9a\x88\xfa\xa7\x59\xe5\x9a\x02\x35\x6d\xc8\x6b\xa4\x74\xe1\x63\x8b\x85\x08\x37\x06\xf6\xe5\x25\x68\x7f\xb7\x67\xb0\xa5\x44\x58\x30\x83\x4d\x6d\x77\x56\x7e\xd9\x3e\x64\xb5\x8c\xd6\x4a\xfb\x72\xa2\x65\x0d\x52\x73\x77\x7a\x82\x34\xe0\x86\xb1\xd1\x8d\x32\x99\x6c\x66\x88\x19\xa9\xe3\x55\x80\x63\x55\x68\x15\x13\x62\xfd\xb4\x8b\x1e\x90\x9c\xba\xed\xc5\x37\xfb\x5a\xe5\xf0\x7d\x77\x54\xf1\x9f\x14\x94\x45\x53\x64\x94\x3b\x35\xe8\x36\xb7\x2a\x66\x7b\x76\xff\x52\x80\x7a\xac\x41\xb7\xbd\x40\x98\x59\xfb\x95\xa9\x35\xb3\x67\x8c\xac\x18\xe9\x54\x01\x48\x43\xdf\x9d\xd9\xec\xa2\xe5\x7a\x4a\x85\xb5\x1f\x5b\xb1\xe2\x0b\xf9\x4b\xa0\x79\x2a\x0f\x78\x86\x17\xc5\x28\x62\xc7\x4c\xb6\xed\x5c\x6d\xf7\xbc\x80\xdd\xf2\x3b\x29\x53\xc7\x19\xa6\x72\x27\x1a\x35\x44\xf7\xaf\x4c\x85\x5a\x3d\xed\x59\x5c\x43\xca\xc4\x17\xec\x99\xb4\xa8\x79\x19\xf1\xe6\x33\x36\x4f\xed\x12\x2a\x3b\xca\x01\x02\xea\x91\x13\x9d\x54\x38\x98\x28\x94\xc7\xff\x99\xa4\x2e\x4f\xf0\x8a\xa2\x49\x42\x29\xe4\xb4\x02\xd6\x4c\x98\x7f\xde\x36\xd4\xe6\x60\xd0\x39\xdf\xad\xe0\x45\xe8\x69\xaa\xda\xe4\x9c\xb3\x15\xd6\x7b\xda\xa1\x51\xc7\x24\xda\xef\xb0\x8a\xc8\xa8\x8e\x7d\xa8\xcf\x0b\x2d\xab\x72\xe4\x9b\x8b\x9e\xf4\xe1\xe1\x68\x42\x45\xd2\xe6\x57\xdb\x09\xf5\x3a\xb6\x0c\x5f\x67\x51\x7b\xcc\x06\x1a\x01\xfc\x58\x98\x73\xeb\xa1\x43\x23\x57\xb7\xb4\xa2\xc4\x44\x1b\xab\x96\x9e\xaa\xe8\x6c\x97\xf2\x6c\x7e\x9d\xf5\x26\x8d\x10\x96\xb9\xfa\x88\xfd\xd3\x53\x43\x4b\x53\x04\x0b\x4d\x8d\xc0\x1f\x4c\xdb\x27\x34\xd8\x18\x9f\x9a\x9e\xf0\xc0\x44\x9b\x61\x2d\x7b\x3c\xc7\xfd\x33\xf0\xb5\xed\x05\xae\xde\x6b\x7e\x3f\xa9\x09\xe4\x67\x94\x74\x55\x84\xd6\xee\xc2\xc9\xb0\x4d\xf4\xe7\xc0\x2b\x14\x12\xda\x6b\xff\x7b\x46\xbe\x0d\x47\x98\x4f\xbe\xa3\xf2\xdf\xc9\x7f\x1c\x99\x60\xa7\xea\x24\x25\x71\x30\x0b\x3c\x3e\x8e\x2f\x13\x6f\x73\x7b\xe7\x6b\x9c\x6a\xfc\xd4\xda\x58\x16\xc9\x96\x9a\xeb\x67\x05\xdd\x74\xdb\x8d\x3c\xe7\x9c\xb4\xf3\xea\xe2\x74\xa8\xe5\xde\xfd\xe6\xa6\xb8\x5c\x7e\xc1\x3d\x25\x38\xff\x40\x56\x15\x15\xd1\xad\x7d\x72\x8b\x30\x6d\xb7\xc7\xdb\x8a\xcf\x70\x5b\x38\x3e\x48\x70\x4d\x7b\x42\xf6\x97\x09\x3f\xc8\xa4\x15\xe0\x6b\x69\x58\xb9\xe0\x5e\x7d\xc2\x8a\xa5\x70\x3d\xb9\xf5\x61\x86\x26\x36\x7b\x73\x48\x34\x99\x59\x22\x4b\x4f\x0c\xde\xb6\x0a\x76\x06\xeb\x01\xf5\x36\x9c\x0d\x0d\xe5\xe8\x9e\x16\x3e\xa0\xba\x0e\x39\x62\x49\x20\x8e\x8e\xb1\x89\xcc\x21\xe6\x45\xd6\x26\x40\xf6\xde\x57\x48\xfd\x7a\x1a\x23\xd8\x0e\xd8\x48\xa9\x06\x16\xd3\x34\x53\xa3\x67\x9e\xf3\x29\xde\x48\x6b\x45\xa2\xa0\xed\x31\x61\xd9\x87\x70\x64\x41\x86\x52\x74\x9f\x32\xd7\xc3\x40\xb0\x1c\xe4\x81\xf8\x0e\xac\x38\x38\x07\x33\x7b\xc4\x03\x4d\x37\x8d\x55\x4b\x87\xf7\x90\x29\x2c\xe0\x2f\x69\xdc\xa6\xfe\xa6\x44\x45\x7a\xef\x53\x43\x8f\x35\x4f\x29\x1b\x6b\x89\x43\x96\x01\x56\x2c\x59\xc0\x41\x15\xe3\xf9\x45\x1d\x10\xd2\x12\x1f\xc7\x57\x93\xbc\xa3\xcf\xe5\xb0\xa8\xe9\xab\x15\x93\x2d\x65\x36\x13\x5c\x62\xd5\xff\xf8\x95\x6a\x10\xdb\xa3\x66\x78\xdc\x74\xf2\x35\xf0\x8c\x90\xcf\x46\x8d\xc3\xe9\x0f\x52\x6e\x15\x25\x07\x57\x11\xb3\xf1\xe4\x3e\x42\x39\xc6\x4a\x0e\x4e\x5b\x9f\xbf\xbd\x8a\xa7\x65\x35\x28\x52\xb7\x10\x3e\xe4\x32\xb8\xae\x61\x06\x5e\xfb\x01\x1a\xe6\x43\x25\x21\xa0\x92\xbe\x7b\x2b\xe3\x47\xf6\x43\x21\xf1\x32\x67\xcd\xa9\xc8\xda\x43\xce\x96\x7b\x70\x49\x8f\x3f\xbc\xf3\x3e\x5e\x1e\xd2\x7a\x8b\xea\x27\x89\xc8\x34\xa9\xa3\x80\x25\x5d\x74\x7c\x52\x5a\x8f\x9d\xce\x37\x8b\x43\xaa\x59\x9f\x51\xfa\x7d\x71\xbe\xd9\xf2\xc7\x09\xdf\xbc\x0f\x32\x04\x88\x4a\x7c\x43\x27\x6d\x27\x27\x75\x49\x24\x1e\x50\xef\xed\x9f\xaa\xea\xd2\x4a\x49\x12\x06\xaf\x66\x47\xfd\x1b\xe5\x9d\x80\xb2\xc9\xad\xec\xdd\x31\xbc\xfa\xd8\xa2\x38\xd2\x46\x17\x6a\x83\xba\x0c\xfd\xdc\x6c\xf9\xf5\xa0\x83\x9c\x86\xee\x50\x17\xb3\xd4\x0f\x8a\x5c\x6d\x42\x9d\x0d\x08\x42\xdf\xbd\x0c\x21\x99\x0d\xde\x2a\xc7\x6a\xc2\x97\x00\xdf\x49\x95\xf9\xa8\x80\xec\x60'
enc_session_key = '\x20\xa0\xc6\x1a\x02\xc9\xf1\xa6\x3d\x4e\x2a\x69\x58\xb2\x85\xc6'
proof = '\xf4\xba\xda\x8f\xa8\x63\x15\x3f\xdf\xc7\x07\xf7\x55\xb8\x99\x1a'
expected_sig = '\x6b\xcf\xf6\xd0\x47\x6c\x74\xfc'
# -----------------------------------------

# calculate the session master key from the HMAC MD5 of ntowfv2 and the proof string
session_key_hmac = hmac.new(response_key)
session_key_hmac.update(proof)
session_master_key = session_key_hmac.digest()

# decrypt the exchanged session key using RC4 and and the session master key
session_cipher = ARC4.new(session_master_key)
session_key = session_cipher.decrypt(enc_session_key)

# no key weakening since 128bit flag is set

# build the sealing and signing magic
sealing_magic = session_key + "session key to client-to-server sealing key magic constant\x00"
signing_magic = session_key + "session key to client-to-server signing key magic constant\x00"

# MD5 the sealing string to get the encryption key for decrypting the message
md5 = hashlib.new('md5')
md5.update(sealing_magic)
seal_key = md5.digest()

# MD5 the signing string to get the encryption key for decrypting the message
md5 = hashlib.new('md5')
md5.update(signing_magic)
sign_key = md5.digest()

# Initialise the RC4 cipher with the sealing key
cipher = ARC4.new(seal_key)

# attempt to decrypt the data
soap = cipher.decrypt(enc_message)
print soap

# ok.... so we CAN decrypt the WinRS data - now lets calculate the signature checksum


# start with the RC4 cipher to seal with again and encrypt the plaintext
sealing_cipher = ARC4.new(seal_key)
new_enc_message = sealing_cipher.encrypt(soap)

seq = 0
# calculate the signature checksum from the signing key and the encrypted message
hmac_context = hmac.new(sign_key)
hmac_context.update(struct.pack('<i', seq) + soap)

# only first 8 bytes are used
hmac_checksum = hmac_context.digest()[:8]

# encrypt with the sealing cipher
my_checksum = sealing_cipher.encrypt(hmac_checksum)

# oh dear, why is my signature still different
print "calculated checksum: " + ":".join("{:02x}".format(ord(c)) for c in my_checksum)
print "expected checksum:   " + ":".join("{:02x}".format(ord(c)) for c in expected_sig)

print "...now compare this checksum to what was in the packet capture"