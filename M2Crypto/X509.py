"""M2Crypto wrapper for OpenSSL X509 API.

Copyright (c) 1999-2000 Ng Pheng Siong. All rights reserved. """

RCS_id='$Id: X509.py,v 1.3 2000/02/23 15:42:18 ngps Exp $'

# M2Crypto
import ASN1, BIO
import M2Crypto 
m2=M2Crypto

m2.x509_init()

V_OK = m2.X509_V_OK

class X509_Store_Context:
    def __init__(self, x509_store_ctx):
        self.ctx = x509_store_ctx


class X509_Name:
    nid = {'C'  : m2.NID_countryName,
           'SP' : m2.NID_stateOrProvinceName,
           'L'  : m2.NID_localityName,
           'O'  : m2.NID_organizationName,
           'OU' : m2.NID_organizationalUnitName,
           'CN' : m2.NID_commonName,
           'Email' : m2.NID_pkcs9_emailAddress}

    def __init__(self, x509_name):
        assert x509_name is not None
        self.x509_name = x509_name

    def __str__(self):
        return m2.x509_name_oneline(self.x509_name)

    def __getattr__(self, attr):
        if attr in self.nid.keys():
            return m2.x509_name_by_nid(self.x509_name, self.nid[attr])
        else:
            raise AttributeError, self, attr


class X509:
    def __init__(self, x509):
        assert not x509 is None
        self.x509=x509

    def as_text(self):
        buf=BIO.MemoryBuffer()
        m2.x509_print(buf.bio_ptr(), self.x509)
        return buf.read_all()

    def as_der(self):
        buf=BIO.MemoryBuffer()
        m2.i2d_x509(buf.bio_ptr(), self.x509)
        return buf.read_all()

    def get_version(self):
        return m2.x509_get_version(self.x509)

    def get_serial_number(self):
        asn1_integer = m2.x509_get_serial_number(self.x509)
        return m2.asn1_integer_get(asn1_integer)

    def get_not_before(self):
        return ASN1.ASN1_UTCTIME(m2.x509_get_not_before(self.x509))

    def get_not_after(self):
        return ASN1.ASN1_UTCTIME(m2.x509_get_not_after(self.x509))

    def get_pubkey(self):
        return m2.x509_get_pubkey(self.x509)

    def get_issuer(self):
        return X509_Name(m2.x509_get_issuer_name(self.x509))

    def get_subject(self):
        return X509_Name(m2.x509_get_subject_name(self.x509))

def load_cert(pemfile):
    f=BIO.openfile(pemfile)
    cptr=m2.x509_read_pem(f.bio_ptr())
    f.close()
    if cptr is None:
        raise Err.get_error()
    return X509(cptr)


class X509_Stack:
    def __init__(self, stack):
        self.stack=stack

    def __len__(self):
        return m2.sk_x509_num(self.stack)

    def __getitem__(self, idx):
        if idx < 0 or idx >= m2.sk_x509_num(self.stack):
            raise IndexError, 'index out of range'
        v=m2.sk_x509_value(self.stack, idx)
        return X509(v)


class Request:
    def __init__(self, req):
        self.req = req

    def as_text(self):
        buf=BIO.MemoryBuffer()
        m2.x509_req_print(buf.bio_ptr(), self.req)
        return buf.read_all()

def load_request(pemfile):
    f=BIO.openfile(pemfile)
    cptr=m2.x509_req_read_pem(f.bio_ptr())
    f.close()
    if cptr is None:
        raise Err.get_error()
    return Request(cptr)


class CRL:
    def __init__(self, crl):
        self.crl = crl

    def as_text(self):
        buf=BIO.MemoryBuffer()
        m2.x509_crl_print(buf.bio_ptr(), self.crl)
        return buf.read_all()

def load_crl(pemfile):
    f=BIO.openfile(pemfile)
    cptr=m2.x509_crl_read_pem(f.bio_ptr())
    f.close()
    if cptr is None:
        raise Err.get_error()
    return CRL(cptr)


