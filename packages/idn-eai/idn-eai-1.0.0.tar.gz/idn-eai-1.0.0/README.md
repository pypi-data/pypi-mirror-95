# Email Address Internationalization

## _IDN-EAI_

An internationalized domain name (IDN) is an Internet domain name that contains at least one label that is displayed in software applications, in whole or in part, in a language-specific script or alphabet, such as Arabic, Chinese, Cyrillic, Devanagari, Hebrew or the Latin alphabet-based characters with diacritics or ligatures, such as French. These writing systems are encoded by computers in multibyte Unicode. Internationalized domain names are stored in the Domain Name System (DNS) as ASCII strings using Punycode transcription.

EAI is the protocol that allows email addresses with IDNs in the domain part and/or Unicode (non-ASCII) characters in the Local part of the Mailbox name. Email software and services need to make specific changes to support EAI, since EAI mail is conceptually a separate mail stream from legacy ASCII mail.

### Installation

You can install the idn-eai module from [PyPI](https://pypi.org/project/idn-eai/):

    pip install idn-eai

The module is supported on Python 3.7

### Features

- API for finding out whether remote mail server is supporting utf-8 or not.
- Based on the returned string, we will able to find out the SMTPUTF8 support 
on remote mail server
    - "TRUE" : SMTPUTF8 is supported on remote mail server
    - "FALSE" : SMTPUTF8 is not supported on remote mail server
    - "EXCEPTION" : When domain is invalid or unable to resolve
- The internationalized domain name (IDN) homograph attack 
is a way a malicious party may deceive computer users about what remote system they are communicating with, by 
exploiting the fact that many different characters look alike in Hindi language (i.e., they are homographs, hence the term for the 
attack, although technically homoglyph is the more accurate term for different characters that look alike).
- Phonics is a method for teaching people how to read and write an alphabetic language. It is done by demonstrating the 
relationship between the sounds of the spoken language (phonemes), and the letters or groups of letters (graphemes) or 
syllables of the written language. This is also known as the Alphabetic principle or the Alphabetic code.
 
> The overriding goal for this package is to provide 
> API for IDN & EAI related stuffs.

### API Modules

Instructions on how to use them in your own application are linked below.

| Module | Functions |
| ------ | ------ |
| eai.eaichecker |  smtputf8_check(domain) |
| eai.idn_services | generate_homograph_variants(word) |
| eai.idn_services | generate_similar_phonic_variants(word) |

### Examples

- smtputf8_check(gmail.com) will return TRUE string
- smtputf8_check(yahoo.com) will return FALSE string
- smtputf8_check(jsds.ins) will return EXCEPTION string
- generate_homograph_variants(मुद्रा) will return मुद्गा,मुद्रा,मुद्ना as comma-separated string
- generate_similar_phonic_variants(मुद्रा) will return मुद्रा,मूद्रा as comma-separated string


### Environment

This code is tested on **python 3.7**

```sh
# python -v
Python 3.7.3 (default, Apr 24 2020, 18:51:23) 
[Clang 11.0.3 (clang-1103.0.32.62)] on darwin
```

### Developer: 
- [Arpit Gupta](https://www.arpitram.com) <gupta.arpit03@gmail.com>
- **www.arpitram.com, www.arpitram.in**

### License

MIT
